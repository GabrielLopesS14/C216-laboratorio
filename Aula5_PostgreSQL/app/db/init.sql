CREATE TABLE IF NOT EXISTS contadores (
    curso VARCHAR PRIMARY KEY,
    valor INTEGER
);

CREATE TABLE IF NOT EXISTS alunos (
    id VARCHAR PRIMARY KEY,
    nome VARCHAR,
    email VARCHAR,
    curso VARCHAR,
    matricula INTEGER
);