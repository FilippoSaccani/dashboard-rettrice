CREATE DATABASE IF NOT EXISTS rettrice;
USE rettrice;

CREATE TABLE rassegna (
    nome_file VARCHAR(100) PRIMARY KEY,
    giorno DATE UNIQUE NOT NULL,
    numero_articoli INT NOT NULL 
)

CREATE TABLE social (
    nome VARCHAR(100) PRIMARY KEY
)

CREATE TABLE dati_social (
    id INT AUTO_INCREMENT PRIMARY KEY,
    giorno DATE NOT NULL,
    visualizzazioni INT NOT NULL,
    interazioni INT NOT NULL, 
    follower INT NOT NULL,
    fk_social VARCHAR(100) NOT NULL,
    FOREIGN KEY (fk_social) REFERENCES social(nome)
)

INSERT INTO social VALUES ('Instagram');
INSERT INTO social VALUES ('Facebook');
INSERT INTO social VALUES ('Linkedin');

SELECT *
FROM dati_social D
JOIN social S ON S.nome=D.fk_social
WHERE S.nome=:nome_social;

SELECT *
FROM rassegna;

INSERT INTO dati_social (giorno, visualizzazioni, interazioni, follower, fk_social) VALUES (:giorno, :visualizzazioni, :interazioni, :follower, :fk_social);

INSERT INTO rassegna VALUES (:nome_file, :giorno, :numero_articoli);

DELETE FROM rassegna WHERE nome_file=:nome_file;