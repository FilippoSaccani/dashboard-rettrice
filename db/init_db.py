import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.executescript('''
    CREATE TABLE IF NOT EXISTS rassegna (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_file TEXT UNIQUE NOT NULL,
        giorno TEXT UNIQUE NOT NULL,
        numero_articoli INTEGER NOT NULL,
        data_salvataggio TEXT NOT NULL,
        testo TEXT NOT NULL
    );
    
    CREATE VIRTUAL TABLE IF NOT EXISTS rassegne_fts USING fts5(
        testo,
        nome_file,
        content='rassegna',    -- tabella sorgente (il nome della tua tabella rassegne)
        content_rowid='id'     -- chiave primaria della tabella sorgente
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
        importanza REAL NOT NULL DEFAULT 3,
        verificata INTEGER NOT NULL DEFAULT 1,
        metodo_class TEXT NOT NULL DEFAULT 'manuale',
        confidence REAL NOT NULL DEFAULT 10,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        fk_scala TEXT NOT NULL,
        FOREIGN KEY (fk_scala) REFERENCES scala(nome)
    );
        
    CREATE TABLE IF NOT EXISTS tema (
        nome TEXT PRIMARY KEY
    );
    
    CREATE TABLE IF NOT EXISTS scala(
        nome TEXT PRIMARY KEY
    );
        
    CREATE TABLE IF NOT EXISTS articolo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fk_tema TEXT NOT NULL,
        fk_rassegna TEXT NOT NULL,
        fk_testata TEXT NOT NULL,
        FOREIGN KEY(fk_tema) REFERENCES tema(nome),
        FOREIGN KEY(fk_rassegna) REFERENCES rassegna(id),
        FOREIGN KEY(fk_testata) REFERENCES testata(nome)
    );
    
    INSERT INTO social VALUES ('Instagram');
    INSERT INTO social VALUES ('Facebook');
    INSERT INTO social VALUES ('Linkedin');
        
    INSERT INTO tema VALUES ('Ricerca e Altri atenei');
    INSERT INTO tema VALUES ('Intelligenza Artificiale e tecnologie');
    INSERT INTO tema VALUES ('Ateneo');
    INSERT INTO tema VALUES ('Politica Locale');
    
    INSERT INTO scala VALUES ('Locale');
    INSERT INTO scala VALUES ('Nazionale');
    INSERT INTO scala VALUES ('Internazionale');
        
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-01-03', 980, 112, 15, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-01-10', 1050, 98, 22, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-01-18', 870, 134, 18, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-01-25', 1120, 145, 31, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-02-02', 930, 101, 12, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-02-14', 1480, 267, 54, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-02-22', 1090, 188, 29, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-03-05', 1340, 201, 37, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-03-14', 1210, 176, 25, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-03-22', 1560, 234, 48, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-04-01', 1400, 198, 33, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-04-10', 1670, 245, 61, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-04-19', 1230, 167, 28, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-04-28', 1890, 312, 74, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-05-06', 2010, 289, 82, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-05-15', 1780, 256, 67, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-05-24', 1650, 223, 55, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-06-03', 1920, 301, 89, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-06-12', 2200, 334, 97, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-06-21', 1980, 278, 71, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-07-02', 1540, 189, 43, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-07-11', 1430, 201, 38, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-07-20', 1380, 167, 29, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-07-29', 1290, 145, 21, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-08-07', 1610, 212, 47, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-08-16', 1750, 243, 59, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-08-25', 1830, 267, 63, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-09-04', 2100, 318, 88, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-09-13', 2340, 356, 102, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-09-22', 2190, 334, 94, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-10-01', 2450, 389, 117, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-10-10', 2280, 345, 108, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-10-19', 2560, 401, 124, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-10-28', 2390, 367, 111, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-11-06', 2710, 423, 138, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-11-15', 2890, 456, 152, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-11-24', 3010, 489, 167, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-12-03', 3200, 512, 178, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-12-12', 3450, 567, 195, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-12-21', 3180, 498, 182, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-01-05', 2890, 445, 163, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-01-14', 3100, 478, 171, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-01-23', 3340, 521, 189, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-02-01', 3560, 556, 204, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-02-10', 3210, 489, 187, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-02-19', 3780, 601, 223, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-03-01', 4010, 634, 241, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-03-10', 3890, 612, 229, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-03-19', 4230, 678, 258, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-03-28', 4500, 712, 274, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-04-06', 4120, 656, 247, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-04-15', 4680, 734, 289, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-04-24', 4390, 698, 267, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-05-03', 4820, 756, 301, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-05-12', 5100, 801, 318, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-05-21', 4930, 778, 309, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-05-30', 5280, 834, 334, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-06-08', 5560, 878, 352, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-06-17', 5340, 845, 341, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-06-26', 5780, 912, 378, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-07-05', 5200, 823, 347, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-07-14', 4980, 789, 329, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-07-23', 5100, 812, 338, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-08-01', 5430, 856, 361, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-08-10', 5670, 891, 379, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-08-19', 5890, 934, 398, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-08-28', 6100, 967, 412, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-09-06', 6380, 1012, 434, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-09-15', 6210, 978, 421, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-09-24', 6590, 1045, 449, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-10-03', 6820, 1089, 467, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-10-12', 7010, 1123, 483, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-10-21', 6750, 1078, 461, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-10-30', 7230, 1156, 498, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-11-08', 7450, 1189, 512, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-11-17', 7680, 1234, 531, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-11-26', 7920, 1267, 548, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-12-05', 8100, 1301, 564, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-12-14', 8340, 1345, 581, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-12-23', 8560, 1378, 597, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-01-04', 8120, 1289, 571, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-01-13', 8390, 1334, 589, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-01-22', 8650, 1378, 608, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-01-31', 8900, 1412, 624, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-02-09', 9100, 1456, 641, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-02-18', 9340, 1489, 658, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-02-27', 9560, 1523, 674, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-03-08', 9780, 1567, 691, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-03-17', 10100, 1612, 712, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-03-26', 9890, 1578, 698, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-04-04', 10230, 1634, 723, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-04-13', 10450, 1667, 738, 'Instagram', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-04-22', 10680, 1701, 754, 'Instagram', CURRENT_TIMESTAMP);
    
    -- Facebook
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-01-05', 2100, 89, 8, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-01-14', 1980, 76, 5, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-01-23', 2240, 102, 11, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-02-01', 2050, 91, 7, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-02-14', 2890, 178, 24, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-02-23', 2310, 112, 13, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-03-03', 2560, 134, 17, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-03-12', 2780, 156, 22, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-03-21', 2430, 118, 14, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-03-30', 2910, 167, 26, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-04-08', 3100, 189, 31, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-04-17', 2870, 156, 23, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-04-26', 3240, 198, 34, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-05-05', 3450, 212, 39, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-05-14', 3280, 198, 35, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-05-23', 3560, 223, 42, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-06-01', 3780, 245, 48, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-06-10', 4010, 267, 55, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-06-19', 3890, 251, 51, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-06-28', 4230, 289, 61, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-07-07', 3910, 245, 49, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-07-16', 3760, 231, 44, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-07-25', 3820, 238, 46, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-08-03', 4100, 267, 57, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-08-12', 4340, 289, 64, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-08-21', 4560, 312, 72, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-08-30', 4780, 334, 79, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-09-08', 5010, 356, 87, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-09-17', 5230, 378, 94, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-09-26', 5450, 401, 102, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-10-05', 5670, 423, 109, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-10-14', 5890, 445, 117, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-10-23', 6100, 467, 124, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-11-01', 6340, 489, 132, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-11-10', 6120, 467, 126, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-11-19', 6560, 512, 138, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-11-28', 6780, 534, 145, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-12-07', 7010, 556, 153, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-12-16', 7230, 578, 161, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-12-25', 6890, 534, 148, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-01-03', 7100, 556, 156, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-01-12', 7340, 578, 164, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-01-21', 7560, 601, 172, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-01-30', 7780, 623, 179, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-02-08', 8010, 645, 187, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-02-17', 8230, 667, 195, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-02-26', 8450, 689, 202, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-03-07', 8670, 712, 210, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-03-16', 8890, 734, 218, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-03-25', 9100, 756, 225, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-04-03', 9320, 778, 233, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-04-12', 9540, 801, 241, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-04-21', 9760, 823, 248, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-04-30', 9980, 845, 256, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-05-09', 10200, 867, 264, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-05-18', 10420, 889, 271, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-05-27', 10640, 912, 279, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-06-05', 10860, 934, 287, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-06-14', 11080, 956, 294, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-06-23', 11300, 978, 302, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-07-02', 10890, 934, 287, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-07-11', 10650, 912, 279, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-07-20', 10780, 923, 283, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-07-29', 11100, 956, 294, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-08-07', 11340, 978, 302, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-08-16', 11560, 1001, 309, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-08-25', 11780, 1023, 317, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-09-03', 12010, 1045, 325, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-09-12', 12230, 1067, 332, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-09-21', 12450, 1089, 340, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-09-30', 12670, 1112, 348, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-10-09', 12890, 1134, 355, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-10-18', 13100, 1156, 363, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-10-27', 13320, 1178, 371, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-11-05', 13540, 1201, 378, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-11-14', 13760, 1223, 386, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-11-23', 13980, 1245, 394, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-12-02', 14200, 1267, 401, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-12-11', 14420, 1289, 409, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-12-20', 14100, 1256, 397, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-12-29', 13890, 1234, 389, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-01-07', 14300, 1267, 401, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-01-16', 14560, 1289, 409, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-01-25', 14780, 1312, 417, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-02-03', 15010, 1334, 424, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-02-12', 15230, 1356, 432, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-02-21', 15450, 1378, 440, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-03-02', 15670, 1401, 447, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-03-11', 15890, 1423, 455, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-03-20', 16100, 1445, 463, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-03-29', 16320, 1467, 470, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-04-07', 16540, 1489, 478, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-04-16', 16760, 1512, 486, 'Facebook', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-04-25', 16980, 1534, 493, 'Facebook', CURRENT_TIMESTAMP);
    
    -- LinkedIn
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-01-04', 450, 67, 12, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-01-13', 520, 78, 18, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-01-22', 490, 71, 15, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-01-31', 610, 89, 22, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-02-09', 580, 84, 19, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-02-18', 670, 98, 26, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-02-27', 720, 107, 29, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-03-07', 780, 115, 33, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-03-16', 840, 124, 37, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-03-25', 910, 134, 42, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-04-03', 980, 145, 47, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-04-12', 1050, 156, 52, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-04-21', 1120, 167, 57, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-04-30', 1190, 178, 62, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-05-09', 1260, 189, 67, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-05-18', 1340, 201, 73, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-05-27', 1420, 213, 79, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-06-05', 1510, 227, 85, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-06-14', 1600, 240, 92, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-06-23', 1690, 254, 98, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-07-02', 1560, 234, 89, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-07-11', 1480, 222, 84, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-07-20', 1520, 228, 86, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-07-29', 1610, 242, 93, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-08-07', 1720, 258, 100, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-08-16', 1840, 276, 108, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-08-25', 1960, 294, 116, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-09-03', 2100, 315, 125, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-09-12', 2250, 338, 135, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-09-21', 2400, 360, 145, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-09-30', 2560, 384, 156, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-10-09', 2720, 408, 167, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-10-18', 2890, 434, 179, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-10-27', 3060, 459, 191, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-11-05', 3230, 485, 203, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-11-14', 3410, 512, 216, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-11-23', 3590, 539, 229, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-12-02', 3780, 567, 243, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-12-11', 3960, 594, 256, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-12-20', 3750, 563, 243, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2024-12-29', 3890, 584, 252, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-01-07', 4100, 615, 267, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-01-16', 4320, 648, 283, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-01-25', 4540, 681, 299, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-02-03', 4780, 717, 316, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-02-12', 5010, 752, 333, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-02-21', 5250, 788, 351, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-03-02', 5490, 824, 369, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-03-11', 5740, 861, 388, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-03-20', 5990, 899, 407, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-03-29', 6250, 938, 427, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-04-07', 6510, 977, 447, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-04-16', 6780, 1017, 468, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-04-25', 7050, 1058, 489, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-05-04', 7330, 1100, 511, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-05-13', 7610, 1142, 533, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-05-22', 7890, 1184, 555, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-05-31', 8180, 1227, 578, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-06-09', 8470, 1271, 601, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-06-18', 8760, 1314, 624, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-06-27', 9060, 1359, 648, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-07-06', 8780, 1317, 628, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-07-15', 8560, 1284, 613, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-07-24', 8690, 1304, 621, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-08-02', 9010, 1352, 645, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-08-11', 9340, 1401, 670, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-08-20', 9670, 1451, 695, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-08-29', 10010, 1502, 721, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-09-07', 10360, 1554, 748, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-09-16', 10710, 1607, 775, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-09-25', 11070, 1661, 803, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-10-04', 11430, 1715, 831, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-10-13', 11800, 1770, 860, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-10-22', 12170, 1826, 889, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-10-31', 12550, 1883, 919, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-11-09', 12930, 1940, 949, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-11-18', 13320, 1998, 980, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-11-27', 13710, 2057, 1011, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-12-06', 14110, 2117, 1043, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-12-15', 14510, 2177, 1075, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2025-12-24', 13980, 2097, 1038, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-01-02', 14320, 2148, 1064, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-01-11', 14760, 2214, 1097, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-01-20', 15200, 2280, 1130, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-01-29', 15650, 2348, 1164, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-02-07', 16100, 2415, 1198, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-02-16', 16560, 2484, 1233, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-02-25', 17020, 2553, 1268, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-03-06', 17490, 2624, 1304, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-03-15', 17960, 2694, 1340, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-03-24', 18440, 2766, 1377, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-04-02', 18920, 2838, 1414, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-04-11', 19410, 2912, 1452, 'Linkedin', CURRENT_TIMESTAMP);
    INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social, data_salvataggio) VALUES ('2026-04-20', 19900, 2985, 1490, 'Linkedin', CURRENT_TIMESTAMP);
    
    INSERT OR IGNORE INTO testata (nome, fk_scala, importanza) VALUES 
    
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