import os
import re
from datetime import date
from time import time

import pdfplumber

from query import *

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

@timer
def count_articles(filename, data):
    text = ""
    folder = get_pdf_folder(data)
    with pdfplumber.open(os.path.join(folder, filename)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    # Ogni articolo ha un marcatore univoco tipo [§27225702§]
    articles = re.findall(r'\[§\d+§]', text)

    # Rimuovi duplicati (lo stesso marcatore appare su più pagine)
    unique_articles = set(articles)

    return len(unique_articles)

def process_pdf(filename, data):
    articles = count_articles(filename, data)
    try:
        update_articles_number(filename, articles)
    except Exception as e:
        print(f'Errore: {e}')
