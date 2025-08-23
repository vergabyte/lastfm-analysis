import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import mysql.connector
from src.load_data import load_data
from src.db_utils import get_connection

# Load tagging data
user_taggedartists = load_data("data/user_taggedartists.dat")

def preprocess_dates(df):
    """Convert year, month, day columns to datetime and extract year-month."""
    df['date'] = pd.to_datetime(dict(year=df['year'], month=df['month'], day=df['day']))
    df['year_month'] = df['date'].dt.to_period('M')
    return df

def print_counts_per_month(df):
    """Print number of unique users, tags, and artists per month."""
    users = df.groupby('year_month')['userID'].nunique()
    tags = df.groupby('year_month')['tagID'].nunique()
    artists = df.groupby('year_month')['artistID'].nunique()

    counts = pd.DataFrame({
        'unique_users': users,
        'unique_tags': tags,
        'unique_artists': artists
    })

    print("\nNumber of Users, Tags, and Artists per Month:")
    print(counts)
    counts.to_csv("output/q3_counts_per_month.csv")

def plot_monthly_counts():
    df = pd.read_csv("output/q3_counts_per_month.csv", index_col=0)
    df.index = pd.to_datetime(df.index)

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["unique_users"], label="Unique Users", marker='o')
    plt.plot(df.index, df["unique_tags"], label="Unique Tags", marker='s')
    plt.plot(df.index, df["unique_artists"], label="Unique Artists", marker='^')

    plt.title("Monthly Counts of Users, Tags, and Artists")
    plt.xlabel("Month")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("output/q3_monthly_counts_plot.png")
    plt.show()

def plot_zoomed_2008_2009():
    # Load and prepare the data
    df = pd.read_csv("output/q3_counts_per_month.csv", index_col=0)
    df.index = pd.to_datetime(df.index)

    # Filter for 2008–2009
    focus_df = df[(df.index >= "2008-01-01") & (df.index <= "2009-12-31")]

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(focus_df.index, focus_df["unique_users"], label="Unique Users", marker='o', linestyle='-', linewidth=2)
    plt.plot(focus_df.index, focus_df["unique_tags"], label="Unique Tags", marker='s', linestyle='--', linewidth=2)
    plt.plot(focus_df.index, focus_df["unique_artists"], label="Unique Artists", marker='^', linestyle='-.', linewidth=2)

    plt.title("Zoomed In: User, Tag, and Artist Activity (2008–2009)", fontsize=16)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(title="Entity", fontsize=10, title_fontsize=11)
    plt.tight_layout()

    # Save the plot
    plt.savefig("output/q3_zoomed_2008_2009_plot.png")
    plt.show()

def top_5_from_mysql():
    """Print top 5 tags and artists per month from MySQL."""
    conn = get_connection("LastFM")
    cursor = conn.cursor(dictionary=True)

    print("\nTop 5 Tags per Month:")
    cursor.execute("""
        SELECT 
            DATE_FORMAT(STR_TO_DATE(CONCAT(year, '-', month, '-', day), '%Y-%m-%d'), '%Y-%m') AS ym,
            tagID,
            COUNT(*) AS tag_count
        FROM user_taggedartists
        GROUP BY ym, tagID
        ORDER BY ym, tag_count DESC;
    """)
    rows = cursor.fetchall()
    df_tags = pd.DataFrame(rows)
    top5_tags = df_tags.groupby('ym').head(5)
    print(top5_tags)
    top5_tags.to_csv("output/q3_top5_tags_per_month.csv", index=False)

    print("\nTop 5 Artists per Month:")
    cursor.execute("""
        SELECT 
            DATE_FORMAT(STR_TO_DATE(CONCAT(year, '-', month, '-', day), '%Y-%m-%d'), '%Y-%m') AS ym,
            artistID,
            COUNT(*) AS artist_count
        FROM user_taggedartists
        GROUP BY ym, artistID
        ORDER BY ym, artist_count DESC;
    """)
    rows = cursor.fetchall()
    df_artists = pd.DataFrame(rows)
    top5_artists = df_artists.groupby('ym').head(5)
    print(top5_artists)
    top5_artists.to_csv("output/q3_top5_artists_per_month.csv", index=False)

    cursor.close()
    conn.close()

def plot_top_5_tags_for_years(years=("2008", "2009")):
    # Load top 5 tags per month
    top5_tags_df = pd.read_csv("output/q3_top5_tags_per_month.csv")

    # Load tag ID-to-name map
    tags_map_df = pd.read_csv("data/tags.dat", sep="\t", encoding="latin1")

    # Merge to get tag names
    merged_df = top5_tags_df.merge(tags_map_df, on="tagID")

    # Filter for the selected years
    merged_df = merged_df[merged_df["ym"].str[:4].isin(years)]

    # Plot
    plt.figure(figsize=(14, 6))
    sns.barplot(data=merged_df, x="ym", y="tag_count", hue="tagValue")
    plt.title(f"Top 5 Tags Per Month ({' & '.join(years)})")
    plt.xlabel("Month")
    plt.ylabel("Tag Usage Count")
    plt.xticks(rotation=45)
    plt.legend(title="Tag", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(f"output/q3_top5_tags_{'_'.join(years)}.png")
    plt.show()

def plot_top_5_artists_for_years(years=("2008", "2009")):
    # Load data
    top5_artists_df = pd.read_csv("output/q3_top5_artists_per_month.csv")
    artists_map_df = pd.read_csv("data/artists.dat", sep="\t", encoding="latin1")
    merged_df = top5_artists_df.merge(artists_map_df, left_on="artistID", right_on="id")

    # Filter for the selected years
    merged_df = merged_df[merged_df["ym"].str[:4].isin(years)]

    # Plot
    plt.figure(figsize=(20, 8))  # Wider plot, good height

    sns.barplot(data=merged_df, x="ym", y="artist_count", hue="name", width=2.5)

    plt.title("Top 5 Artists Per Month (2008 & 2009)", fontsize=16)
    plt.xlabel("Month", fontsize=11)
    plt.ylabel("Tagging Frequency", fontsize=11)
    plt.xticks(rotation=45, fontsize=10)

    # Move legend outside to the right, without shrinking the plot
    plt.legend(
        title="Artist",
        bbox_to_anchor=(1.01, 1),
        loc='upper left',
        borderaxespad=0,
        fontsize=10,
        title_fontsize=12
    )

    plt.tight_layout(rect=[0, 0, 0.75, 1])  # more room for legend
    plt.savefig(f"output/q3_top5_artists_{'_'.join(years)}.png")
    plt.show()

def run():
    print("\nRunning Q3: Monthly Trends Analysis...")
    df = preprocess_dates(user_taggedartists)

    # Q3.1: Using Pandas
    print_counts_per_month(df)

    # Q3.2: Using MySQL
    top_5_from_mysql()
    print("Q3 outputs saved to 'output/' folder.")

    plot_monthly_counts()
    plot_zoomed_2008_2009()
    plot_top_5_tags_for_years(("2008", "2009"))
    plot_top_5_artists_for_years(("2008", "2009"))


if __name__ == "__main__":
    run()
