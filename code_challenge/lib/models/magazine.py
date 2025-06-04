from typing import List, Dict, Optional
import sqlite3
from code_challenge.lib.db.connection import get_connection  # Adjust the import based on your project structure
class Magazine:
    def __init__(self, name: str, category: str, id: Optional[int] = None):
        self.id = id
        self.name = name
        self.category = category

    def save(self) -> None:
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute(
                    "INSERT INTO magazines (name, category) VALUES (?, ?)", 
                    (self.name, self.category)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE magazines SET name = ?, category = ? WHERE id = ?", 
                    (self.name, self.category, self.id)
                )
            conn.commit()

    def articles(self) -> List[Dict]:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
            results = cursor.fetchall()
        return [dict(row) for row in results]

    def contributors(self) -> List:
        from lib.models.author import Author  # Lazy import here
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT a.* FROM authors a
                JOIN articles ar ON ar.author_id = a.id
                WHERE ar.magazine_id = ?
            """, (self.id,))
            rows = cursor.fetchall()
        return [Author.from_row(row) for row in rows]

    def article_titles(self) -> List[str]:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
            results = cursor.fetchall()
        return [row['title'] for row in results]

    def contributing_authors(self) -> List:
        from lib.models.author import Author  # Lazy import here
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.*, COUNT(ar.id) as article_count FROM authors a
                JOIN articles ar ON a.id = ar.author_id
                WHERE ar.magazine_id = ?
                GROUP BY a.id
                HAVING COUNT(ar.id) > 2
            """, (self.id,))
            rows = cursor.fetchall()
        return [Author.from_row(row) for row in rows]

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Magazine":
        return cls(
            id=row["id"],
            name=row["name"],
            category=row["category"]
        )

    # New classmethods added below:

    @classmethod
    def find_by_name(cls, name: str) -> Optional["Magazine"]:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
            row = cursor.fetchone()
        if row:
            return cls.from_row(row)
        return None

    @classmethod
    def find_by_category(cls, category: str) -> List["Magazine"]:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
            rows = cursor.fetchall()
        return [cls.from_row(row) for row in rows]

    @classmethod
    def with_multiple_authors(cls) -> List["Magazine"]:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.* FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                GROUP BY m.id
                HAVING COUNT(DISTINCT a.author_id) > 1
            """)
            rows = cursor.fetchall()
        return [cls.from_row(row) for row in rows]

    @classmethod
    def article_counts(cls) -> List[Dict]:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.id, m.name, m.category, COUNT(a.id) AS article_count
                FROM magazines m
                LEFT JOIN articles a ON m.id = a.magazine_id
                GROUP BY m.id
            """)
            rows = cursor.fetchall()
        return [dict(row) for row in rows]
