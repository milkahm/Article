# lib/db/seed.py
import os
import sqlite3

print("Database file absolute path:", os.path.abspath("articles.db"))

def seed_data():
    conn = sqlite3.connect("articles.db")
    cursor = conn.cursor()

    # Clear existing data
    cursor.executescript("""
        DELETE FROM articles;
        DELETE FROM authors;
        DELETE FROM magazines;
    """)

    # Insert authors
    authors = [
        ("Alice Walker",),
        ("George Orwell",),
        ("Toni Morrison",)
    ]
    cursor.executemany("INSERT INTO authors (name) VALUES (?)", authors)

    # Insert magazines
    magazines = [
        ("Tech Monthly", "Technology"),
        ("Literary Digest", "Literature"),
        ("Science Weekly", "Science")
    ]
    cursor.executemany("INSERT INTO magazines (name, category) VALUES (?, ?)", magazines)

    # Insert articles
    articles = [
        ("The Future of AI", 1, 1),  # Alice in Tech Monthly
        ("1984 Revisited", 2, 2),   # George in Literary Digest
        ("Quantum Thoughts", 3, 3), # Toni in Science Weekly
        ("AI in Literature", 1, 2), # Alice in Literary Digest
        ("Big Brother and You", 2, 1) # George in Tech Monthly
    ]
    cursor.executemany("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", articles)

    # Commit changes to save inserts
    conn.commit()

    # Close the connection
    conn.close()

if __name__ == "__main__":
    seed_data()
