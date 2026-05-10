import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# =========================================
# KONFIGURASI HALAMAN
# =========================================
st.set_page_config(
    page_title="Pembukuan Es",
    layout="wide"
)

st.title("📒 Sistem Pembukuan Jualan Es")

# =========================================
# FILE DATABASE JSON
# =========================================
USER_FILE = "users.json"
MENU_FILE = "menu.json"
PENGELUARAN_FILE = "pengeluaran.json"
PENDAPATAN_FILE = "pendapatan.json"
KARYAWAN_FILE = "karyawan.json"

# =========================================
# DEFAULT ADMIN
# =========================================
DEFAULT_HOST = {
    "admin": {
        "password": "admin123",
        "role": "host"
    }
}

# =========================================
# LOAD JSON
# =========================================
def load_json(file, default):

    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump(default, f)

    with open(file, "r") as f:
        return json.load(f)

# =========================================
# SAVE JSON
# =========================================
def save_json(file, data):

    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# =========================================
# LOAD DATABASE
# =========================================
users = load_json(USER_FILE, DEFAULT_HOST)
menu_data = load_json(MENU_FILE, [])
pengeluaran_data = load_json(PENGELUARAN_FILE, [])
pendapatan_data = load_json(PENDAPATAN_FILE, [])
karyawan_data = load_json(KARYAWAN_FILE, [])

# =========================================
# SESSION
# =========================================
if "login" not in st.session_state:
    st.session_state.login = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

# =========================================
# LOGIN PAGE
# =========================================
if not st.session_state.login:

    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username in users:

            if users[username]["password"] == password:

                st.session_state.login = True
                st.session_state.username = username
                st.session_state.role = users[username]["role"]

                st.success("Login berhasil")
                st.rerun()

            else:
                st.error("Password salah")

        else:
            st.error("Username tidak ditemukan")

