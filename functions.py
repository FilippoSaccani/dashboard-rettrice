import os
import re
from datetime import date
from time import time
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
        file.save(os.path.join(folder, new_filename))
        return True, ""
    except FileExistsError:
        return False, "Errore: duplicato"
    except Exception:
        return False, "Errore nell'archiviazione del file"

def delete_pdf(path):
    if os.path.exists(path):
        os.remove(path)
        return True, "File rimosso correttamente"
    else:
        return False, "Errore nell'eliminazione del file"

def extract_articles(filename, data):
    text = ""
    folder = get_pdf_folder(data)
    with pdfplumber.open(os.path.join(folder, filename)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

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

@timer
def process_pdf(filename, data):
    articles = extract_articles(filename, data)
    try:
        insert_rassegna(filename, data, len(articles))
        for article in articles:
            # print("Tema: ", article["tema"], " Testata: ", article['testata'])
            ok, error = insert_articolo(filename, article['tema'], article['testata'])

            if not ok:
                print(error)
                return error, 400

        # update_articles_number(filename, articles)
    except Exception as e:
        print(f'Errore: {e}')
