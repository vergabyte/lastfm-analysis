import pandas as pd
from src.data_loader import load_data

def friend_correlation():
    user_artists = load_data('data/user_artists.dat')
    user_friends = load_data('data/user_friends.dat')
    friend_counts = user_friends.groupby('userID').size().reset_index(name='friend_count')
    
    artist_counts = user_artists.groupby('userID')['artistID'].nunique().reset_index(name='artist_count')
    merged = artist_counts.merge(friend_counts, on='userID')
    corr1 = merged[['artist_count', 'friend_count']].corr().iloc[0, 1]
    print(f'Artist-Friend correlation: {corr1:.4f}')
    
    listening = user_artists.groupby('userID')['weight'].sum().reset_index(name='total_listening')
    merged = listening.merge(friend_counts, on='userID')
    corr2 = merged[['total_listening', 'friend_count']].corr().iloc[0, 1]
    print(f'Listening-Friend correlation: {corr2:.4f}')

if __name__ == '__main__':
    friend_correlation()