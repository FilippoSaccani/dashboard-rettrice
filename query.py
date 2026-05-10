from newspaper_analysis import *

def connect_db():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def select_social():
    conn = connect_db()
    cur = conn.cursor()
    rows = cur.execute("SELECT nome FROM social;").fetchall()
    conn.close()
    return rows

def select_all_rassegne():
    conn = connect_db()
    cur = conn.cursor()
    rows = cur.execute('''
            SELECT 
                json_patch(
                    json_object(
                            'nome_file', nome_file,
                            'giorno', giorno,
                            'Totale', numero_articoli
                    ),
                    json_group_object(tema, n_articoli)
                ) AS risultato
            FROM (
                SELECT 
                    rassegna.nome_file,
                    rassegna.giorno,
                    rassegna.numero_articoli,
                    articolo.fk_tema AS tema,
                    COUNT(*) AS n_articoli
                FROM articolo
                INNER JOIN rassegna 
                    ON rassegna.id = articolo.fk_rassegna
                GROUP BY rassegna.nome_file, articolo.fk_tema
            ) t
            GROUP BY nome_file, giorno, numero_articoli;
    ''').fetchall()
    conn.close()
    return rows

def select_rassegne_per_scala():
    conn = connect_db()
    cur = conn.cursor()
    rows = cur.execute('''
        SELECT 
            json_patch(
                json_object(
                    'giorno', giorno,
                    'rassegna', nome_file
                ),
                json_group_object(
                    scala,
                    json_patch(
                        json_object('totale', totale_scala),
                        temi_json
                    )
                )
            ) AS risultato
        FROM (
            SELECT 
                nome_file,
                giorno,
                scala,
                SUM(n_articoli) AS totale_scala,
                json_group_object(tema, n_articoli) AS temi_json
            FROM (
                SELECT 
                    r.nome_file,
                    r.giorno,
                    t.fk_scala AS scala,
                    a.fk_tema AS tema,
                    COUNT(*) AS n_articoli
                FROM articolo a
                JOIN rassegna r 
                    ON r.id = a.fk_rassegna
                JOIN testata t 
                    ON t.nome = a.fk_testata
                GROUP BY 
                    r.nome_file,
                    r.giorno,
                    t.fk_scala,
                    a.fk_tema
            )
            GROUP BY 
                nome_file,
                giorno,
                scala
        )
        GROUP BY 
            nome_file,
            giorno;
    ''').fetchall()
    conn.close()
    return rows

def select_rassegne_per_testata():
    conn = connect_db()
    cur = conn.cursor()
    rows = cur.execute('''
        SELECT 
            json_patch(
                json_object(
                    'giorno', giorno,
                    'rassegna', nome_file
                ),
                json_group_object(
                    testata,
                    json_patch(
                        json_object('totale', totale_testata),
                        temi_json
                    )
                )
            ) AS risultato
        FROM (
            SELECT 
                nome_file,
                giorno,
                testata,
                SUM(n_articoli) AS totale_testata,
                json_group_object(tema, n_articoli) AS temi_json
            FROM (
                SELECT 
                    r.nome_file,
                    r.giorno,
                    a.fk_testata AS testata,
                    a.fk_tema AS tema,
                    COUNT(*) AS n_articoli
                FROM articolo a
                JOIN rassegna r 
                    ON r.id = a.fk_rassegna
                WHERE a.fk_testata IN (
                    SELECT DISTINCT t.nome
                    FROM testata t
                    JOIN articolo a ON a.fk_testata = t.nome
                    ORDER BY t.importanza DESC
                    LIMIT 5
                )
                GROUP BY 
                    r.nome_file,
                    r.giorno,
                    a.fk_testata,
                    a.fk_tema
            )
            GROUP BY 
                nome_file,
                giorno,
                testata
        )
        GROUP BY 
            nome_file,
            giorno;
    ''').fetchall()
    conn.close()
    return rows

