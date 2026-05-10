import streamlit as st
import pandas as pd
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(page_title="Pembukuan Keuangan Sederhana", layout="centered")

st.title("📒 Pembukuan Keuangan Sederhana")
st.write("Aplikasi sederhana untuk mencatat pemasukan dan pengeluaran.")

# Session state untuk menyimpan data
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Tanggal", "Keterangan", "Kategori", "Jenis", "Jumlah"
    ])

# Form input transaksi
with st.form("form_keuangan"):
    tanggal = st.date_input("Tanggal", datetime.today())
    keterangan = st.text_input("Keterangan")
    kategori = st.selectbox(
        "Kategori",
        ["Makanan", "Transportasi", "Belanja", "Gaji", "Lainnya"]
    )
    jenis = st.radio("Jenis Transaksi", ["Pemasukan", "Pengeluaran"])
    jumlah = st.number_input("Jumlah (Rp)", min_value=0, step=1000)

    submit = st.form_submit_button("Tambah Transaksi")

    if submit:
        data_baru = pd.DataFrame({
            "Tanggal": [tanggal],
            "Keterangan": [keterangan],
            "Kategori": [kategori],
            "Jenis": [jenis],
            "Jumlah": [jumlah]
        })

        st.session_state.data = pd.concat(
            [st.session_state.data, data_baru],
            ignore_index=True
        )

        st.success("Transaksi berhasil ditambahkan!")

# Menampilkan data
st.subheader("📋 Data Transaksi")

if not st.session_state.data.empty:
    st.dataframe(st.session_state.data, use_container_width=True)

    # Perhitungan keuangan
    pemasukan = st.session_state.data[
        st.session_state.data["Jenis"] == "Pemasukan"
    ]["Jumlah"].sum()

    pengeluaran = st.session_state.data[
        st.session_state.data["Jenis"] == "Pengeluaran"
    ]["Jumlah"].sum()

    saldo = pemasukan - pengeluaran

    # Ringkasan
    st.subheader("💰 Ringkasan Keuangan")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Pemasukan", f"Rp {pemasukan:,.0f}")
    col2.metric("Total Pengeluaran", f"Rp {pengeluaran:,.0f}")
    col3.metric("Saldo", f"Rp {saldo:,.0f}")

    # Grafik
    st.subheader("📊 Grafik Keuangan")

    grafik = pd.DataFrame({
        "Jenis": ["Pemasukan", "Pengeluaran"],
        "Jumlah": [pemasukan, pengeluaran]
    })

    st.bar_chart(grafik.set_index("Jenis"))

    # Download CSV
    csv = st.session_state.data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Data CSV",
        data=csv,
        file_name="pembukuan_keuangan.csv",
        mime="text/csv"
    )

else:
    st.info("Belum ada data transaksi.")
