import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.models.author import Author
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def clean_database():
    """Clear authors table before each test to isolate tests."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM authors")
        conn.commit()

def test_author_can_be_created_and_saved():
    author = Author("Test Author")
    author.save()
    assert author.id is not None

def test_author_can_be_found_by_id():
    author = Author("Find Me")
    author.save()

    found = Author.find_by_id(author.id)
    assert found is not None
    assert found.name == "Find Me"
