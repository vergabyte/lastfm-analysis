import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.load_data import load_data
from src.db_utils import get_connection

# Load data
user_artists = load_data("data/user_artists.dat")
tags = load_data("data/tags.dat")
user_taggedartists = load_data("data/user_taggedartists.dat")

# Utility: Remove outliers using z-score
def remove_outliers_zscore(df, column, threshold=3):
    mean = df[column].mean()
    std = df[column].std()
    df['zscore'] = (df[column] - mean) / std
    cleaned_df = df[df['zscore'].abs() <= threshold].copy()
    removed_df = df[df['zscore'].abs() > threshold]
    cleaned_df.drop(columns=['zscore'], inplace=True)
    return cleaned_df, removed_df

# Q2.1: Detect and remove outliers by listening count for artists
def clean_artist_listening():
    artist_weights = user_artists.groupby("artistID")["weight"].sum().reset_index()
    artist_weights.columns = ["artistID", "total_weight"]
    cleaned, removed = remove_outliers_zscore(artist_weights, "total_weight")
    print(f"Q2.1: Removed {len(removed)} artist outliers")
    return cleaned

# Q2.2: Detect and remove outliers by usage count for tags
def clean_tag_usage():
    tag_usage = user_taggedartists.groupby("tagID").size().reset_index(name="usage_count")
    cleaned, removed = remove_outliers_zscore(tag_usage, "usage_count")
    print(f"Q2.2: Removed {len(removed)} tag outliers")
    return cleaned

# Q2.3: Detect and remove outliers by total listening count for users
def clean_user_listening():
    user_weights = user_artists.groupby("userID")["weight"].sum().reset_index()
    user_weights.columns = ["userID", "total_weight"]
    cleaned, removed = remove_outliers_zscore(user_weights, "total_weight")
    print(f"Q2.3: Removed {len(removed)} user outliers")
    return cleaned

# Remove outliers from MySQL tables

def remove_outliers_from_mysql(table, id_column, ids_to_remove):
    conn = get_connection("LastFM")
    cursor = conn.cursor()
    format_strings = ','.join(['%s'] * len(ids_to_remove))
    query = f"DELETE FROM {table} WHERE {id_column} IN ({format_strings})"
    cursor.execute(query, tuple(ids_to_remove))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Removed {len(ids_to_remove)} records from {table} in MySQL")

def run():
    print("\nRunning Q2 (z-score based outlier detection)...")

    # Artist listening
    artist_weights, cleaned_artists, artist_removed = clean_artist_listening()
    print(f"Q2.1: Removed {len(artist_removed)} artist outliers")
    plot_boxplot_before_after(artist_weights, cleaned_artists, "total_weight", "Artist Listening Count")
    plot_top_outliers(artist_removed, "artistID", "total_weight", "Artist Listening Count")

    # Tag usage
    tag_usage, cleaned_tags, tag_removed = clean_tag_usage()
    print(f"Q2.2: Removed {len(tag_removed)} tag outliers")
    plot_boxplot_before_after(tag_usage, cleaned_tags, "usage_count", "Tag Usage Count")
    plot_top_outliers(tag_removed, "tagID", "usage_count", "Tag Usage Count")

    # User listening
    user_weights, cleaned_users, user_removed = clean_user_listening()
    print(f"Q2.3: Removed {len(user_removed)} user outliers")
    plot_boxplot_before_after(user_weights, cleaned_users, "total_weight", "User Listening Count")
    plot_top_outliers(user_removed, "userID", "total_weight", "User Listening Count")

    # Summary plot
    plot_outliers_removed_counts(artist_removed, tag_removed, user_removed)

    # Delete outliers from DB
    remove_outliers_from_mysql("user_artists", "artistID", artist_removed["artistID"].tolist())
    remove_outliers_from_mysql("user_taggedartists", "tagID", tag_removed["tagID"].tolist())
    remove_outliers_from_mysql("user_artists", "userID", user_removed["userID"].tolist())

    # Save cleaned datasets
    cleaned_artists.to_csv("output/q2_cleaned_artists.csv", index=False)
    cleaned_tags.to_csv("output/q2_cleaned_tags.csv", index=False)
    cleaned_users.to_csv("output/q2_cleaned_users.csv", index=False)
    print("Cleaned datasets saved to 'output/'")

def clean_artist_listening():
    artist_weights = user_artists.groupby("artistID")["weight"].sum().reset_index()
    artist_weights.columns = ["artistID", "total_weight"]
    return artist_weights, *remove_outliers_zscore(artist_weights, "total_weight")

def clean_tag_usage():
    tag_usage = user_taggedartists.groupby("tagID").size().reset_index(name="usage_count")
    return tag_usage, *remove_outliers_zscore(tag_usage, "usage_count")

def clean_user_listening():
    user_weights = user_artists.groupby("userID")["weight"].sum().reset_index()
    user_weights.columns = ["userID", "total_weight"]
    return user_weights, *remove_outliers_zscore(user_weights, "total_weight")

def plot_boxplot_before_after(original_df, cleaned_df, column, title):
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    sns.boxplot(y=original_df[column], ax=axs[0])
    axs[0].set_title(f"{title} - Before Cleaning")

    sns.boxplot(y=cleaned_df[column], ax=axs[1])
    axs[1].set_title(f"{title} - After Cleaning")

    plt.tight_layout()
    plt.show()

def plot_top_outliers(removed_df, id_column, value_column, title):
    # Build label map depending on which column we're plotting
    if id_column == "artistID":
        artists = load_data("data/artists.dat")
        label_map = dict(zip(artists["id"], artists["name"]))
    elif id_column == "tagID":
        tags = load_data("data/tags.dat")
        label_map = dict(zip(tags["tagID"], tags["tagValue"]))
    elif id_column == "userID":
        label_map = {uid: f"User {uid}" for uid in removed_df["userID"]}
    else:
        label_map = {id_val: str(id_val) for id_val in removed_df[id_column]}

    # Get top outliers and apply label
    top_outliers = removed_df.sort_values(value_column, ascending=False).head(10).copy()
    top_outliers["label"] = top_outliers[id_column].map(label_map)

    # Plot with names
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_outliers, x=value_column, y="label", palette="viridis")
    plt.title(f"Top 10 Outliers in {title}")
    plt.xlabel(value_column)
    plt.ylabel("")  # don't show "label"
    plt.tight_layout()
    plt.show()

def plot_outliers_removed_counts(artist_removed, tag_removed, user_removed):
    categories = ['Artists', 'Tags', 'Users']
    counts = [len(artist_removed), len(tag_removed), len(user_removed)]

    plt.figure(figsize=(8, 5))
    ax = sns.barplot(x=categories, y=counts, palette="Set2")

    # Annotate bars with count values
    for i, count in enumerate(counts):
        ax.text(i, count + max(counts)*0.02, str(count), ha='center', va='bottom', fontsize=12)

    plt.title("Number of Outliers Removed per Category", fontsize=14)
    plt.ylabel("Count", fontsize=12)
    plt.xlabel("")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run()