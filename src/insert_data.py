import pandas as pd
from src.db_utils import get_connection
from src.load_data import load_data

def insert_dataframe(df, table_name):
    """Insert a DataFrame into the specified MySQL table."""
    conn = get_connection("LastFM")
    cursor = conn.cursor()

    cols = ",".join(df.columns)
    placeholders = ", ".join(["%s"] * len(df.columns))
    sql = f"INSERT IGNORE INTO {table_name} ({cols}) VALUES ({placeholders})"

    values_list = [
        tuple(None if pd.isna(x) else x for x in row)
        for _, row in df.iterrows()
    ]

    cursor.executemany(sql, values_list)
    conn.commit()
    print(f"Inserted {len(values_list)} rows into '{table_name}'")

    cursor.close()
    conn.close()

def run():
    """Load .dat files and insert them into MySQL tables."""
    datasets = {
        "artists": "data/artists.dat",
        "tags": "data/tags.dat",
        "user_artists": "data/user_artists.dat",
        "user_taggedartists": "data/user_taggedartists.dat",
        "user_friends": "data/user_friends.dat"
    }

    for table_name, path in datasets.items():
        print(f"\nProcessing '{table_name}'...")
        df = load_data(path)
        insert_dataframe(df, table_name)

if __name__ == "__main__":
    run()