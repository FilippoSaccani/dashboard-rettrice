import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.executescript('''
    CREATE TABLE IF NOT EXISTS rassegna (
        nome_file TEXT PRIMARY KEY,
        giorno TEXT UNIQUE NOT NULL,
        numero_articoli INTEGER NOT NULL 
    );
    
    CREATE TABLE IF NOT EXISTS social (
        nome TEXT PRIMARY KEY
    );
    
    CREATE TABLE IF NOT EXISTS dati_social (
        giorno TEXT NOT NULL,
        visualizzazioni INTEGER NOT NULL,
        interazioni INTEGER NOT NULL, 
        follower INTEGER NOT NULL,
        fk_social TEXT NOT NULL,
        FOREIGN KEY (fk_social) REFERENCES social(nome),
        PRIMARY KEY (giorno, fk_social)
    );
    
    INSERT INTO social VALUES ('Instagram');
    INSERT INTO social VALUES ('Facebook');
    INSERT INTO social VALUES ('Linkedin');
    
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social) VALUES ('2026-02-12', 100, 20, 34, 'Instagram');
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social) VALUES ('2025-02-12', 10, 202, 341, 'Instagram');
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social) VALUES ('2026-03-12', 120, 210, 134, 'Instagram');
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social) VALUES ('2025-03-12', 10, 20, 34, 'Facebook');
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social) VALUES ('2025-05-12', 130, 220, 121, 'Facebook');
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social) VALUES ('2025-06-12', 120, 234, 101, 'Facebook');
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social) VALUES ('2025-06-12', 120, 234, 101, 'Linkedin');
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social) VALUES ('2025-07-12', 23, 34, 56, 'Linkedin');
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social) VALUES ('2025-08-12', 56, 78, 98, 'Linkedin');

    INSERT INTO rassegna VALUES ('Unimore20260812.txt', '2026-08-12', 42);
    INSERT INTO rassegna VALUES ('Unimore20250812.txt', '2025-08-12', 30);
''')

conn.commit()
conn.close()
print("Database created successfully")