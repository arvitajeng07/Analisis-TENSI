import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Analisis Tensi Puskesmas")

st.write("Upload file Excel tensi untuk analisis grafik dan deteksi anomali.")

uploaded = st.file_uploader("Upload file (format .xlsx)", type=["xlsx"])

if uploaded:
    df = pd.read_excel(uploaded)

    st.subheader("📄 Data Tensi")
    st.dataframe(df)

    # Sesuaikan nama kolom Excel kamu
    sistol_col = "Sistol"
    diastol_col = "Diastol"

    # Batas normal
    low_sys = 90
    high_sys = 140
    low_dia = 60
    high_dia = 90

    # Analisis tensi
    df['Status'] = df.apply(lambda row: 
        'Tinggi' if row[sistol_col] > high_sys or row[diastol_col] > high_dia else
        'Rendah' if row[sistol_col] < low_sys or row[diastol_col] < low_dia else
        'Normal', axis=1)

    st.subheader("📊 Grafik Tensi")

    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(df[sistol_col], label='Sistol')
    ax.plot(df[diastol_col], label='Diastol')
    ax.set_xlabel("Index")
    ax.set_ylabel("Tensi")
    ax.legend()

    st.pyplot(fig)

    st.subheader("🔔 Hasil Analisis")

    abnormal = df[df['Status'] != "Normal"]

    if len(abnormal) > 0:
        st.error("⚠ Ada tensi yang tinggi/rendah!")
        st.write(abnormal)
    else:
        st.success("✔ Semua tensi normal.")
