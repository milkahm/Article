from lib.db.connection import get_connection

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")

    # Insert authors
    cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Alice Smith",))
    cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Bob Johnson",))

    # Insert magazines
    cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Tech Today", "Technology"))
    cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Health Weekly", "Health"))

    # Get the inserted IDs
    cursor.execute("SELECT id FROM authors WHERE name = 'Alice Smith'")
    alice_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM authors WHERE name = 'Bob Johnson'")
    bob_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM magazines WHERE name = 'Tech Today'")
    tech_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM magazines WHERE name = 'Health Weekly'")
    health_id = cursor.fetchone()[0]

    # Insert articles
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                   ("The Future of AI", alice_id, tech_id))
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                   ("Staying Fit in 2025", bob_id, health_id))

    conn.commit()
    conn.close()
    print("✅ Seed data inserted.")

if __name__ == "__main__":
    seed_data()
