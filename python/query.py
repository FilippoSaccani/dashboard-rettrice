import functools
from contextlib import contextmanager

from python.newspaper_analysis import *


# --- Connessione ---

@contextmanager
def get_db():
    """
    Context manager per la connessione al DB.
    Gestisce automaticamente commit, rollback e chiusura.
    """
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        raise
    except sqlite3.DatabaseError as e:
        conn.rollback()
        raise
    finally:
        conn.close()


def db_write(func):
    """
    Decorator per le funzioni di scrittura sul DB.
    Gestisce le eccezioni e restituisce (bool, messaggio).
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return True, result
        except sqlite3.IntegrityError:
            return False, 'Duplicato'
        except sqlite3.OperationalError as e:
            return False, f'Errore operativo: {e}'
        except sqlite3.DatabaseError as e:
            return False, f'Errore nel database: {e}'

    return wrapper


# --- SELECT ---

def select_social():
    with get_db() as conn:
        return conn.execute("SELECT nome FROM social").fetchall()


def select_all_temi():
    with get_db() as conn:
        return conn.execute("SELECT nome FROM tema").fetchall()


def select_all_scale():
    with get_db() as conn:
        return conn.execute("SELECT nome FROM scala").fetchall()


def select_all_testate():
    with get_db() as conn:
        return conn.execute(
            "SELECT nome, fk_scala AS scala, importanza FROM testata ORDER BY importanza DESC"
        ).fetchall()


def select_testate_importanti():
    with get_db() as conn:
        return conn.execute('''
                            SELECT DISTINCT t.nome
                            FROM testata t
                                     INNER JOIN articolo a ON a.fk_testata = t.nome
                            ORDER BY t.importanza DESC LIMIT 5
                            ''').fetchall()


def select_dati_social(nome_social):
    with get_db() as conn:
        return conn.execute(
            '''SELECT giorno, visualizzazioni, interazioni, follower
               FROM dati_social
               WHERE fk_social = ?
               ORDER BY giorno''',
            (nome_social,)  # ← parametrizzato, prima era f-string (SQL injection)
        ).fetchall()


def select_all_dati_social():
    with get_db() as conn:
        return conn.execute(
            '''SELECT giorno, visualizzazioni, interazioni, follower, fk_social AS social
               FROM dati_social
               ORDER BY giorno, social'''
        ).fetchall()


def select_latest():
    with get_db() as conn:
        return conn.execute('''
                            SELECT fk_social AS nome, giorno, 'social' AS tipo, data_salvataggio
                            FROM dati_social
                            UNION
                            SELECT nome_file AS nome, giorno, 'rassegna' AS tipo, data_salvataggio
                            FROM rassegna
                            ORDER BY data_salvataggio DESC LIMIT 10
                            ''').fetchall()


def select_all_rassegne():
    with get_db() as conn:
        return conn.execute('''
                            SELECT json_patch(
                                           json_object('nome_file', nome_file, 'giorno', giorno, 'Totale',
                                                       numero_articoli),
                                           json_group_object(tema, n_articoli)
                                   ) AS risultato
                            FROM (SELECT r.nome_file,
                                         r.giorno,
                                         r.numero_articoli,
                                         a.fk_tema AS tema,
                                         COUNT(*)  AS n_articoli
                                  FROM articolo a
                                           INNER JOIN rassegna r ON r.id = a.fk_rassegna
                                  GROUP BY r.nome_file, a.fk_tema)
                            GROUP BY nome_file, giorno, numero_articoli
                            ''').fetchall()


def select_rassegne_per_scala():
    with get_db() as conn:
        return conn.execute('''
                            SELECT json_patch(
                                           json_object('giorno', giorno, 'rassegna', nome_file),
                                           json_group_object(scala,
                                                             json_patch(json_object('totale', totale_scala), temi_json))
                                   ) AS risultato
                            FROM (SELECT nome_file,
                                         giorno,
                                         scala,
                                         SUM(n_articoli)                     AS totale_scala,
                                         json_group_object(tema, n_articoli) AS temi_json
                                  FROM (SELECT r.nome_file,
                                               r.giorno,
                                               t.fk_scala AS scala,
                                               a.fk_tema  AS tema,
                                               COUNT(*)   AS n_articoli
                                        FROM articolo a
                                                 JOIN rassegna r ON r.id = a.fk_rassegna
                                                 JOIN testata t ON t.nome = a.fk_testata
                                        GROUP BY r.nome_file, r.giorno, t.fk_scala, a.fk_tema)
                                  GROUP BY nome_file, giorno, scala)
                            GROUP BY nome_file, giorno
                            ''').fetchall()


def select_rassegne_per_testata():
    with get_db() as conn:
        return conn.execute('''
                            SELECT json_patch(
                                           json_object('giorno', giorno, 'rassegna', nome_file),
                                           json_group_object(testata,
                                                             json_patch(json_object('totale', totale_testata), temi_json))
                                   ) AS risultato
                            FROM (SELECT nome_file,
                                         giorno,
                                         testata,
                                         SUM(n_articoli)                     AS totale_testata,
                                         json_group_object(tema, n_articoli) AS temi_json
                                  FROM (SELECT r.nome_file,
                                               r.giorno,
                                               a.fk_testata AS testata,
                                               a.fk_tema    AS tema,
                                               COUNT(*)     AS n_articoli
                                        FROM articolo a
                                                 JOIN rassegna r ON r.id = a.fk_rassegna
                                        WHERE a.fk_testata IN (SELECT DISTINCT t.nome
                                                               FROM testata t
                                                                        JOIN articolo a ON a.fk_testata = t.nome
                                                               ORDER BY t.importanza DESC LIMIT 5)
                                  GROUP BY r.nome_file, r.giorno, a.fk_testata, a.fk_tema)
                            GROUP BY nome_file, giorno, testata )
                            GROUP BY nome_file, giorno
                            ''').fetchall()


def controllo_testate():
    with get_db() as conn:
        return conn.execute('''
                            SELECT nome, importanza, fk_scala AS scala
                            FROM testata
                            ORDER BY nome COLLATE NOCASE
                            ''').fetchall()


def search_rassegne(query: str, limit: int = 20) -> list[dict]:
    """Cerca nelle rassegne usando FTS5 con snippet evidenziato."""
    if not query.strip():
        return []

    with get_db() as conn:
        rows = conn.execute('''
                            SELECT r.id, r.giorno, r.nome_file, r.numero_articoli, fts.snippet
                            FROM (SELECT rowid,
                                         snippet(rassegne_fts, 0, '<mark>', '</mark>', '...', 20) AS snippet,
                                         rank
                                  FROM rassegne_fts
                                  WHERE rassegne_fts MATCH ?
                                  ORDER BY rank
                                  LIMIT ?) AS fts
                            JOIN rassegna r ON r.id = fts.rowid
                            ''', (query, limit)).fetchall()

    return [dict(row) for row in rows]


# --- INSERT / UPDATE / DELETE ---

@db_write
def insert_dati(dati):
    with get_db() as conn:
        conn.execute(
            'INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)',
            (dati['giorno'], dati['visualizzazioni'], dati['interazioni'], dati['follower'], dati['social'])
        )


@db_write
def insert_tema(nome):
    with get_db() as conn:
        conn.execute('INSERT INTO tema (nome) VALUES (?)', (nome,))


@db_write
def insert_articolo(rassegna, tema, testata):
    with get_db() as conn:
        conn.execute(
            'INSERT INTO articolo (fk_rassegna, fk_tema, fk_testata) VALUES (?, ?, ?)',
            (rassegna, tema, testata)
        )


@db_write
def insert_rassegna(nome_file, giorno, numero_articoli, testo):
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO rassegna (nome_file, giorno, numero_articoli, data_salvataggio, testo) VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?)",
            (nome_file, giorno, numero_articoli, testo)
        )
        rassegna_id = cur.lastrowid
        conn.execute(
            "INSERT OR IGNORE INTO rassegne_fts(rowid, testo, nome_file) SELECT id, testo, nome_file FROM rassegna WHERE id = ?",
            (rassegna_id,)
        )
        return rassegna_id  # il decorator lo restituisce come secondo elemento della tupla


@db_write
def handle_new_testata(testata):
    with get_db() as conn:
        get_or_classify_testata(testata, conn)


@db_write
def conferma_testata(dati):
    with get_db() as conn:
        conn.execute(
            "UPDATE testata SET verificata=1, importanza=?, fk_scala=? WHERE nome=?",
            (dati['importanza'], dati['scala'], dati['nome'])
        )


@db_write
def delete_rassegna(giorno):
    with get_db() as conn:
        rows = conn.execute("SELECT id FROM rassegna WHERE giorno = ?", (giorno,)).fetchall()
        if not rows:
            return
        rassegna_id = rows[0][0]
        conn.execute("DELETE FROM articolo    WHERE fk_rassegna = ?", (rassegna_id,))
        conn.execute("DELETE FROM rassegne_fts WHERE rowid = ?", (rassegna_id,))
        conn.execute("DELETE FROM rassegna    WHERE id = ?", (rassegna_id,))


@db_write
def delete_dato_social(social, giorno):
    with get_db() as conn:
        conn.execute(
            "DELETE FROM dati_social WHERE giorno = ? AND fk_social = ?",
            (giorno, social)
        )
