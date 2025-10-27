import mysql.connector

DB_CONFIG = {'host': 'localhost', 'user': 'lastfm', 'password': 'lastfm123'}

def get_connection(db_name=None):
    config = DB_CONFIG.copy()
    if db_name:
        config['database'] = db_name
    return mysql.connector.connect(**config)

def create_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DROP DATABASE IF EXISTS LastFM')
    cursor.execute('CREATE DATABASE LastFM')
    cursor.execute('USE LastFM')
    cursor.execute('CREATE TABLE artists (id INT PRIMARY KEY, name VARCHAR(255), url TEXT, pictureURL TEXT)')
    cursor.execute('CREATE TABLE tags (tagID INT PRIMARY KEY, tagValue VARCHAR(255))')
    cursor.execute('CREATE TABLE user_artists (userID INT, artistID INT, weight INT, PRIMARY KEY (userID, artistID), FOREIGN KEY (artistID) REFERENCES artists(id))')
    cursor.execute('CREATE TABLE user_taggedartists (userID INT, artistID INT, tagID INT, day INT, month INT, year INT, PRIMARY KEY (userID, artistID, tagID, day, month, year), FOREIGN KEY (artistID) REFERENCES artists(id), FOREIGN KEY (tagID) REFERENCES tags(tagID))')
    cursor.execute('CREATE TABLE user_friends (userID INT, friendID INT, PRIMARY KEY (userID, friendID))')
    conn.commit()
    cursor.close()
    conn.close()