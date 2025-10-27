from src.data_loader import load_data
from src.db_utils import get_connection

def remove_outliers(df, col, threshold=3):
    z = ((df[col] - df[col].mean()) / df[col].std()).abs()
    return df[z <= threshold], df[z > threshold]

def delete_from_db(cursor, table, id_col, ids):
    if len(ids):
        cursor.execute(f'DELETE FROM {table} WHERE {id_col} IN ({",".join(map(str, ids))})')

def clean_outliers():
    user_artists = load_data('data/user_artists.dat')
    user_taggedartists = load_data('data/user_taggedartists.dat')
    
    artist_weights = user_artists.groupby('artistID')['weight'].sum().reset_index(name='total_weight')
    clean_artists, removed_artists = remove_outliers(artist_weights, 'total_weight')
    
    tag_usage = user_taggedartists.groupby('tagID').size().reset_index(name='usage_count')
    clean_tags, removed_tags = remove_outliers(tag_usage, 'usage_count')
    
    user_weights = user_artists.groupby('userID')['weight'].sum().reset_index(name='total_weight')
    clean_users, removed_users = remove_outliers(user_weights, 'total_weight')
    
    conn = get_connection('LastFM')
    cursor = conn.cursor()
    delete_from_db(cursor, 'user_artists', 'artistID', removed_artists['artistID'])
    delete_from_db(cursor, 'user_taggedartists', 'tagID', removed_tags['tagID'])
    delete_from_db(cursor, 'user_artists', 'userID', removed_users['userID'])
    conn.commit()
    cursor.close()
    conn.close()
    
    clean_artists.to_csv('output/q2_clean_artists.csv', index=False)
    clean_tags.to_csv('output/q2_clean_tags.csv', index=False)
    clean_users.to_csv('output/q2_clean_users.csv', index=False)

if __name__ == '__main__':
    clean_outliers()