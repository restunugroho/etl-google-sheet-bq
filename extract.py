import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def extract_from_gsheet(sheet_url, sheet_name, credentials_path):
    # Setup OAuth2
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    print(creds)
    client = gspread.authorize(creds)
    print(client)

    # Open sheet
    sheet = client.open_by_url(sheet_url).worksheet(sheet_name)

    # Get all data into a DataFrame
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    # Contoh penggunaan
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1N2WuTE4NpGSij0qTnYP1kciZNM83e_fW9cUWmoM835Y/edit?usp=sharing"
    SHEET_NAME = "data"
    CREDENTIAL_PATH = "config/credentials.json"

    df = extract_from_gsheet(SHEET_URL, SHEET_NAME, CREDENTIAL_PATH)
    print(df.head())
