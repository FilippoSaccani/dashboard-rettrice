import sqlite3

def connect_db():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_social():
    conn = connect_db()
    cur = conn.cursor()
    rows = cur.execute("SELECT nome FROM social;").fetchall()
    conn.close()
    return rows

def get_rassegne():
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

def get_dati(nome_social):
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

def insert_dati(dati):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social) VALUES (?, ?, ?, ?, ?)',
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
                        VALUES ("{nome_file}", "{giorno}", {numero_articoli});
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

def delete_rassegna(dati):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f'''
        DELETE * 
        FROM rassegna 
        WHERE nome_file="{dati.nome_file}"
    ''')
    conn.commit()
    conn.close()