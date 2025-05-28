# scripts/setup_db.py

import sqlite3

def setup_database():
    conn = sqlite3.connect("articles.db")
    with open("lib/db/schema.sql") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("✅ Database setup complete.")

if __name__ == "__main__":
    setup_database()
