import pandas as pd
import numpy as np
import json
from src.data_loader import load_data
from src.db_utils import get_connection

def cosine_similarity(matrix):
    vals = matrix.values
    norm = np.linalg.norm(vals, axis=1)
    sim = np.dot(vals, vals.T) / (norm[:, None] * norm[None, :])
    return pd.DataFrame(sim, index=matrix.index, columns=matrix.index)

def compute_knn(sim_df, k):
    neighbors = {}
    for user in sim_df.index:
        sims = sim_df.loc[user].copy()
        sims[user] = -1
        neighbors[str(user)] = sims.nlargest(k).index.tolist()
    return neighbors

def batch_insert(cursor, sql, data, batch_size=10000):
    for i in range(0, len(data), batch_size):
        cursor.executemany(sql, data[i:i+batch_size])

def user_similarity():
    df = load_data('data/user_artists.dat')
    matrix = df.pivot_table(index='userID', columns='artistID', values='weight', fill_value=0)
    sim_df = cosine_similarity(matrix)
    sim_df.to_csv('output/user-pairs-similarity.dat', sep='\t')
    
    conn = get_connection('LastFM')
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE IF NOT EXISTS user_pairs_similarity (user1 INT, user2 INT, similarity FLOAT, PRIMARY KEY (user1, user2))')
    data = [(int(u1), int(u2), float(sim_df.loc[u1, u2])) for u1 in sim_df.index for u2 in sim_df.columns if u1 != u2]
    batch_insert(cursor, 'INSERT IGNORE INTO user_pairs_similarity VALUES (%s, %s, %s)', data)
    conn.commit()
    
    for k in [3, 10]:
        neighbors = compute_knn(sim_df, k)
        with open(f'output/neighbors-k{k}-users.dat', 'w') as f:
            json.dump(neighbors, f, indent=2)
        
        cursor.execute(f'CREATE TABLE IF NOT EXISTS neighbors_k{k}_users (userID INT, neighborID INT, rank_order INT, PRIMARY KEY (userID, neighborID))')
        data = [(int(user), n, rank+1) for user, nlist in neighbors.items() for rank, n in enumerate(nlist)]
        batch_insert(cursor, f'INSERT IGNORE INTO neighbors_k{k}_users VALUES (%s, %s, %s)', data)
        conn.commit()
    
    cursor.close()
    conn.close()

if __name__ == '__main__':
    user_similarity()