def select_testate_importanti():
    conn = connect_db()
    cur = conn.cursor()
    rows = cur.execute('''
        SELECT DISTINCT t.nome
        FROM testata t
        INNER JOIN articolo a ON a.fk_testata = t.nome
        ORDER BY t.importanza DESC
        LIMIT 5
    ''').fetchall()
    conn.close()
    return rows

def select_dati_social(nome_social):
    conn = connect_db()
    cur = conn.cursor()
    rows = cur.execute(
        f'''
            SELECT giorno, visualizzazioni, interazioni, follower
            FROM dati_social
            WHERE fk_social="{nome_social}"
            ORDER BY giorno;
        '''
    ).fetchall()
    conn.close()
    return rows

def select_all_dati_social():
    conn = connect_db()
    cur = conn.cursor()
    rows = cur.execute(
        f'''
            SELECT giorno, visualizzazioni, interazioni, follower, fk_social as social
            FROM dati_social
            ORDER BY giorno, social;
        '''
    ).fetchall()
    conn.close()
    return rows

def select_latest():
    conn = connect_db()
    cur = conn.cursor()
    rows = cur.execute(
        '''
        SELECT fk_social as nome, giorno, 'social' as tipo, data_salvataggio
        FROM dati_social
        UNION
        SELECT nome_file as nome, giorno, 'rassegna' as tipo, data_salvataggio
        FROM rassegna
        ORDER BY data_salvataggio DESC
        LIMIT 10;
        '''
    ).fetchall()
    conn.close()
    return rows

def select_all_temi():
    conn = connect_db()
    cur = conn.cursor()
    rows = cur.execute(
        '''
        SELECT nome
        FROM tema
        '''
    ).fetchall()
    conn.close()
    return rows

def select_all_scale():
    conn = connect_db()
    cur = conn.cursor()
    rows = cur.execute(
        '''
        SELECT nome
        FROM scala
        '''
    ).fetchall()
    conn.close()
    return rows

def select_all_testate():
    conn = connect_db()
    cur = conn.cursor()
    rows = cur.execute(
        '''
        SELECT nome, fk_scala AS scala, importanza
        FROM testata
        ORDER BY importanza DESC ;
        '''
    ).fetchall()
    conn.close()
    return rows

def insert_dati(dati):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)',
            (dati['giorno'], dati['visualizzazioni'], dati['interazioni'], dati['follower'], dati['social'])
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        return False, 'Questo dato è già stato inserito'
    except sqlite3.OperationalError as e:
        conn.rollback()
        return False, f'Errore operativo: {e}'
    except sqlite3.DatabaseError as e:
        conn.rollback()
        return False, f'Errore nel database: {e}'
    finally:
        conn.close()
    return True, ''

def insert_rassegna(nome_file, giorno, numero_articoli, testo):
    conn = connect_db()

    try:
        cur = conn.execute(
            "INSERT INTO rassegna (nome_file, giorno, numero_articoli, data_salvataggio, testo) VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?)",
            (nome_file, giorno, numero_articoli, testo)
        )

        rassegna_id = cur.lastrowid

        conn.execute(
            "INSERT OR IGNORE INTO rassegne_fts(rowid, testo, nome_file) "
            "SELECT id, testo, nome_file FROM rassegna WHERE id = ?",
            (rassegna_id,)
        )

        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        return False, 'Questa rassegna è già stata inserita'
    except sqlite3.OperationalError as e:
        conn.rollback()
        return False, f'Errore operativo: {e}'
    except sqlite3.DatabaseError as e:
        conn.rollback()
        return False, f'Errore nel database: {e}'
    finally:
        conn.close()
    return True, cur.lastrowid

def handle_new_testata(testata):
    print("DEBUG: handling new newspaper")
    conn = connect_db()
    get_or_classify_testata(testata, conn)
    conn.commit()
    conn.close()
    return True, ''

