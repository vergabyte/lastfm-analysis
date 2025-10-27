import pandas as pd
from src.data_loader import load_data
from src.db_utils import get_connection

def get_top5_by_month(cursor, entity):
    cursor.execute(f'''
        SELECT DATE_FORMAT(STR_TO_DATE(CONCAT(year, '-', month, '-', day), '%Y-%m-%d'), '%Y-%m') AS ym,
               {entity}ID, COUNT(*) AS count
        FROM user_taggedartists
        GROUP BY ym, {entity}ID
        ORDER BY ym, count DESC
    ''')
    return pd.DataFrame(cursor.fetchall()).groupby('ym').head(5)

def temporal_analysis():
    df = load_data('data/user_taggedartists.dat')
    df['year_month'] = pd.to_datetime(df[['year', 'month', 'day']]).dt.to_period('M')
    
    counts = pd.DataFrame({
        'users': df.groupby('year_month')['userID'].nunique(),
        'tags': df.groupby('year_month')['tagID'].nunique(),
        'artists': df.groupby('year_month')['artistID'].nunique()
    })
    counts.to_csv('output/q3_monthly_counts.csv')
    
    conn = get_connection('LastFM')
    cursor = conn.cursor(dictionary=True)
    get_top5_by_month(cursor, 'tag').to_csv('output/q3_top5_tags.csv', index=False)
    get_top5_by_month(cursor, 'artist').to_csv('output/q3_top5_artists.csv', index=False)
    cursor.close()
    conn.close()

if __name__ == '__main__':
    temporal_analysis()