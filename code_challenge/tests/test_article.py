import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def clean_database():
    """Run before each test to clear relevant tables for test isolation."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM articles")
        cursor.execute("DELETE FROM authors")
        cursor.execute("DELETE FROM magazines")
        conn.commit()

def test_article_creation():
    author = Author("Writer")
    author.save()

    mag = Magazine("Mag1", "Tech")
    mag.save()

    article = Article(title="My First", author_id=author.id, magazine_id=mag.id)
    article.save()

    assert article.id is not None
