from src.data_loader import load_data, PATHS

def explore_data():
    data = {name: load_data(path) for name, path in PATHS.items()}
    
    for name, df in data.items():
        print(f'\n{name.upper()}')
        print(df.info())
        print(df.describe(include='all'))
        print(df.head())

if __name__ == '__main__':
    explore_data()