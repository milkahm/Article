from lib.db.connection import get_connection
from typing import Optional, List, Dict
import sqlite3

class Author:
    def __init__(self, name: str, id: Optional[int] = None):
        self.id = id
        self.name = name

    def save(self) -> None:
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
                self.id = cursor.lastrowid
            else:
                cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
            conn.commit()

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Author":
        return cls(
            id=row["id"],
            name=row["name"]
        )

    @classmethod
    def find_by_id(cls, author_id: int) -> Optional["Author"]:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM authors WHERE id = ?", (author_id,))
            row = cursor.fetchone()
        if row:
            return cls.from_row(row)
        return None

    @classmethod
    def find_by_name(cls, name: str) -> Optional["Author"]:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
            row = cursor.fetchone()
        if row:
            return cls.from_row(row)
        return None

    @classmethod
    def top_author(cls) -> Optional["Author"]:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT authors.*, COUNT(articles.id) as article_count
                FROM authors
                JOIN articles ON authors.id = articles.author_id
                GROUP BY authors.id
                ORDER BY article_count DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
        if row:
            return cls.from_row(row)
        return None

    def articles(self) -> List:
        from lib.models.article import Article  # Lazy import here
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
            rows = cursor.fetchall()
        return [Article.from_row(row) for row in rows]

    def magazines(self) -> List:
        from lib.models.magazine import Magazine  # Lazy import here
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT m.* FROM magazines m
                JOIN articles a ON a.magazine_id = m.id
                WHERE a.author_id = ?
            """, (self.id,))
            rows = cursor.fetchall()
        return [Magazine.from_row(row) for row in rows]

    def add_article(self, magazine, title: str):
        from lib.models.article import Article  # Lazy import here
        article = Article(title=title, author_id=self.id, magazine_id=magazine.id)
        article.save()
        return article

    def topic_areas(self) -> List[str]:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT m.category FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
            """, (self.id,))
            rows = cursor.fetchall()
        return [row["category"] for row in rows]
