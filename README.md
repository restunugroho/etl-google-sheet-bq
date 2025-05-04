# 📊 ETL Komoditas Pangan: Google Sheets ➝ BigQuery ➝ Streamlit
ETL (Extract, Transform, Load) adalah proses yang digunakan untuk mengumpulkan, memproses, dan memindahkan data dari berbagai sumber ke dalam data warehouse atau sistem lain untuk dianalisis lebih lanjut. Proses ini menjadi salah satu tulang punggung dalam pengelolaan data di banyak perusahaan, terutama yang memiliki volume data besar dan berasal dari berbagai sumber yang berbeda. Dengan menggunakan ETL, data yang tersebar dan mungkin tidak terstruktur dapat disatukan dalam satu tempat yang terorganisir dan siap untuk dianalisis.

Mini-project ini adalah pipeline ETL sederhana yang mengambil data harga komoditas pangan dari Google Sheets, membersihkannya dengan Python, dan memuatnya ke BigQuery. Kemudian data dapat divisualisasikan dengan Streamlit. 

Project ETL dari Google Sheet ke Data Warehouse dilakukan ketika data diinput biasanya oleh tim lapangan / non IT ke dalam Google Sheet, sehingga di beberapa kasus lumrah dilakukan.

## 🔧 Tools & Teknologi
- 🟢 Google Sheets (sebagai sumber data)
- 🟡 Python (ETL scripts)
- 🔵 Google BigQuery (penyimpanan data)
- ⚪ Streamlit (dashboard visualisasi)
- 🔐 Service Account (akses API)

## 📁 Struktur Folder
```
etl-komoditas/
│
├── config/
│   └── credentials.json       # File kredensial Service Account (JANGAN upload ke GitHub!)
│
├── extract.py                 # Mengambil data dari Google Sheets
├── transform.py              # Membersihkan dan menyiapkan data
├── load.py                   # Mengirim data ke BigQuery (overwrite, free tier friendly)
├── dashboard.py              # Visualisasi dengan Streamlit (opsional)
├── requirements.txt          # Daftar dependency
└── README.md                 # Dokumentasi proyek ini
```

## ✅ Prasyarat

### 1. Aktifkan Google Cloud API
- Masuk ke [Google Cloud Console](https://console.cloud.google.com/)
- Pilih project kamu atau buat project baru
- Aktifkan:
  - **BigQuery API**
  - **Google Sheets API**

### 🔐 2. Buat Service Account & Simpan Kredensial
1. Masuk ke [IAM & Admin – Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Klik **Create Service Account**
   - Name: `etl-service`
   - Klik **Create and Continue**
3. Tambahkan roles:
   - `BigQuery Data Editor`
   - `BigQuery Job User`
4. Klik **Done**
5. Setelah service account dibuat:
   - Klik nama service account ➝ buka tab **Keys**
   - Klik **Add Key** ➝ **Create new key**
     - Pilih **JSON**
     - Simpan file ke: `config/credentials.json`
6. Salin email service account, misalnya: `etl-service@your-project-id.iam.gserviceaccount.com`
7. Buka file Google Sheets kamu ➝ klik **Share**
   - Tambahkan email tersebut
   - Berikan akses **Editor**

### 🗂️ 3. Buat Dataset & Tabel di BigQuery

#### Opsi A: Manual (di UI)
1. Buka [BigQuery Console](https://console.cloud.google.com/bigquery)
2. Klik project ➝ **+ CREATE DATASET**
   - ID: `komoditas_pangan`
   - Location: `US`
   - Klik **Create**
3. Di dalam dataset ➝ **+ CREATE TABLE**
   - Source: **Empty table**
   - Table name: `harga`
   - Schema (input manual):

     | Field         | Type   | Mode     |
     |---------------|--------|----------|
     | tanggal       | DATE   | NULLABLE |
     | komoditas     | STRING | NULLABLE |
     | daerah        | STRING | NULLABLE |
     | harga_per_kg  | FLOAT  | NULLABLE |

   - Klik **Create Table**

#### Opsi B: Otomatis dari script
Biarkan script `load.py` membuat tabel dengan `autodetect=True`.

## ⚙️ Instalasi & Setup
```bash
# Clone repo
git clone https://github.com/username/etl-komoditas.git
cd etl-komoditas

# Aktifkan virtual environment (opsional)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🧪 Cara Menjalankan

### 1. Ekstrak data dari Google Sheets
```bash
python extract.py
```

### 2. Transformasi & pembersihan data
```bash
python transform.py
```

### 3. Load ke BigQuery (overwrite semua data)
```bash
python load.py
```

📌 **Catatan**:  
Script `load.py` ini dirancang agar bisa digunakan di BigQuery **Free Tier (sandbox)**, jadi tidak menggunakan query `MERGE`, `UPDATE`, atau `INSERT`.  
Semua data di tabel akan diganti setiap kali script dijalankan (`WRITE_TRUNCATE`).

## 📊 Jalankan Visualisasi (Streamlit)
```bash
streamlit run dashboard.py
```

## 🛡️ Tips Keamanan
> ❗ Jangan pernah mengupload `credentials.json` ke GitHub publik!

Tambahkan ini ke file `.gitignore`:
```
config/credentials.json
```

## ✍️ Kontribusi
Silakan fork, pull request, atau kembangkan project ini sesuai kebutuhan kamu 🙌
