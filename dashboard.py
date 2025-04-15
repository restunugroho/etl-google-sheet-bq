import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from google.cloud import bigquery
from google.oauth2 import service_account
from prophet import Prophet

# === KONFIGURASI ===
PROJECT_ID = "komoditas-pangan-123"
DATASET = "komoditas_pangan"
TABLE = "harga"
CREDENTIAL_PATH = "config/credentials.json"

# === AUTH ===
credentials = service_account.Credentials.from_service_account_file(CREDENTIAL_PATH)
client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

# === AMBIL DATA ===
@st.cache_data(ttl=600)
def get_data():
    query = f"""
        SELECT * FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
    """
    df = client.query(query).to_dataframe()
    df["tanggal"] = pd.to_datetime(df["tanggal"])
    return df

# === UI DASHBOARD ===
st.title("📊 Dashboard Harga Komoditas Pangan")

df = get_data()

# === FILTER ===
komoditas_list = sorted(df["komoditas"].unique())
daerah_list = sorted(df["daerah"].unique())

col1, col2 = st.columns(2)
komoditas = col1.selectbox("Pilih Komoditas", komoditas_list)
daerah = col2.selectbox("Pilih Daerah", daerah_list)

filtered_df = df[(df["komoditas"] == komoditas) & (df["daerah"] == daerah)]

tanggal_min = filtered_df["tanggal"].min()
tanggal_max = filtered_df["tanggal"].max()
tanggal_range = st.date_input("Pilih rentang tanggal", [tanggal_min, tanggal_max])

filtered_df = filtered_df[
    (filtered_df["tanggal"] >= pd.to_datetime(tanggal_range[0])) &
    (filtered_df["tanggal"] <= pd.to_datetime(tanggal_range[1]))
]

st.write(f"Menampilkan data untuk **{komoditas}** di **{daerah}**:")
st.dataframe(filtered_df)

# === FORECASTING ===
st.subheader("📈 Forecast Harga 7 Hari ke Depan")

if len(filtered_df) >= 10:
    df_prophet = filtered_df[["tanggal", "harga_per_kg"]].rename(columns={"tanggal": "ds", "harga_per_kg": "y"})
    model = Prophet()
    model.fit(df_prophet)

    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)

    last_date = df_prophet["ds"].max()
    forecast_future = forecast[forecast["ds"] > last_date]

    fig = go.Figure()

    # Harga aktual
    fig.add_trace(go.Scatter(
        x=df_prophet["ds"], y=df_prophet["y"],
        mode="lines+markers", name="Aktual",
        line=dict(color="blue")
    ))

    # Prediksi hanya setelah data terakhir
    fig.add_trace(go.Scatter(
        x=forecast_future["ds"], y=forecast_future["yhat"],
        mode="lines", name="Forecast",
        line=dict(color="green", dash="dash")
    ))

    # Area shadow (confidence interval)
    fig.add_trace(go.Scatter(
        x=forecast_future["ds"], y=forecast_future["yhat_upper"],
        mode="lines", name="Upper Bound", line=dict(width=0),
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=forecast_future["ds"], y=forecast_future["yhat_lower"],
        mode="lines", name="Interval", line=dict(width=0),
        fill="tonexty", fillcolor="rgba(0, 200, 100, 0.2)",
        showlegend=True
    ))

    fig.update_layout(title="Forecast Harga 7 Hari ke Depan", xaxis_title="Tanggal", yaxis_title="Harga")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Data terlalu sedikit untuk melakukan forecast. Minimal 10 baris.")
