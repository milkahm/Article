import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.models.magazine import Magazine
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def clean_database():
    """Clear relevant tables before each test to ensure isolation."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM articles")
        cursor.execute("DELETE FROM authors")
        cursor.execute("DELETE FROM magazines")
        conn.commit()

def test_magazine_creation():
    mag = Magazine(name="Science Weekly", category="Science")
    mag.save()
    assert mag.id is not None

def test_magazine_articles_and_contributors_empty():
    mag = Magazine(name="EmptyMag", category="None")
    mag.save()
    assert mag.articles() == []
    assert mag.contributors() == []
