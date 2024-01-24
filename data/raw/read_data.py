import pandas as pd

def read_data():
    file_path = 'data/raw/kaufpreissammlung-liegenschaften.xlsx'
    df = pd.read_excel(file_path)
    return df

