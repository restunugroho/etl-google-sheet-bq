# load.py

from google.cloud import bigquery
from extract import extract_from_gsheet
from transform import clean_data

# --- CONFIG ---
PROJECT_ID = "komoditas-pangan-123"  # Ganti dengan project kamu
DATASET_ID = "komoditas_pangan"
TABLE_ID = "harga"
CREDENTIAL_PATH = "config/credentials.json"

# URL dan sheet name dari Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1N2WuTE4NpGSij0qTnYP1kciZNM83e_fW9cUWmoM835Y/edit?usp=sharing"
SHEET_NAME = "data"

def load_to_bigquery(df, credentials_path):
    client = bigquery.Client.from_service_account_json(credentials_path)
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",  # Hapus isi tabel, replace full
        autodetect=True,  # Deteksi schema otomatis
    )

    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()  # Tunggu sampai selesai
    print(f"✅ Data berhasil di-replace ke BigQuery: {table_ref}")

if __name__ == "__main__":
    # 1. Ekstrak data dari Google Sheets
    df_raw = extract_from_gsheet(SHEET_URL, SHEET_NAME, CREDENTIAL_PATH)

    # 2. Transformasi / pembersihan
    df_clean = clean_data(df_raw)

    # 3. Load ke BigQuery (overwrite)
    load_to_bigquery(df_clean, CREDENTIAL_PATH)
