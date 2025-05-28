from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

# Example for testing
if __name__ == '__main__':
    a1 = Author.create("Alice")
    m1 = Magazine.create("Tech Times", "Technology")
    a1.add_article(m1, "AI in 2025")
    print(a1.articles())
    print(a1.magazines())
    print(m1.contributors())
