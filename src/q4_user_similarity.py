import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from src.load_data import load_data
from src.db_utils import get_connection

def load_user_artist_matrix():
    """Load user-artist interaction matrix with weights."""
    df = load_data("data/user_artists.dat")
    user_artist_matrix = df.pivot_table(index='userID', columns='artistID', values='weight', fill_value=0)
    return user_artist_matrix

def compute_cosine_similarity(matrix):
    """Manually compute cosine similarity between all user vectors."""
    matrix_values = matrix.values
    norm = np.linalg.norm(matrix_values, axis=1)
    similarity = np.dot(matrix_values, matrix_values.T) / (norm[:, None] * norm[None, :])
    return pd.DataFrame(similarity, index=matrix.index, columns=matrix.index)

def save_similarity_to_csv(similarity_df, path='output/user-pairs-similarity.dat'):
    """Save cosine similarity matrix to a TSV file."""
    similarity_df.to_csv(path, sep='\t')
    print(f"Saved cosine similarity matrix to {path}")

def save_similarity_to_mysql(similarity_df):
    """Store cosine similarity results in MySQL using batch insert."""
    conn = get_connection("LastFM")
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_pairs_similarity (
            user1 INT,
            user2 INT,
            similarity FLOAT,
            PRIMARY KEY (user1, user2)
        );
    """)

    # Prepare similarity data for all user pairs (excluding self)
    data = [
        (int(u1), int(u2), float(similarity_df.loc[u1, u2]))
        for u1 in similarity_df.index
        for u2 in similarity_df.columns
        if u1 != u2
    ]

    # Insert data in batches to prevent connection loss
    sql = "INSERT IGNORE INTO user_pairs_similarity (user1, user2, similarity) VALUES (%s, %s, %s)"
    batch_size = 10000
    for i in range(0, len(data), batch_size):
        cursor.executemany(sql, data[i:i + batch_size])
        conn.commit()

    cursor.close()
    conn.close()
    print("Saved similarity matrix to MySQL table 'user_pairs_similarity'")

def compute_knn_manual(similarity_df, k):
    """Compute k-nearest neighbors for each user based on similarity values."""
    neighbors_dict = {}
    for user in similarity_df.index:
        similarities = similarity_df.loc[user].copy()
        similarities[user] = -1  # Exclude self
        top_neighbors = similarities.sort_values(ascending=False).head(k).index.tolist()
        neighbors_dict[str(user)] = [int(n) for n in top_neighbors]
    return neighbors_dict

def save_knn_to_json(neighbors_dict, k):
    """Save k-nearest neighbors to JSON file in output folder."""
    file_path = f"output/neighbors-k{k}-users.dat"
    with open(file_path, "w") as f:
        json.dump(neighbors_dict, f, indent=2)
    print(f"Saved neighbors to {file_path}")

def save_knn_to_mysql(neighbors_dict, k):
    """Store k-nearest neighbors in MySQL using batch insert."""
    conn = get_connection("LastFM")
    cursor = conn.cursor()

    # Create neighbors table for k
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS neighbors_k{k}_users (
            userID INT,
            neighborID INT,
            rank_order INT,
            PRIMARY KEY (userID, neighborID)
        );
    """)

    # Prepare neighbor data for batch insert
    data = []
    for user, neighbors in neighbors_dict.items():
        for rank, neighbor in enumerate(neighbors, start=1):
            data.append((int(user), neighbor, rank))

    # Insert in batches
    sql = f"INSERT IGNORE INTO neighbors_k{k}_users (userID, neighborID, rank_order) VALUES (%s, %s, %s)"
    batch_size = 10000
    for i in range(0, len(data), batch_size):
        cursor.executemany(sql, data[i:i + batch_size])
        conn.commit()

    cursor.close()
    conn.close()
    print(f"Saved k-NN (k={k}) results to MySQL table 'neighbors_k{k}_users'")

def run_similarity():
    """Run full cosine similarity pipeline (load, compute, save)."""
    print("\nLoading user-artist matrix...")
    matrix = load_user_artist_matrix()

    print("\nComputing cosine similarity manually...")
    similarity_df = compute_cosine_similarity(matrix)
    save_similarity_to_csv(similarity_df)
    save_similarity_to_mysql(similarity_df)

    # Visualizing cosine similarity
    visualize_similarity_heatmap(similarity_df)
    visualize_similarity_histogram(similarity_df)

def run_knn():
    """Run k-NN computation and save to JSON and MySQL."""
    print("\nLoading user-artist matrix...")
    matrix = load_user_artist_matrix()
    similarity_df = compute_cosine_similarity(matrix)

    for k in [3, 10]:
        print(f"\nFinding top {k} neighbors manually...")
        neighbors_dict = compute_knn_manual(similarity_df, k=k)
        save_knn_to_json(neighbors_dict, k=k)
        save_knn_to_mysql(neighbors_dict, k=k)
        visualize_knn_barplot(similarity_df, neighbors_dict, k)

def run():
    """Execute full Q4 pipeline: similarity + k-NN."""
    run_similarity()
    run_knn()

def visualize_similarity_heatmap(similarity_df):
    """Show heatmap of cosine similarity matrix (subset of users)."""
    subset = similarity_df.iloc[:30, :30]
    
    plt.figure(figsize=(14, 12))
    sns.heatmap(
        subset, 
        cmap="viridis", 
        square=True, 
        annot=True, 
        fmt=".2f", 
        linewidths=0.5, 
        cbar_kws={'label': 'Cosine Similarity'}
    )
    plt.title("Cosine Similarity Heatmap (First 30 Users)", fontsize=16)
    plt.xlabel("User ID", fontsize=12)
    plt.ylabel("User ID", fontsize=12)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()

def visualize_similarity_histogram(similarity_df):
    """Plot histogram of user-user similarity scores (excluding diagonal)."""
    sim_matrix = similarity_df.values
    similarities = sim_matrix[~np.eye(sim_matrix.shape[0], dtype=bool)]
    plt.figure(figsize=(8, 6))
    plt.hist(similarities, bins=50, color='skyblue', edgecolor='black')
    plt.title("Distribution of User-User Cosine Similarities")
    plt.xlabel("Cosine Similarity")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def visualize_knn_barplot(similarity_df, neighbors_dict, k):
    """Bar plot for one example user's top-k neighbors."""
    example_user = list(neighbors_dict.keys())[0]
    top_neighbors = neighbors_dict[example_user]
    scores = [similarity_df.loc[int(example_user), n] for n in top_neighbors]

    plt.figure(figsize=(8, 6))
    plt.bar(range(len(top_neighbors)), scores, tick_label=top_neighbors)
    plt.title(f"Top {k} Neighbors of User {example_user}")
    plt.ylabel("Cosine Similarity")
    plt.xlabel("Neighbor User ID")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run()