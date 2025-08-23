import os
from src import (
    db_utils,
    insert_data,
    q1_read_explore,
    q2_outlier_removal,
    q3_temporal_exploration,
    q4_user_similarity,
    q5_user_friend_correlation
)

# Ensure output folder exists 
os.makedirs("output", exist_ok=True)

def main():
    print("\nStarting LastFM project pipeline...")

    # Q1: Create the database and tables
    print("\nCreating database and tables...")
    db_utils.create_database()

    # Q1: Insert data into MySQL
    print("\nInserting data into tables...")
    insert_data.run()

    # Q1: Explore and describe data
    print("\nExploring data...")
    q1_read_explore.run()

    # Q2: Remove outliers using z-score method
    print("\nRemoving outliers...")
    q2_outlier_removal.run()

    # Q3: Monthly trends analysis (Pandas + MySQL)
    print("\nMonthly tag and artist activity analysis...")
    q3_temporal_exploration.run()

    # Q4: Compute cosine similarity between users
    print("\nComputing user-user cosine similarity...")
    q4_user_similarity.run_similarity()

    # Q4: Compute k-nearest neighbors for users
    print("\nFinding k-nearest neighbors for users...")
    q4_user_similarity.run_knn()

    # Q5: Correlation analysis between users and friends
    print("\nQ5.1: Correlation between artist count and friend count")
    q5_user_friend_correlation.q5_1_artist_friend_correlation()

    # Q5: Correlation analysis between total listening time of a user and the number of friends
    print("\nQ5.2: Correlation between total listening and friend count")
    q5_user_friend_correlation.q5_2_listening_friend_correlation()

    print("\nCompleted successfully!")

if __name__ == "__main__":
    main()
