# transform.py
import pandas as pd

def clean_data(df):
    # Ubah tanggal jadi format datetime
    df['tanggal'] = pd.to_datetime(df['tanggal'], errors='coerce')

    # Drop rows yang tanggalnya kosong
    df = df.dropna(subset=['tanggal'])

    # Harga ke integer (kalau string)
    df['harga_per_kg'] = pd.to_numeric(df['harga_per_kg'], errors='coerce')

    # Drop duplikat dan sort
    df = df.drop_duplicates()
    df = df.sort_values(by='tanggal')

    return df
