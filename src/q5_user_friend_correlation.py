import pandas as pd
import numpy as np
import mysql.connector
from src.load_data import load_data
from src.db_utils import get_connection
import matplotlib.pyplot as plt
import seaborn as sns

# Load necessary data
user_artists = load_data("data/user_artists.dat")
user_friends = load_data("data/user_friends.dat")

# Calculate number of friends per user
def compute_user_friend_counts():
    """Compute the number of friends each user has."""
    friend_counts = user_friends.groupby("userID").size().reset_index(name="friend_count")
    return friend_counts

# Q5.1: Correlation between number of artists and number of friends
def q5_1_artist_friend_correlation():
    """Compute correlation between number of artists a user listens to and their friend count."""
    artist_counts = user_artists.groupby("userID")["artistID"].nunique().reset_index(name="artist_count")
    friend_counts = compute_user_friend_counts()
    merged = pd.merge(artist_counts, friend_counts, on="userID")

    print(artist_counts)
    print(friend_counts)

    # Correlation
    corr = merged[["artist_count", "friend_count"]].corr().iloc[0, 1]
    print(f"\nCorrelation between number of artists and number of friends: {corr:.4f}")

    # Visualization
    sns.scatterplot(data=merged, x="artist_count", y="friend_count")
    plt.title("Artist Count vs Friend Count")
    plt.xlabel("Number of Artists")
    plt.ylabel("Number of Friends")
    plt.tight_layout()
    plt.savefig("output/q5_artist_friend_correlation.png")
    plt.show()

# Q5.2: Correlation between total listening time and number of friends
def q5_2_listening_friend_correlation():
    """Compute correlation between total listening time and number of friends."""
    listening_sum = user_artists.groupby("userID")["weight"].sum().reset_index(name="total_listening")
    friend_counts = compute_user_friend_counts()
    merged = pd.merge(listening_sum, friend_counts, on="userID")

    # Correlation
    corr = merged[["total_listening", "friend_count"]].corr().iloc[0, 1]
    print(f"\nCorrelation between total listening time and number of friends: {corr:.4f}")

    # Visualization
    sns.scatterplot(data=merged, x="total_listening", y="friend_count")
    plt.title("Total Listening Time vs Friend Count")
    plt.xlabel("Total Listening Time")
    plt.ylabel("Number of Friends")
    plt.tight_layout()
    plt.savefig("output/q5_listening_friend_correlation.png")
    plt.show()

if __name__ == "__main__":
    q5_1_artist_friend_correlation()
    q5_2_listening_friend_correlation()
