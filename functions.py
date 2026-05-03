import os
from datetime import date
from time import time, sleep
from collections import defaultdict
import pdfplumber

from query import *

# Boilerplate da ignorare
BOILERPLATE = re.compile(
    r'Riproduzione autorizzata|'
    r'^(domenica|lunedì|martedì|mercoledì|giovedì|venerdì|sabato)\b|'
    r'^Pagina\s+\d+|'
    r'©?\s*RIPRODUZIONE RISERVATA|'
    r'^\d{1,4}$',
    re.IGNORECASE
)

def timer(func):
    def wrap(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap

def get_date_from_formatted(data):
    fields = data.split('-')

    if len(fields) == 3:
        return date(int(fields[0]), int(fields[1]), int(fields[2]))
    else:
        fields = data.split('/')
        if len(fields) == 3:
            return date(int(fields[2]), int(fields[1]), int(fields[0]))
        else:
            return False, "Formato data non valido"

def get_pdf_folder(data):
    mesi = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']

    return os.path.join('static/pdfs', str(data.year), mesi[data.month - 1])

def save_pdf(file, data, new_filename):
    try:
        folder = get_pdf_folder(data)
        os.makedirs(folder, exist_ok=True)

        full_path = os.path.join(folder, new_filename)

        # Controllo esplicito se il file esiste
        if os.path.exists(full_path):
            return False, "Questa rassegna è già stata inserita"

        file.save(os.path.join(folder, new_filename))
        file.flush()  # Passa i dati al sistema operativo
        os.fsync(file.fileno()) # Forza la scrittura fisica sul disco
        return True, ""
    except Exception:
        return False, "Errore nell'archiviazione del file"

def delete_pdf(path):
    if os.path.exists(path):
        os.remove(path)
        return True, "File rimosso correttamente"
    else:
        return False, "Errore nell'eliminazione del file"

def extract_text(filename, data):
    """Estrae il testo grezzo dal PDF."""
    text = ""
    folder = get_pdf_folder(data)
    with pdfplumber.open(os.path.join(folder, filename)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_articles(text):
    # Splitta mantenendo i marcatori come delimitatori
    parts = re.split(r'(\[§\d+§])', text)

    # Accumula il testo per ogni marcatore univoco
    articles_raw = defaultdict(str)
    current_marker = None

    for part in parts:
        if re.fullmatch(r'\[§\d+§]', part.strip()):
            current_marker = part.strip()
        elif current_marker:
            articles_raw[current_marker] += part

    # Estrai testata e tema da ogni blocco
    results = []
    for marker, content in articles_raw.items():
        lines = [
            l.strip() for l in content.split('\n')
            if l.strip() and not BOILERPLATE.search(l.strip())
        ]

        if len(lines) < 2:
            continue

        # Le ultime 2 righe significative sono sempre testata e tema
        testata = lines[0]
        tema = lines[1]

        results.append({
            'marker': marker,
            'testata': testata,
            'tema': tema,
        })

    return results

def clean_text(text: str) -> str:
    # Rimuovi i marcatori univoci degli articoli
    text = re.sub(r'\[§\d+§]', '', text)
    # Rimuovi i boilerplate di riproduzione
    text = re.sub(r'Riproduzione autorizzata licenza Ars Promopress[^\n]*', '', text)
    text = re.sub(r'©?\s*RIPRODUZIONE RISERVATA[^\n]*', '', text)
    # Rimuovi le righe con solo "Pagina X"
    text = re.sub(r'(?m)^Pagina\s+\d+\s*$', '', text)
    # Rimuovi date in testa alle pagine (es. "domenica 15 febbraio 2026")
    text = re.sub(r'(?m)^(lunedì|martedì|mercoledì|giovedì|venerdì|sabato|domenica)\s+\d{1,2}\s+\w+\s+\d{4}\s*$', '',
                  text, flags=re.IGNORECASE)
    # Rimuovi righe con solo numeri (numeri di pagina)
    text = re.sub(r'(?m)^\s*\d+\s*$', '', text)

    return text.strip()

@timer
def process_pdf(filename, data, status):
    path = get_pdf_folder(data)

    sleep(0.3)

    try:
        text = extract_text(filename, data)
        articles = extract_articles(text)

        if len(articles) == 0:
            print("File non valido")
            status["done"] = True
            status["error"] = True
            delete_pdf(os.path.join(path, filename))

            return False, "File non valido"

        temi = select_all_temi()
        temi = [r[0] for r in temi]

        testate = select_all_testate()
        testate = [row[0] for row in testate]

        ok, rassegna_id = insert_rassegna(filename, data, len(articles), clean_text(text))

        for article in articles:
            tema = article['tema'].strip()
            testata = article['testata'].strip()

            if tema not in temi:
                ok, error = insert_tema(tema)

                if not ok:
                    print("Tema: ", error)
                    status["done"] = True
                    status["error"] = True
                    delete_pdf(os.path.join(path, filename))

                    return ok, error

                temi = select_all_temi()

            if testata not in testate:
                ok, error = handle_new_testata(testata)

                if not ok:
                    print("Testata: ", error)
                    status["done"] = True
                    status["error"] = True
                    delete_pdf(os.path.join(path, filename))

                    return ok, error

                testate = select_all_testate()

            ok, error = insert_articolo(rassegna_id, tema, testata)

            if not ok:
                print("Database: ", error)
                status["done"] = True
                status["error"] = True
                delete_pdf(os.path.join(path, filename))

                return ok, error
    except Exception as e:
        print(f'Errore: {e}')
        status["done"] = True
        status["error"] = True
        delete_pdf(os.path.join(path, filename))

        return False, e

    status["done"] = True
    status["error"] = False
    return True, ''
