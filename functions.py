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

def date_from_pdf(filename):
    match_dmy = re.search(r'(\d{2})(\d{2})(\d{4})', filename)
    match_ymd = re.search(r'(\d{4})(\d{2})(\d{2})', filename)

    if match_dmy:
        day, month, year = int(match_dmy.group(1)), int(match_dmy.group(2)), int(match_dmy.group(3))
    elif match_ymd:
        year, month, day = int(match_ymd.group(1)), int(match_ymd.group(2)), int(match_ymd.group(3))
    else:
        return None

    try:
        return date(year, month, day)
    except ValueError:
        return None

def validate_filename(filename):
    match_dmy = re.match(r'^Unimore(\d{2})(\d{2})(\d{4})\.pdf$', filename)
    match_ymd = re.match(r'^Unimore(\d{4})(\d{2})(\d{2})\.pdf$', filename)

    if match_dmy:
        day, month, year = int(match_dmy.group(1)), int(match_dmy.group(2)), int(match_dmy.group(3))
    elif match_ymd:
        year, month, day = int(match_ymd.group(1)), int(match_ymd.group(2)), int(match_ymd.group(3))
    else:
        return False, 'Il nome del file deve essere nel formato UnimoreGGMMAAAA.pdf o UnimoreAAAAMMGG.pdf'

    try:
        data = date(year, month, day)
    except ValueError:
        return False, 'La data nel nome del file non è valida'

    if data > date.today():
        return False, 'La data nel nome del file non può essere successiva ad oggi'

    return True, None

def get_pdf_folder(data):
    mesi = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']

    return os.path.join('static/pdfs', str(data.year), mesi[data.month - 1])

def save_pdf(file, data):
    try:
        folder = get_pdf_folder(data)
        os.makedirs(folder, exist_ok=True)
        file.save(os.path.join(folder, file.filename))
        return True, ""
    except FileExistsError:
        return False, "Errore: duplicato"
    except Exception:
        return False, "Errore nell'archiviazione del file"

@timer
def count_articles(filename):
    text = ""
    folder = get_pdf_folder(date_from_pdf(filename))
    with pdfplumber.open(os.path.join(folder, filename)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    # Ogni articolo ha un marcatore univoco tipo [§27225702§]
    articles = re.findall(r'\[§\d+§]', text)

    # Rimuovi duplicati (lo stesso marcatore appare su più pagine)
    unique_articles = set(articles)

    return len(unique_articles)

def process_pdf(filename):
    articles = count_articles(filename)
    try:
        update_articles_number(filename, articles)
    except Exception as e:
        print(f'Errore: {e}')