# =========================================
# DASHBOARD
# =========================================
else:

    st.sidebar.success(f"Login : {st.session_state.username}")
    st.sidebar.info(f"Role : {st.session_state.role}")

    if st.sidebar.button("Logout"):

        st.session_state.login = False
        st.session_state.username = ""
        st.session_state.role = ""

        st.rerun()

    # =====================================
    # MENU HOST
    # =====================================
    if st.session_state.role == "host":

        menu = st.sidebar.radio(
            "Menu",
            [
                "Menu Jualan",
                "Pengeluaran",
                "Pendapatan",
                "Karyawan",
                "Rekap Harian",
                "Rekap Bulanan",
                "Grafik"
            ]
        )

        # =================================
        # 1. MENU JUALAN
        # =================================
        if menu == "Menu Jualan":

            st.subheader("🍹 Tambah Menu Jualan")

            nama = st.text_input("Nama Es")

            harga_1 = st.number_input(
                "Harga 1 Barang",
                min_value=0,
                step=1000
            )

            harga_2 = st.number_input(
                "Harga Paket 2 Barang",
                min_value=0,
                step=1000
            )

            if st.button("Tambah Menu"):

                data = {
                    "nama": nama,
                    "harga_1": harga_1,
                    "harga_2": harga_2
                }

                menu_data.append(data)

                save_json(MENU_FILE, menu_data)

                st.success("Menu berhasil ditambahkan")

            st.divider()

            st.subheader("📋 Daftar Menu")

            df = pd.DataFrame(menu_data)

            if not df.empty:
                st.dataframe(df, use_container_width=True)

        # =================================
        # 2. PENGELUARAN
        # =================================
        elif menu == "Pengeluaran":

            st.subheader("💸 Modal / Pengeluaran")

            tanggal = st.date_input("Tanggal")

            barang = st.text_input("Membeli Apa")

            harga = st.number_input(
                "Harga",
                min_value=0,
                step=1000
            )

            if st.button("Tambah Pengeluaran"):

                data = {
                    "tanggal": str(tanggal),
                    "barang": barang,
                    "harga": harga,
                    "user": st.session_state.username
                }

                pengeluaran_data.append(data)

                save_json(PENGELUARAN_FILE, pengeluaran_data)

                st.success("Pengeluaran berhasil ditambahkan")

            df = pd.DataFrame(pengeluaran_data)

            if not df.empty:
                st.dataframe(df, use_container_width=True)

        # =================================
        # 3. PENDAPATAN
        # =================================
        elif menu == "Pendapatan":

            st.subheader("💰 Pendapatan")

            tanggal = st.date_input("Tanggal")

            pilihan_menu = [x["nama"] for x in menu_data]

            nama_menu = st.selectbox(
                "Pilih Menu",
                pilihan_menu
            )

            jumlah = st.number_input(
                "Jumlah Terjual",
                min_value=1
            )

            harga = 0

            for x in menu_data:

                if x["nama"] == nama_menu:

                    if jumlah >= 2:
                        harga = x["harga_2"]
                    else:
                        harga = x["harga_1"]

            total = harga * jumlah

            st.info(f"Total Pendapatan : Rp {total:,.0f}")

            if st.button("Tambah Pendapatan"):

                data = {
                    "tanggal": str(tanggal),
                    "menu": nama_menu,
                    "jumlah": jumlah,
                    "total": total
                }

                pendapatan_data.append(data)

                save_json(PENDAPATAN_FILE, pendapatan_data)

                st.success("Pendapatan berhasil ditambahkan")

            df = pd.DataFrame(pendapatan_data)

            if not df.empty:
                st.dataframe(df, use_container_width=True)

        # =================================
        # 4. KARYAWAN
        # =================================
        elif menu == "Karyawan":

            st.subheader("👨‍🔧 Tambah Karyawan")

            nama = st.text_input("Nama Karyawan")

            gaji = st.number_input(
                "Gaji per Bulan",
                min_value=0,
                step=100000
            )

            username = st.text_input("Username")

            password = st.text_input(
                "Password",
                type="password"
            )

            if st.button("Tambah Karyawan"):

                users[username] = {
                    "password": password,
                    "role": "karyawan"
                }

                save_json(USER_FILE, users)

                data = {
                    "nama": nama,
                    "gaji": gaji,
                    "username": username
                }

                karyawan_data.append(data)

                save_json(KARYAWAN_FILE, karyawan_data)

                st.success("Karyawan berhasil ditambahkan")

            df = pd.DataFrame(karyawan_data)

            if not df.empty:
                st.dataframe(df, use_container_width=True)

        # =================================
        # 5. REKAP HARIAN
        # =================================
        elif menu == "Rekap Harian":

            st.subheader("📅 Rekap Harian")

            pendapatan_df = pd.DataFrame(pendapatan_data)
            pengeluaran_df = pd.DataFrame(pengeluaran_data)

            if not pendapatan_df.empty:

                pendapatan_harian = pendapatan_df.groupby(
                    "tanggal"
                )["total"].sum()

                pengeluaran_harian = pengeluaran_df.groupby(
                    "tanggal"
                )["harga"].sum()

                rekap = pd.concat(
                    [pendapatan_harian, pengeluaran_harian],
                    axis=1
                ).fillna(0)

                rekap.columns = [
                    "Pendapatan",
                    "Pengeluaran"
                ]

                rekap["Keuntungan"] = (
                    rekap["Pendapatan"]
                    - rekap["Pengeluaran"]
                )

                st.dataframe(rekap)

        # =================================
        # 6. REKAP BULANAN
        # =================================
        elif menu == "Rekap Bulanan":

            st.subheader("📆 Rekap Bulanan")

            pendapatan_df = pd.DataFrame(pendapatan_data)
            pengeluaran_df = pd.DataFrame(pengeluaran_data)

            if not pendapatan_df.empty:

                pendapatan_df["bulan"] = pd.to_datetime(
                    pendapatan_df["tanggal"]
                ).dt.to_period("M")

                pengeluaran_df["bulan"] = pd.to_datetime(
                    pengeluaran_df["tanggal"]
                ).dt.to_period("M")

                pendapatan_bulanan = pendapatan_df.groupby(
                    "bulan"
                )["total"].sum()

                pengeluaran_bulanan = pengeluaran_df.groupby(
                    "bulan"
                )["harga"].sum()

                rekap = pd.concat(
                    [pendapatan_bulanan, pengeluaran_bulanan],
                    axis=1
                ).fillna(0)

                rekap.columns = [
                    "Pendapatan",
                    "Pengeluaran"
                ]

                rekap["Keuntungan"] = (
                    rekap["Pendapatan"]
                    - rekap["Pengeluaran"]
                )

                st.dataframe(rekap)

        # =================================
        # 7. GRAFIK
        # =================================
        elif menu == "Grafik":

            st.subheader("📊 Grafik Keuangan")

            pendapatan_df = pd.DataFrame(pendapatan_data)

            if not pendapatan_df.empty:

                pendapatan_df["tanggal"] = pd.to_datetime(
                    pendapatan_df["tanggal"]
                )

                harian = pendapatan_df.groupby(
                    pendapatan_df["tanggal"].dt.day
                )["total"].sum()

                bulanan = pendapatan_df.groupby(
                    pendapatan_df["tanggal"].dt.month
                )["total"].sum()

                st.write("### Grafik Harian")

                st.bar_chart(harian)

                st.line_chart(harian)

                st.write("### Grafik Bulanan")

                st.bar_chart(bulanan)

                st.line_chart(bulanan)

    # =====================================
    # MENU KARYAWAN
    # =====================================
    elif st.session_state.role == "karyawan":

        menu = st.sidebar.radio(
            "Menu Karyawan",
            [
                "Menu Jualan",
                "Pengeluaran",
                "Pendapatan"
            ]
        )

        # =================================
        # MENU JUALAN
        # =================================
        if menu == "Menu Jualan":

            st.subheader("🍹 Daftar Menu")

            df = pd.DataFrame(menu_data)

            if not df.empty:
                st.dataframe(df, use_container_width=True)

        # =================================
        # PENGELUARAN
        # =================================
        elif menu == "Pengeluaran":

            st.subheader("💸 Tambah Pengeluaran")

            tanggal = st.date_input("Tanggal")

            barang = st.text_input("Membeli Apa")

            harga = st.number_input(
                "Harga",
                min_value=0,
                step=1000
            )

            if st.button("Tambah"):

                data = {
                    "tanggal": str(tanggal),
                    "barang": barang,
                    "harga": harga,
                    "user": st.session_state.username
                }

                pengeluaran_data.append(data)

                save_json(PENGELUARAN_FILE, pengeluaran_data)

                st.success("Pengeluaran berhasil ditambahkan")

        # =================================
        # PENDAPATAN
        # =================================
        elif menu == "Pendapatan":

            st.subheader("💰 Tambah Pendapatan")

            tanggal = st.date_input("Tanggal")

            pilihan_menu = [x["nama"] for x in menu_data]

            nama_menu = st.selectbox(
                "Pilih Menu",
                pilihan_menu
            )

            jumlah = st.number_input(
                "Jumlah",
                min_value=1
            )

            harga = 0

            for x in menu_data:

                if x["nama"] == nama_menu:

                    if jumlah >= 2:
                        harga = x["harga_2"]
                    else:
                        harga = x["harga_1"]

            total = harga * jumlah

            st.info(f"Total : Rp {total:,.0f}")

            if st.button("Tambah Pendapatan"):

                data = {
                    "tanggal": str(tanggal),
                    "menu": nama_menu,
                    "jumlah": jumlah,
                    "total": total
                }

                pendapatan_data.append(data)

                save_json(PENDAPATAN_FILE, pendapatan_data)

                st.success("Pendapatan berhasil ditambahkan")
