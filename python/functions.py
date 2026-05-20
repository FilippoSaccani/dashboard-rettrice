import os
from collections import defaultdict
from datetime import date
from time import time, sleep

import pdfplumber

from python.query import *

# Boilerplate da ignorare
BOILERPLATE = re.compile(
    r'Riproduzione autorizzata|'
    r'^(domenica|lunedì|martedì|mercoledì|giovedì|venerdì|sabato)\b|'
    r'^Pagina\s+\d+|'
    r'©?\s*RIPRODUZIONE RISERVATA|'
    r'^\d{1,4}$',
    re.IGNORECASE
)

MESI = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
        'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']


def timer(func):
    # functools.wraps preserva il nome e il docstring della funzione originale
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        print(f'Function {func.__name__!r} executed in {(time() - t1):.4f}s')
        return result

    return wrap


def get_date_from_formatted(data: str) -> date:
    """Converte una stringa data in oggetto date. Solleva ValueError se il formato non è valido."""
    for fmt in ('%Y-%m-%d', '%d/%m/%Y'):
        try:
            from datetime import datetime
            return datetime.strptime(data, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Formato data non valido: {data}")


def get_pdf_folder(data: date) -> str:
    return os.path.join('static/pdfs', str(data.year), MESI[data.month - 1])


def get_pdf_name(giorno: str) -> str:
    return f'Unimore{giorno}.pdf'


def save_pdf(file, data: date, new_filename: str) -> tuple[bool, str]:
    try:
        folder = get_pdf_folder(data)
        os.makedirs(folder, exist_ok=True)
        full_path = os.path.join(folder, new_filename)

        if os.path.exists(full_path):
            return False, "Questa rassegna è già stata inserita"

        file.save(full_path)
        file.flush()
        os.fsync(file.fileno())
        return True, ""
    except Exception as e:
        return False, "Errore nell'archiviazione del file"


def delete_pdf(path: str) -> tuple[bool, str]:
    try:
        os.remove(path)
        return True, ""
    except FileNotFoundError:
        return False, "File non trovato"
    except Exception as e:
        return False, f"Errore nell'eliminazione: {e}"


def extract_text(filename: str, data: date) -> str:
    text = ""
    path = os.path.join(get_pdf_folder(data), filename)
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def extract_articles(text: str) -> list[dict]:
    parts = re.split(r'(\[§\d+§])', text)
    articles_raw = defaultdict(str)
    current_marker = None

    for part in parts:
        if re.fullmatch(r'\[§\d+§]', part.strip()):
            current_marker = part.strip()
        elif current_marker:
            articles_raw[current_marker] += part

    results = []
    for marker, content in articles_raw.items():
        lines = [
            l.strip() for l in content.split('\n')
            if l.strip() and not BOILERPLATE.search(l.strip())
        ]

        if len(lines) < 2:
            continue

        # Testata e tema sono le prime 2 righe significative
        results.append({
            'marker': marker,
            'testata': lines[0],
            'tema': lines[1],
        })

    return results


def clean_text(text: str) -> str:
    patterns = [
        (r'\[§\d+§]', ''),
        (r'Riproduzione autorizzata licenza Ars Promopress[^\n]*', ''),
        (r'©?\s*RIPRODUZIONE RISERVATA[^\n]*', ''),
        (r'(?m)^Pagina\s+\d+\s*$', ''),
        (r'(?mi)^(lunedì|martedì|mercoledì|giovedì|venerdì|sabato|domenica)\s+\d{1,2}\s+\w+\s+\d{4}\s*$', ''),
        (r'(?m)^\s*\d+\s*$', ''),
        (r'\n{3,}', '\n\n'),
    ]
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)
    return text.strip()


def _abort(status: dict, pdf_path: str, error: str) -> tuple[bool, str]:
    """Segna il processo come fallito, elimina il PDF e ritorna l'errore."""
    status["done"] = True
    status["error"] = True
    delete_pdf(pdf_path)
    return False, error


@timer
def process_pdf(filename: str, data: date, status: dict) -> tuple[bool, str]:
    pdf_path = os.path.join(get_pdf_folder(data), filename)

    sleep(0.3)

    try:
        text = extract_text(filename, data)
        articles = extract_articles(text)

        if not articles:
            return _abort(status, pdf_path, "File non valido")

        # Usa set per ricerca O(1) invece di lista O(n)
        temi = {r[0] for r in select_all_temi()}
        testate = {r[0] for r in select_all_testate()}

        ok, rassegna_id = insert_rassegna(filename, data, len(articles), clean_text(text))
        if not ok:
            return _abort(status, pdf_path, rassegna_id)  # rassegna_id contiene l'errore se ok=False

        for article in articles:
            tema = article['tema'].strip()
            testata = article['testata'].strip()

            if tema not in temi:
                ok, err = insert_tema(tema)
                if not ok:
                    return _abort(status, pdf_path, err)
                temi.add(tema)

            if testata not in testate:
                ok, err = handle_new_testata(testata)
                if not ok:
                    return _abort(status, pdf_path, err)
                testate.add(testata)

            ok, err = insert_articolo(rassegna_id, tema, testata)
            if not ok:
                return _abort(status, pdf_path, err)

    except Exception as e:
        return _abort(status, pdf_path, str(e))

    status["done"] = True
    status["error"] = False
    return True, ''
