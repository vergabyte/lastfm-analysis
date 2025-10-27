import os

from src import db_utils
from src import data_loader
from src import q1_read_explore
from src import q2_outlier_removal
from src import q3_temporal_exploration
from src import q4_user_similarity
from src import q5_user_friend_correlation

os.makedirs('output', exist_ok=True)

def main():
    db_utils.create_database()
    data_loader.insert_data()
    q1_read_explore.explore_data()
    q2_outlier_removal.clean_outliers()
    q3_temporal_exploration.temporal_analysis()
    q4_user_similarity.user_similarity()
    q5_user_friend_correlation.friend_correlation()

if __name__ == '__main__':
    main()