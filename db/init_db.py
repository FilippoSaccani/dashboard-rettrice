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

    CREATE TABLE IF NOT EXISTS testata(
        nome TEXT PRIMARY KEY,
        scala TEXT CHECK (scala IN ('Locale', 'Nazionale', 'Internazionale')) NOT NULL, 
        importanza INTEGER DEFAULT 3
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
        FOREIGN KEY(fk_rassegna) REFERENCES rassegna(nome_file),
        FOREIGN KEY(fk_testata) REFERENCES testata(nome)
    );
    
    INSERT INTO social VALUES ('Instagram');
    INSERT INTO social VALUES ('Facebook');
    INSERT INTO social VALUES ('Linkedin');
        
    INSERT INTO tema VALUES ('Ricerca e Altri atenei');
    INSERT INTO tema VALUES ('Intelligenza Artificiale e tecnologie');
    INSERT INTO tema VALUES ('Ateneo');
    INSERT INTO tema VALUES ('Politica Locale');
        
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-02-12', 100, 20, 34, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-02-12', 10, 202, 341, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-03-12', 120, 210, 134, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-03-12', 10, 20, 34, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-05-12', 130, 220, 121, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-06-12', 120, 234, 101, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-06-12', 120, 234, 101, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-07-12', 23, 34, 56, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-08-12', 56, 78, 98, 'Linkedin', CURRENT_TIMESTAMP);
    
    INSERT OR IGNORE INTO testata (nome, scala, importanza) VALUES 
    
    -- --- TESTATE DALLA TUA RASSEGNA STAMPA ---
    ('Avvenire', 'Nazionale', 7), -- Rilevata nel documento (Pag. 9)
    
    -- --- FOCUS EMILIA-ROMAGNA: MODENA E PROVINCIA ---
    ('Gazzetta di Modena', 'Locale', 6),
    ('Il Resto del Carlino - Modena', 'Locale', 6),
    ('Il Resto del Carlino Modena', 'Locale', 6),
    ('ModenaToday', 'Locale', 5),
    ('Modena2000', 'Locale', 4),
    ('TRC Modena', 'Locale', 5),
    ('Sul Panaro', 'Locale', 3),
    ('Voce di Carpi', 'Locale', 4),
    ('Notizie di Carpi', 'Locale', 4),
    ('Sassuolo2000', 'Locale', 4),
    ('Prima Pagina Modena', 'Locale', 4),
    ('Lapam.mo.it', 'Locale', 2),
    ('Comune di Modena', 'Locale', 2),
    ('Unimore.it', 'Locale', 3), -- Spesso citato in rassegne universitarie
    
    -- --- REGGIO EMILIA, PARMA, PIACENZA ---
    ('Gazzetta di Reggio', 'Locale', 5),
    ('Il Resto del Carlino - Reggio', 'Locale', 5),
    ('ReggioSera', 'Locale', 4),
    ('ReggioOnline', 'Locale', 4),
    ('Gazzetta di Parma', 'Locale', 6),
    ('ParmaToday', 'Locale', 5),
    ('ParmaDaily', 'Locale', 4),
    ('Libertà', 'Locale', 6), -- Piacenza
    ('PiacenzaSera', 'Locale', 4),
    ('IlPiacenza', 'Locale', 4),
    
    -- --- BOLOGNA, FERRARA E ROMAGNA ---
    ('Il Resto del Carlino - Bologna', 'Locale', 7),
    ('Corriere di Bologna', 'Locale', 6),
    ('BolognaToday', 'Locale', 5),
    ('Bologna In Diretta', 'Locale', 4),
    ('La Nuova Ferrara', 'Locale', 5),
    ('Il Resto del Carlino - Ferrara', 'Locale', 5),
    ('Estense.com', 'Locale', 4),
    ('Corriere Romagna', 'Locale', 6),
    ('Corriere Romagna - Forlì-Cesena', 'Locale', 5),
    ('Corriere Romagna - Ravenna', 'Locale', 5),
    ('Corriere Romagna - Rimini', 'Locale', 5),
    ('Il Resto del Carlino - Rimini', 'Locale', 5),
    ('RavennaToday', 'Locale', 4),
    ('RiminiToday', 'Locale', 4),
    
    -- --- GRANDI NAZIONALI (ALTO TRAFFICO) ---
    ('Corriere della Sera', 'Nazionale', 10),
    ('La Repubblica', 'Nazionale', 10),
    ('Il Sole 24 Ore', 'Nazionale', 10),
    ('La Stampa', 'Nazionale', 9),
    ('Il Messaggero', 'Nazionale', 8),
    ('Il Fatto Quotidiano', 'Nazionale', 8),
    ('QN', 'Nazionale', 8), -- Quotidiano Nazionale (Carlino/Nazione/Giorno)
    ('Il Giornale', 'Nazionale', 7),
    ('Libero', 'Nazionale', 7),
    ('La Verità', 'Nazionale', 7),
    ('Il Foglio', 'Nazionale', 6),
    ('Il Manifesto', 'Nazionale', 5),
    ('Italia Oggi', 'Nazionale', 7),
    ('Milano Finanza', 'Nazionale', 7),
    ('L''Unità', 'Nazionale', 5),
    ('Il Riformista', 'Nazionale', 5),
    ('Il Dubbio', 'Nazionale', 5),
    
    -- --- AGENZIE DI STAMPA E NEWS ONLINE (CRITICHE PER RASSEGNE) ---
    ('ANSA', 'Nazionale', 10),
    ('Adnkronos', 'Nazionale', 9),
    ('AGI', 'Nazionale', 9),
    ('Dire', 'Nazionale', 8), -- Molto forte in Emilia-Romagna
    ('Radiocor', 'Nazionale', 8),
    ('Askanews', 'Nazionale', 7),
    ('TGCOM24', 'Nazionale', 9),
    ('Sky TG24', 'Nazionale', 9),
    ('Fanpage.it', 'Nazionale', 9),
    ('Open', 'Nazionale', 7),
    
    -- --- INTERNAZIONALI ---
    ('The New York Times', 'Internazionale', 10),
    ('The Guardian', 'Internazionale', 9),
    ('Le Monde', 'Internazionale', 9),
    ('El País', 'Internazionale', 8),
    ('Financial Times', 'Internazionale', 9),
    ('The Wall Street Journal', 'Internazionale', 9),
    ('BBC News', 'Internazionale', 10),
    ('Reuters', 'Internazionale', 10),
    ('Bloomberg', 'Internazionale', 10),
    ('CNN', 'Internazionale', 10),
    ('Der Spiegel', 'Internazionale', 8),
    ('Le Figaro', 'Internazionale', 8),      
    ('Avvenire','Nazionale',7),
    ('Corriere della Sera','Nazionale',10),
    ('Il Fatto Quotidiano','Nazionale',8),
    ('Il Resto del Carlino (ed. Reggio Emilia)','Locale',5),
    ('Il Resto del Carlino (ed. Modena)','Locale',6),
    ('Il Sole 24 Ore','Nazionale',10),
    ('La Stampa','Nazionale',9),
    ('24Emilia','Locale',4),
    ('Agenparl','Nazionale',6),
    ('Bologna2000','Locale',4),
    ('Corriere di Bologna','Locale',6),
    ('Corriere Romagna','Locale',6),
    ('Gazzetta di Modena','Locale',6),
    ('Gazzetta di Reggio','Locale',5),
    ('ilrestodelcarlino.it','Nazionale',8),
    ('Modena2000','Locale',4),
    ('Msn','Internazionale',9),
    ('Reggio2000','Locale',4),
    ('Reggionline','Locale',5)
''')

conn.commit()
conn.close()
print("Database created successfully")