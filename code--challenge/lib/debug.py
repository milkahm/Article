from lib.db.connection import get_connection
import sqlite3

def debug():
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        print("📄 AUTHORS")
        cursor.execute("SELECT * FROM authors")
        for row in cursor.fetchall():
            print(dict(row))

        print("\n📄 ARTICLES")
        cursor.execute("SELECT * FROM articles")
        for row in cursor.fetchall():
            print(dict(row))

        print("\n📄 MAGAZINES")
        cursor.execute("SELECT * FROM magazines")
        for row in cursor.fetchall():
            print(dict(row))

if __name__ == '__main__':
    debug()
