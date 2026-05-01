import sqlite3

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
    rows = cur.execute(
        '''
            SELECT *
            FROM rassegna
            ORDER BY giorno;
        '''
    ).fetchall()
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

def insert_dati(dati):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)',
            (dati['giorno'], dati['visualizzazioni'], dati['interazioni'], dati['follower'], dati['social'])
        )
    except sqlite3.IntegrityError as e:
        return False, 'Errore: duplicato'
    except sqlite3.OperationalError as e:
        return False, 'Errore operativo'
    except sqlite3.DatabaseError as e:
        return False, 'Errore nel database'
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
        return False, 'Errore: duplicato'
    except sqlite3.OperationalError as e:
        return False, 'Errore operativo'
    except sqlite3.DatabaseError as e:
        return False, 'Errore nel database'
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
        return False, 'Errore: duplicato'
    except sqlite3.OperationalError as e:
        return False, 'Errore operativo'
    except sqlite3.DatabaseError as e:
        return False, f'Errore nel database: {e}'
    finally:
        conn.commit()
        conn.close()
    return True, ''

def update_articles_number(nome_file, numero_articoli):
    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute(f'''
                        UPDATE rassegna 
                        SET numero_articoli="{numero_articoli}"
                        WHERE nome_file="{nome_file}";
        ''')
    except sqlite3.IntegrityError as e:
        return False, 'Errore: duplicato'
    except sqlite3.OperationalError as e:
        return False, 'Errore operativo'
    except sqlite3.DatabaseError as e:
        return False, 'Errore nel database'
    finally:
        conn.commit()
        conn.close()
    return True, ''

def delete_rassegna(giorno):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(f'''
                DELETE FROM rassegna 
                WHERE giorno="{giorno}"
        ''')
    except sqlite3.OperationalError as e:
        return False, 'Errore operativo'
    except sqlite3.DatabaseError as e:
        return False, 'Errore nel database'
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
    except sqlite3.OperationalError:
        return False, 'Errore operativo'
    except sqlite3.DatabaseError:
        return False, 'Errore nel database'
    finally:
        conn.commit()
        conn.close()

    return True, ''