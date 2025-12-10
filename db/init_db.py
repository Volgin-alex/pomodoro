import sqlite3
from pathlib import Path

DB_PATH = Path("pomodoro.db")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS Tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    pomodor_cnt  INTEGER
);

CREATE TABLE IF NOT EXISTS Categories (
	id INTEGER PRIMARY KEY,
	name TEXT NOT NULL);
"""

FOREGIN_SQL = """
    ALTER TABLE Tasks ADD COLUMN category_id INTEGER REFERENCES Categories(id);
    """
    
SEED_SQL = """
INSERT OR IGNORE INTO Categories (id, name) VALUES
 (1, 'work'),
 (2, 'education'),
 (3, 'sport');
 
INSERT OR IGNORE INTO Tasks (id, name, pomodor_cnt, category_id) VALUES
 (1, 'Read books', 4, 2),
 (2, 'Create dashboard', 12, 1),
 (3, 'Swimming', 6, 3);


SELECT * FROM Categories ;

SELECT * FROM Tasks;
"""

def main():
    # создаём/открываем базу
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")   # быстрее для записи
        conn.execute("PRAGMA synchronous=NORMAL;") # баланс надёжности/скорости
        conn.executescript(SCHEMA_SQL)
        conn.executescript(FOREGIN_SQL)      
        conn.executescript(SEED_SQL)
        # Пример запроса (джойн двух таблиц)
        rows = conn.execute("""
            SELECT *
            FROM Tasks s
            JOIN Categories c ON s.category_id = c.id
        """).fetchall()

    print(f"База создана: {DB_PATH.resolve()}")
    for r in rows:
        print(r)

if __name__ == "__main__":
    main()