import pandas as pd
from src.db_utils import get_connection

PATHS = {
    'artists': 'data/artists.dat',
    'tags': 'data/tags.dat',
    'user_artists': 'data/user_artists.dat',
    'user_taggedartists': 'data/user_taggedartists.dat',
    'user_friends': 'data/user_friends.dat'
}

def load_data(filepath):
    return pd.read_csv(filepath, delimiter='\t', encoding='latin1')

def insert_data():
    conn = get_connection('LastFM')
    cursor = conn.cursor()
    
    for table, path in PATHS.items():
        df = load_data(path)
        cols = ','.join(df.columns)
        placeholders = ','.join(['%s'] * len(df.columns))
        values = [tuple(None if pd.isna(x) else x for x in row) for _, row in df.iterrows()]
        cursor.executemany(f'INSERT IGNORE INTO {table} ({cols}) VALUES ({placeholders})', values)
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    insert_data()