from lib.models.author import Author

def test_author_can_be_created():
    author = Author(1, "Test Author")
    assert author.name == "Test Author"