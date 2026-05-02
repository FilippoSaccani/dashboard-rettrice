from search_functions import *

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
                            'Tutti', numero_articoli
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
                    ON rassegna.nome_file = articolo.fk_rassegna
                GROUP BY rassegna.nome_file, articolo.fk_tema
            ) t
            GROUP BY nome_file, giorno, numero_articoli;
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

def select_all_testate():
    conn = connect_db()
    cur = conn.cursor()
    rows = cur.execute(
        '''
        SELECT nome, scala, importanza
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
    except sqlite3.IntegrityError as e:
        return False, 'Questo dato è già stato inserito'
    except sqlite3.OperationalError as e:
        return False, f'Errore operativo: {e}'
    except sqlite3.DatabaseError as e:
        return False, f'Errore nel database: {e}'
    finally:
        conn.commit()
        conn.close()
    return True, ''

def insert_rassegna(nome_file, giorno, numero_articoli):
    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute(f'''
                        INSERT INTO rassegna 
                        VALUES ("{nome_file}", "{giorno}", {numero_articoli}, CURRENT_TIMESTAMP);
        ''')
    except sqlite3.IntegrityError as e:
        return False, 'Questa rassegna è già stata inserita'
    except sqlite3.OperationalError as e:
        return False, f'Errore operativo: {e}'
    except sqlite3.DatabaseError as e:
        return False, f'Errore nel database: {e}'
    finally:
        conn.commit()
        conn.close()
    return True, ''

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
    except sqlite3.IntegrityError as e:
        return False, 'Tema duplicato'
    except sqlite3.OperationalError as e:
        return False, f'Errore operativo: {e}'
    except sqlite3.DatabaseError as e:
        return False, f'Errore nel database: {e}'
    finally:
        conn.commit()
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
    except sqlite3.IntegrityError as e:
        return False, 'Articolo duplicato'
    except sqlite3.OperationalError as e:
        return False, f'Errore operativo: {e}'
    except sqlite3.DatabaseError as e:
        return False, f'Errore nel database: {e}'
    finally:
        conn.commit()
        conn.close()
    return True, ''

def delete_rassegna(giorno):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute('''
                    DELETE FROM articolo WHERE fk_rassegna = 
                        (SELECT nome_file FROM rassegna WHERE giorno=?);
            ''',
            (giorno,)
        )

        cur.execute(
                    "DELETE FROM rassegna WHERE giorno = (?);",
                    (giorno,)
        )
    except sqlite3.OperationalError as e:
        return False, f'Errore operativo: {e}'
    except sqlite3.DatabaseError as e:
        return False, f'Errore nel database: {e}'
    finally:
        conn.commit()
        conn.close()

    return True, ''

def delete_dato_social(social, giorno):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(f'''
                    DELETE FROM dati_social 
                    WHERE giorno="{giorno}" AND fk_social="{social}"
            ''')
    except sqlite3.OperationalError as e:
        return False, f'Errore operativo: {e}'
    except sqlite3.DatabaseError as e:
        return False, f'Errore nel database: {e}'
    finally:
        conn.commit()
        conn.close()

    return True, ''