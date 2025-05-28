from lib.db.connection import get_connection

class Article:
    def __init__(self, id, title, author_id, magazine_id):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    @classmethod
    def create(cls, title, author_id, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO articles (title, author_id, magazine_id)
            VALUES (?, ?, ?) RETURNING id
        """, (title, author_id, magazine_id))
        id = cursor.fetchone()['id']
        conn.commit()
        conn.close()
        return cls(id, title, author_id, magazine_id)

    @classmethod
    def find_by_author_id(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (author_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(**row) for row in rows]

    @classmethod
    def find_by_magazine_id(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(**row) for row in rows]
