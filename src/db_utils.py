import mysql.connector

def get_connection(db_name=None):
    """Establish and return a MySQL connection."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="pvergas",
        database=db_name
    )

def create_database():
    """Create the LastFM database and all required tables."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP DATABASE IF EXISTS LastFM;")
    cursor.execute("CREATE DATABASE LastFM;")
    cursor.execute("USE LastFM;")

    table_queries = {
        "artists": """
            CREATE TABLE IF NOT EXISTS artists (
                id INT PRIMARY KEY,
                name VARCHAR(255),
                url TEXT,
                pictureURL TEXT
            )
        """,
        "tags": """
            CREATE TABLE IF NOT EXISTS tags (
                tagID INT PRIMARY KEY,
                tagValue VARCHAR(255)
            )
        """,
        "user_artists": """
            CREATE TABLE IF NOT EXISTS user_artists (
                userID INT,
                artistID INT,
                weight INT,
                PRIMARY KEY (userID, artistID),
                FOREIGN KEY (artistID) REFERENCES artists(id)
            )
        """,
        "user_taggedartists": """
            CREATE TABLE IF NOT EXISTS user_taggedartists (
                userID INT,
                artistID INT,
                tagID INT,
                day INT,
                month INT,
                year INT,
                PRIMARY KEY (userID, artistID, tagID, day, month, year),
                FOREIGN KEY (artistID) REFERENCES artists(id),
                FOREIGN KEY (tagID) REFERENCES tags(tagID)
            )
        """,
        "user_friends": """
            CREATE TABLE IF NOT EXISTS user_friends (
                userID INT,
                friendID INT,
                PRIMARY KEY (userID, friendID)
            )
        """
    }

    for name, query in table_queries.items():
        cursor.execute(query)
        print(f"Table '{name}' created successfully!")

    conn.commit()
    cursor.close()
    conn.close()
    print("Database and tables setup complete.")

if __name__ == "__main__":
    create_database()

