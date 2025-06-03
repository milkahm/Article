from lib.db.connection import get_connection
from typing import Optional, List
import sqlite3

class Article:
    def __init__(self, title: str, author_id: int, magazine_id: int, id: Optional[int] = None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def save(self) -> None:
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute(
                    "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                    (self.title, self.author_id, self.magazine_id)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                    (self.title, self.author_id, self.magazine_id, self.id)
                )
            conn.commit()

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Article":
        return cls(
            id=row["id"],
            title=row["title"],
            author_id=row["author_id"],
            magazine_id=row["magazine_id"]
        )

    @classmethod
    def find_by_id(cls, article_id: int) -> Optional["Article"]:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
            row = cursor.fetchone()
        if row:
            return cls.from_row(row)
        return None

    @classmethod
    def find_by_title(cls, title: str) -> Optional["Article"]:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
            row = cursor.fetchone()
        if row:
            return cls.from_row(row)
        return None

    @classmethod
    def all(cls) -> List["Article"]:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles")
            rows = cursor.fetchall()
        return [cls.from_row(row) for row in rows]
