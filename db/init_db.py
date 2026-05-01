import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.executescript('''
    CREATE TABLE IF NOT EXISTS rassegna (
        nome_file TEXT PRIMARY KEY,
        giorno TEXT UNIQUE NOT NULL,
        numero_articoli INTEGER NOT NULL,
        data_salvataggio TEXT NOT NULL
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
        data_salvataggio TEXT NOT NULL,
        FOREIGN KEY (fk_social) REFERENCES social(nome),
        PRIMARY KEY (giorno, fk_social)
    );
    
    CREATE TABLE IF NOT EXISTS scala (
        nome TEXT PRIMARY KEY
    );
        
    CREATE TABLE IF NOT EXISTS testata(
        nome TEXT PRIMARY KEY,
        scala TEXT NOT NULL,
        FOREIGN KEY (scala) REFERENCES scala(nome)
    );
        
    CREATE TABLE IF NOT EXISTS tema (
        nome TEXT PRIMARY KEY
    );
        
    CREATE TABLE IF NOT EXISTS articolo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fk_tema TEXT NOT NULL,
        fk_rassegna TEXT NOT NULL,
        fk_testata TEXT NOT NULL,
        FOREIGN KEY(fk_tema) REFERENCES tema(nome),
        FOREIGN KEY(fk_rassegna) REFERENCES rassegna(nome_file)
    );
    
    INSERT INTO social VALUES ('Instagram');
    INSERT INTO social VALUES ('Facebook');
    INSERT INTO social VALUES ('Linkedin');
        
    INSERT INTO tema VALUES ('Ricerca e Altri atenei');
    INSERT INTO tema VALUES ('Intelligenza Artificiale e tecnologie');
    INSERT INTO tema VALUES ('Ateneo');
    INSERT INTO tema VALUES ('Politica Locale');
        
    INSERT INTO scala VALUES ('locale');
    INSERT INTO scala VALUES ('nazionale');
    INSERT INTO scala VALUES ('internazionale');
    
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-02-12', 100, 20, 34, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-02-12', 10, 202, 341, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-03-12', 120, 210, 134, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-03-12', 10, 20, 34, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-05-12', 130, 220, 121, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-06-12', 120, 234, 101, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-06-12', 120, 234, 101, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-07-12', 23, 34, 56, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-08-12', 56, 78, 98, 'Linkedin', CURRENT_TIMESTAMP);
''')

conn.commit()
conn.close()
print("Database created successfully")