import pandas as pd

def load_data(filepath):
    """Load a single .dat file."""
    return pd.read_csv(filepath, delimiter='\t', encoding='latin1')

def load_all_data():
    """Load all .dat files and return as a dictionary."""
    paths = {
        "artists": "data/artists.dat",
        "tags": "data/tags.dat",
        "user_artists": "data/user_artists.dat",
        "user_taggedartists": "data/user_taggedartists.dat",
        "user_friends": "data/user_friends.dat"
    }
    return {name: load_data(path) for name, path in paths.items()}