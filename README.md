# Rassegna Stampa & Social Dashboard

## Descrizione

Dashboard web per la gestione, analisi e consultazione di:

- dati di rassegna stampa
- metriche social (Instagram, Facebook, LinkedIn)
- amministrazione dei dati caricati
- ricerca rassegne per data o parola chiave

L’interfaccia permette la visualizzazione interattiva dei dati tramite grafici e strumenti di filtro dinamici.

---

## Architettura generale

### Frontend
- React 19 (via CDN + Babel standalone)
- React Router 7
- Recharts
- HTML + CSS custom

### Backend
- Flask (API REST)
- SQLite per la persistenza dei dati
- endpoint principali:
  - `/`
  - `/social`
  - `/admin`

---

## Sezioni principali

### Rassegna Stampa (`/`)

#### Contiene tre grafici principali:
- chart 1 → articoli per tema
- chart 2 → articoli per scala
- chart 3 → articoli per testata

Funzionalità:
- toggle dinamico delle linee
- brush per zoom temporale
- doppio click su punto del grafico → apertura rassegna
- filtri per temi / scale / testate

#### Ricerca rassegne:
- ricerca per data
  - `AAAA`
  - `MM/AAAA`
  - `GG/MM/AAAA`
- ricerca testuale
  - ricerca full-text lato server
  - risultati ordinati per rilevanza
  - possibilità di aprire o scaricare le rassegne

### Social Media (`/social`)

#### Dashboard per analisi social:
- Instagram
- Facebook
- LinkedIn

Metriche:
- follower
- interazioni
- visualizzazioni

Funzionalità:
- toggle serie dati
- zoom temporale con brush

### Amministrazione (`/admin`)

Gestione completa dei dati:

#### Social
- inserimento dati giornalieri per piattaforma

#### Rassegne stampa
- upload PDF giornaliero
- estrazione automatica dati

#### Eliminazione dati
- rimozione ultimi record (dati social e rassegne)

#### Controllo testate
- valutazione automatica di importanza e scala delle testate (con ollama)
- modifica scala (Locale, Nazionale, Internazionale) e importanza (0–10)

---

## Funzionalità globali

- refresh manager globale
- polling stato elaborazione rassegne
- layout responsive
- normalizzazione formato date

---

## Installazione e utilizzo

Per sistemi **Ubuntu / Debian**:

Sono richiesti i pacchetti:

- `python3.14` (o equivalente)
- `python3.14-venv` (o equivalente)

### Installazione Ollama

```shell
./scripts/install_ollama.sh
```

### Inizializzazione del server
```shell
./scripts/init.sh
```

### Avvio del server
```shell
./scripts/run.sh <porta>
```
Se non si specifica una porta, il server utilizza la porta 51852.