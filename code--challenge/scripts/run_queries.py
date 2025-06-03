from lib.models.author import Author
from lib.models.article import Article, add_author_with_articles
from lib.models.magazine import Magazine

def run_queries():
    print("\n--- RUNNING SAMPLE QUERIES ---")

    # 1. Create new author and magazines
    author = Author("Demo Author")
    author.save()

    mag1 = Magazine("Tech Monthly", "Technology")
    mag2 = Magazine("Food World", "Cuisine")
    mag1.save()
    mag2.save()

    # 2. Add articles by the author
    author.add_article(mag1, "AI in 2025")
    author.add_article(mag2, "Gourmet Guide")

    # 3. Print author's magazines
    print("\nMagazines by Author:")
    for mag in author.magazines():
        print(f"- {mag['name']} ({mag['category']})")

    # 4. Print topic areas for the author
    print("\nTopic Areas:")
    print(author.topic_areas())

    # 5. Contributors to a magazine
    print("\nContributors to Tech Monthly:")
    for contributor in mag1.contributors():
        print(f"- {contributor['name']}")

    # 6. Create author with multiple articles in a transaction
    print("\nAdding bulk articles with transaction...")
    success = add_author_with_articles("Bulk Author", [
        {"title": "Quantum Basics", "magazine_id": mag1.id},
        {"title": "Future of Code", "magazine_id": mag1.id}
    ])
    print("Transaction success?", success)

    # 7. Get article titles from magazine
    print("\nArticles in Tech Monthly:")
    for title in mag1.article_titles():
        print(f"- {title}")

if __name__ == "__main__":
    run_queries()