def insert_tema(nome):
    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute(
            'INSERT INTO tema (nome) VALUES (?)',
            (nome,)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        return False, 'Tema duplicato'
    except sqlite3.OperationalError as e:
        conn.rollback()
        return False, f'Errore operativo: {e}'
    except sqlite3.DatabaseError as e:
        conn.rollback()
        return False, f'Errore nel database: {e}'
    finally:
        conn.close()
    return True, ''

def insert_articolo(rassegna, tema, testata):
    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute(
            'INSERT INTO articolo (fk_rassegna, fk_tema, fk_testata) VALUES (?, ?, ?)',
            (rassegna, tema, testata)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        return False, 'Articolo duplicato'
    except sqlite3.OperationalError as e:
        conn.rollback()
        return False, f'Errore operativo: {e}'
    except sqlite3.DatabaseError as e:
        conn.rollback()
        return False, f'Errore nel database: {e}'
    finally:
        conn.close()
    return True, ''

def delete_rassegna(giorno):
    conn = connect_db()
    try:
        conn.execute(
            "DELETE FROM articolo WHERE fk_rassegna = (SELECT rassegna.id FROM rassegna WHERE giorno=?);",
            (giorno,)
        )

        rows = conn.execute(
            "SELECT id FROM rassegna WHERE giorno = (?);",
            (giorno,)
        ).fetchall()

        rassegna_id = rows[0][0]

        conn.execute(
            "DELETE FROM rassegne_fts WHERE rowid = ?",
            (rassegna_id,)
        )

        conn.execute(
            "DELETE FROM rassegna WHERE giorno = (?);",
            (giorno,)
        )

        conn.commit()
    except sqlite3.OperationalError as e:
        conn.rollback()
        return False, f'Errore operativo: {e}'
    except sqlite3.DatabaseError as e:
        conn.rollback()
        return False, f'Errore nel database: {e}'
    finally:
        conn.close()

    return True, ''

def delete_dato_social(social, giorno):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM dati_social WHERE giorno=? AND fk_social=?",
            (giorno, social)
        )
        conn.commit()
    except sqlite3.OperationalError as e:
        conn.rollback()
        return False, f'Errore operativo: {e}'
    except sqlite3.DatabaseError as e:
        conn.rollback()
        return False, f'Errore nel database: {e}'
    finally:
        conn.close()

    return True, ''

def search_rassegne(query: str, limit: int = 20) -> list[dict]:
    conn = connect_db()
    """
    Cerca nelle rassegne usando FTS5.
    Restituisce i risultati con uno snippet evidenziato.
    """
    if not query.strip():
        return []

    # snippet() è una funzione built-in di FTS5:
    # evidenzia il match con <mark> e ritorna ~20 token di contesto
    rows = conn.execute("""
    SELECT r.id,
           r.giorno,
           r.nome_file,
           r.numero_articoli,
           fts.snippet
    FROM (SELECT rowid, snippet(rassegne_fts, 0, '<mark>', '</mark>', '...', 20) AS snippet, rank
          FROM rassegne_fts
          WHERE rassegne_fts MATCH ?
          ORDER BY rank
          LIMIT ?) AS fts
    JOIN rassegna r ON r.id = fts.rowid
    """, (query, limit)).fetchall()

    return [
        {
            'id':              row['id'],
            'giorno':          row['giorno'],
            'nome_file':       row['nome_file'],
            'numero_articoli': row['numero_articoli'],
            'snippet':         row['snippet'],
        }
        for row in rows
    ]

def controllo_testate():
    conn = connect_db()
    cur = conn.cursor()
    rows = cur.execute('''
        SELECT nome, importanza, fk_scala AS scala
        FROM testata
        WHERE verificata=0
    ''').fetchall()
    conn.close()
    return rows

def conferma_testata(dati):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE testata SET verificata=1, importanza=?, fk_scala=? WHERE nome=?",
            (dati['importanza'], dati['scala'], dati['nome'])
        )
        conn.commit()
    except sqlite3.OperationalError as e:
        conn.rollback()
        return False, f'Errore operativo: {e}'
    except sqlite3.DatabaseError as e:
        conn.rollback()
        return False, f'Errore nel database: {e}'
    finally:
        conn.close()

    return True, ''