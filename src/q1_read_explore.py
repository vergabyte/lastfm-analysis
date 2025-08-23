import pandas as pd
import matplotlib.pyplot as plt
from src.load_data import load_data, load_all_data

def describe_dataframe(name, df):
    """Print statistical description and sample rows."""
    print(f"\n--- {name.upper()} ---")
    print("\nInfo:")
    print(df.info())
    print("\nStatistical Description:")
    print(df.describe(include='all'))
    print("\nTop 5 rows:")
    print(df.head())
    print("\nBottom 5 rows:")
    print(df.tail())
    print("=" * 60)

def plot_top_10_artists(user_artists_df, artists_df):
    """Plot the top 10 most listened to artists by total weight."""
    top_artists = user_artists_df.groupby('artistID')['weight'].sum().reset_index()
    top_artists = top_artists.sort_values(by='weight', ascending=False).head(10)
    
    # Merge with artist names
    top_artists = top_artists.merge(artists_df, left_on='artistID', right_on='id')

    # Plot
    plt.figure(figsize=(12, 6))
    plt.bar(top_artists['name'], top_artists['weight'])
    plt.xticks(rotation=45, ha='right')
    plt.title('Top 10 Most Listened Artists')
    plt.xlabel('Artist Name')
    plt.ylabel('Total Listening Count')
    plt.tight_layout()
    plt.savefig("output/q1_top_10_artists.png")
    plt.show()

def plot_top_10_tags(user_taggedartists_df, tags_df):
    """Plot the top 10 most used tags."""
    top_tags = user_taggedartists_df['tagID'].value_counts().head(10).reset_index()
    top_tags.columns = ['tagID', 'count']

    # Merge with tag names
    top_tags = top_tags.merge(tags_df, on='tagID')

    # Plot
    plt.figure(figsize=(12, 6))
    plt.bar(top_tags['tagValue'], top_tags['count'])
    plt.xticks(rotation=45, ha='right')
    plt.title('Top 10 Most Used Tags')
    plt.xlabel('Tag')
    plt.ylabel('Usage Count')
    plt.tight_layout()
    plt.savefig("output/q1_top_10_tags.png")
    plt.show()

def run():
    """Main function to load and explore all datasets."""
    dataframes = load_all_data()

    for name, df in dataframes.items():
        describe_dataframe(name, df)

    # Plot top 10 artists
    plot_top_10_artists(dataframes['user_artists'], dataframes['artists'])

    # Plot top 10 tags
    plot_top_10_tags(dataframes['user_taggedartists'], dataframes['tags'])

if __name__ == "__main__":
    run()
