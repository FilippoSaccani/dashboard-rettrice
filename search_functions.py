import re
from dataclasses import dataclass
import httpx
from bs4 import BeautifulSoup
import ollama
import json
import sqlite3
from datetime import datetime

# LIVELLO 1
@dataclass
class TestataPrediction:
    scala: str  # 'Locale', 'Nazionale', 'Internazionale'
    importanza: float  # 0-10
    confidence: float  # 0-1
    metodo: str

# Pattern per domini noti
LOCALE_PATTERNS = [
    r'\b(modena|reggio|parma|bologna|ferrara|ravenna|forlì|cesena|rimini|carpi|'
    r'sassuolo|mirandola|vignola|nonantola|piacenza)\b',
    r'\b(gazzetta|cronaca|corriere)\s+di\b',
    r'modena\d{4}|reggio\d{4}|emilia\d{4}',
    r'\.(mo|re|bo|pr|pc|fe|ra|rn|fc)\.it$',  # TLD provinciali
]

NAZIONALE_PATTERNS = [
    r'\b(corriere\s+della\s+sera|repubblica|stampa|sole\s*24|messaggero|'
    r'giornale|fatto\s+quotidiano|avvenire|libero|mattino)\b',
    r'\.it$',  # generico ma esclude .com/.co.uk ecc.
]

INTERNAZIONALE_PATTERNS = [
    r'\b(guardian|times|reuters|bloomberg|bbc|cnn|le\s+monde|spiegel|'
    r'new\s+york\s+times|washington\s+post|financial\s+times)\b',
    r'\.(com|co\.uk|fr|de|es|nl|be)(/|$)',
]

# Pesi per importanza euristica
IMPORTANCE_HINTS = {
    'corriere della sera': 9.5,
    'sole 24 ore': 9.2,
    'repubblica': 9.0,
    'la stampa': 8.5,
    'fatto quotidiano': 7.5,
    'avvenire': 7.0,
    'agenparl': 4.0,
}

def heuristic_classify(testata_name: str) -> TestataPrediction | None:
    name_lower = testata_name.lower().strip()

    # Check importanza diretta
    for key, imp in IMPORTANCE_HINTS.items():
        if key in name_lower:
            scala = 'Nazionale' if imp > 6 else 'Locale'
            return TestataPrediction(scala, imp, 0.9, 'euristica_diretta')

    # Pattern locali prima (più specifici)
    for pat in LOCALE_PATTERNS:
        if re.search(pat, name_lower):
            return TestataPrediction('Locale', 4.5, 0.75, 'euristica_regex')

    for pat in INTERNAZIONALE_PATTERNS:
        if re.search(pat, name_lower):
            return TestataPrediction('Internazionale', 7.0, 0.7, 'euristica_regex')

    for pat in NAZIONALE_PATTERNS:
        if re.search(pat, name_lower):
            return TestataPrediction('Nazionale', 6.0, 0.65, 'euristica_regex')

    return None  # Nessun match, vai al livello 2

#LIVELLO 2
def search_testata_info(testata_name: str) -> dict | None:
    """
    Cerca informazioni sulla testata tramite DuckDuckGo (no API key).
    Estrae indicatori di reach da snippet di risultati.
    """
    query = f'"{testata_name}" giornale testata giornalistica tiratura traffico'

    try:
        # DuckDuckGo HTML search (no rate limit severo)
        resp = httpx.get(
            'https://html.duckduckgo.com/html/',
            params={'q': query},
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=5.0
        )
        soup = BeautifulSoup(resp.text, 'html.parser')
        snippets = [r.get_text() for r in soup.select('.result__snippet')]

        if not snippets:
            return None

        # Segnali testuali per scala
        full_text = ' '.join(snippets).lower()

        scala = 'Nazionale'  # default
        if any(w in full_text for w in ['locale', 'provinciale', 'comunale', 'città di']):
            scala = 'Locale'
        elif any(w in full_text for w in ['internazionale', 'worldwide', 'global', 'europe']):
            scala = 'Internazionale'

        # Stima importanza da indicatori numerici trovati negli snippet
        importanza = _estimate_importance_from_text(full_text)

        return {
            'scala': scala,
            'importanza': importanza,
            'snippets': snippets[:3],
        }

    except Exception:
        return None

