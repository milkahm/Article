from lib.db.connection import get_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name


    @classmethod
    def create(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?) RETURNING id", (name,))
        id = cursor.fetchone()['id']
        conn.commit()
        conn.close()
        return cls(id, name)

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls(row['id'], row['name']) if row else None

    def articles(self):
        from lib.models.article import Article
        return Article.find_by_author_id(self.id)

    def magazines(self):
        from lib.models.magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(**row) for row in rows]

    def add_article(self, magazine, title):
        from lib.models.article import Article
        return Article.create(title, self.id, magazine.id)

    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row['category'] for row in rows]
