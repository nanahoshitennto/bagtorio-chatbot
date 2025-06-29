DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS options;

CREATE TABLE questions (
    id TEXT PRIMARY KEY,
    text TEXT NOT NULL
);

CREATE TABLE options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT NOT NULL,
    label TEXT NOT NULL,
    next_id TEXT,
    FOREIGN KEY (question_id) REFERENCES questions (id)
);