def _estimate_importance_from_text(text: str) -> float:
    """
    Cerca numeri di traffico/tiratura nel testo e li mappa su 0-10.
    Esempi: "2 milioni di lettori", "500mila copie", "1.2M monthly"
    """
    # Cerca pattern tipo "X milioni" o "Xk visitatori"
    milioni = re.findall(r'(\d+(?:[.,]\d+)?)\s*milion', text)
    migliaia = re.findall(r'(\d+(?:[.,]\d+)?)\s*(mila|k)\b', text)

    if milioni:
        n = float(milioni[0].replace(',', '.'))
        # 10M+ → 9-10, 1M → 7, 100k → 5
        return min(10.0, 5.0 + n * 0.8)
    if migliaia:
        n = float(migliaia[0][0].replace(',', '.'))
        return min(7.0, 3.0 + n * 0.01)

    return 5.0  # default medio se non troviamo numeri

#LIVELLO 3
SYSTEM_PROMPT = """Sei un esperto di media italiani. 
Data una testata giornalistica, rispondi SOLO con un JSON valido, 
senza markdown e senza spiegazioni.

Schema obbligatorio:
{
  "scala": "Locale" | "Nazionale" | "Internazionale",
  "importanza": <float 0.0-10.0>,
  "reasoning": "<max 20 parole>"
}

Criteri per importanza:
- 9-10: grandi quotidiani nazionali (Corriere, Repubblica, Sole 24 Ore)
- 7-8:  quotidiani nazionali medi o grandi testate locali regionali
- 5-6:  testate locali con buona diffusione provinciale
- 3-4:  testate locali piccole, blog locali noti
- 1-2:  siti iperlocali, newsletter, agenzie piccole
"""

def llm_classify(testata_name: str, snippets: list[str] | None = None) -> TestataPrediction:
    context = f'Testata: "{testata_name}"'
    if snippets:
        context += f'\n\nContesto trovato online:\n' + '\n'.join(f'- {s}' for s in snippets)

    try:
        response = ollama.chat(
            model='gemma3',  # o 'mistral', 'llama3.2:3b' per leggerezza
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': context},
            ],
            options={'temperature': 0.1},  # output deterministico
        )

        raw = response['message']['content'].strip()
        # Estrai JSON anche se il modello aggiunge testo
        json_match = re.search(r'\{.*}', raw, re.DOTALL)
        if not json_match:
            raise ValueError('No JSON in response')

        data = json.loads(json_match.group())

        return TestataPrediction(
            scala=data['scala'],
            importanza=round(float(data['importanza']), 1),
            confidence=0.8,
            metodo='llm_locale',
        )

    except Exception as e:
        # Fallback di sicurezza
        return TestataPrediction('Nazionale', 5.0, 0.3, f'llm_fallback: {e}')

#DB
def get_or_classify_testata(testata_name: str, db_conn: sqlite3.Connection, save_if_new: bool = True) -> TestataPrediction:
    # 0. Controlla nel DB
    cur = db_conn.execute(
        'SELECT scala, importanza FROM testata WHERE nome = ? COLLATE NOCASE',
        (testata_name,)
    )
    row = cur.fetchone()
    if row:
        return TestataPrediction(row[0], row[1], 1.0, 'database')

    # 1. Euristiche rapide
    result = heuristic_classify(testata_name)

    # 2. Web search
    if result is None or result.confidence < 0.7:
        search_data = search_testata_info(testata_name)
        if search_data:
            snippets = search_data.get('snippets', [])
            # 3. LLM locale (con il contesto degli snippet)
            result = llm_classify(testata_name, snippets)
        else:
            result = llm_classify(testata_name)

    # Salva nel DB con flag "non verificata" per revisione umana
    if save_if_new:
        db_conn.execute('''
                        INSERT OR IGNORE INTO testata
                        (nome, scala, importanza, verificata, metodo_class, created_at)
                        VALUES (?, ?, ?, 0, ?, ?)
                        ''', (
                            testata_name,
                            result.scala,
                            result.importanza,
                            result.metodo,
                            datetime.now().isoformat(),
                        ))
        db_conn.commit()

    return result