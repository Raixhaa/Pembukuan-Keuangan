import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
from datetime import datetime

# =========================================
# KONFIGURASI HALAMAN
# =========================================
st.set_page_config(
    page_title="EsKu Dashboard",
    page_icon="🍹",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================
st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.main {
    background: linear-gradient(135deg,#eff6ff,#dbeafe);
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0f172a,#1e3a8a);
    padding-top: 20px;
}

[data-testid="stSidebar"] * {
    color: white;
}

/* TITLE */
.big-title {
    font-size: 52px;
    font-weight: 800;
    color: #0f172a;
    text-align: center;
}

.sub-title {
    text-align: center;
    color: #475569;
    font-size: 18px;
    margin-bottom: 30px;
}

/* LOGIN */
.login-box {
    background: white;
    padding: 40px;
    border-radius: 25px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.12);
}

/* CARD */
.metric-card {
    background: linear-gradient(135deg,#2563eb,#38bdf8);
    padding: 30px;
    border-radius: 25px;
    color: white;
    text-align: center;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.15);
    transition: 0.3s;
}

.metric-card:hover {
    transform: translateY(-5px);
}

.metric-title {
    font-size: 18px;
    opacity: 0.9;
}

.metric-value {
    font-size: 34px;
    font-weight: bold;
}

/* MENU CARD */
.menu-card {
    background: white;
    border-radius: 25px;
    padding: 25px;
    text-align: center;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.08);
    transition: 0.3s;
    margin-bottom: 25px;
}

.menu-card:hover {
    transform: scale(1.03);
}

.menu-image {
    font-size: 60px;
}

.menu-title {
    font-size: 26px;
    font-weight: bold;
    color: #0f172a;
}

.price {
    color: #2563eb;
    font-size: 30px;
    font-weight: bold;
}

.paket {
    background: #dbeafe;
    padding: 10px;
    border-radius: 12px;
    margin-top: 10px;
    color: #1e3a8a;
    font-weight: bold;
}

/* BUTTON */
.stButton>button {
    width: 100%;
    border-radius: 15px;
    height: 50px;
    border: none;
    background: linear-gradient(90deg,#2563eb,#38bdf8);
    color: white;
    font-size: 18px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.02);
}

/* INPUT */
.stTextInput input,
.stNumberInput input {
    border-radius: 12px !important;
}

/* TABLE */
[data-testid="stDataFrame"] {
    border-radius: 20px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# FILE DATABASE
# =========================================
USER_FILE = "users.json"
MENU_FILE = "menu.json"
PENGELUARAN_FILE = "pengeluaran.json"
PENDAPATAN_FILE = "pendapatan.json"
KARYAWAN_FILE = "karyawan.json"

# =========================================
# DEFAULT HOST
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
# LOAD DATA
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

    st.markdown(
        """
        <div class='big-title'>
            🍹 EsKu Dashboard
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='sub-title'>
            Sistem Pembukuan Modern UMKM Minuman
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image(
        "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd",
        use_container_width=True
    )

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("<div class='login-box'>", unsafe_allow_html=True)

        st.subheader("🔐 Login")

        username = st.text_input("Username")
        password = st.text_input(
            "Password",
            type="password"
        )

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

        st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# DASHBOARD
# =========================================
else:

    st.sidebar.success(
        f"👤 {st.session_state.username}"
    )

    st.sidebar.info(
        f"Role : {st.session_state.role}"
    )

    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.rerun()

    # =====================================
    # HEADER
    # =====================================
    st.markdown(
        """
        <div class='big-title'>
            🍹 EsKu Dashboard
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='sub-title'>
            Sistem Pembukuan Modern Untuk Jualan Minuman
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image(
        "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd",
        use_container_width=True
    )

    # =====================================
    # HITUNG DATA
    # =====================================
    total_pendapatan = sum(
        item["total"]
        for item in pendapatan_data
    )

    total_pengeluaran = sum(
        item["harga"]
        for item in pengeluaran_data
    )

    keuntungan = (
        total_pendapatan
        - total_pengeluaran
    )

    # =====================================
    # CARD STATISTIK
    # =====================================
    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class='metric-card'>
                <div class='metric-title'>
                    💰 Pendapatan
                </div>

                <div class='metric-value'>
                    Rp {total_pendapatan:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class='metric-card'>
                <div class='metric-title'>
                    💸 Pengeluaran
                </div>

                <div class='metric-value'>
                    Rp {total_pengeluaran:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class='metric-card'>
                <div class='metric-title'>
                    📈 Keuntungan
                </div>

                <div class='metric-value'>
                    Rp {keuntungan:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # =====================================
    # MENU HOST
    # =====================================
    if st.session_state.role == "host":

        menu = st.sidebar.radio(
            "📋 Menu",
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
        # MENU JUALAN
        # =================================
        if menu == "Menu Jualan":

            st.subheader("🍹 Tambah Menu Minuman")

            col1, col2 = st.columns(2)

            with col1:

                nama = st.text_input(
                    "Nama Minuman"
                )

                harga_1 = st.number_input(
                    "Harga 1 Barang",
                    min_value=0,
                    step=1000
                )

            with col2:

                harga_2 = st.number_input(
                    "Harga Paket 2 Barang",
                    min_value=0,
                    step=1000
                )

            if st.button("➕ Tambah Menu"):

                data = {
                    "nama": nama,
                    "harga_1": harga_1,
                    "harga_2": harga_2
                }

                menu_data.append(data)

                save_json(
                    MENU_FILE,
                    menu_data
                )

                st.success(
                    "Menu berhasil ditambahkan"
                )

            st.write("")
            st.subheader("📋 Daftar Menu")

            if len(menu_data) > 0:

                cols = st.columns(3)

                emoji_list = [
                    "🥤",
                    "🍧",
                    "🧋",
                    "🍹",
                    "🧊",
                    "🥶"
                ]

                for i, item in enumerate(menu_data):

                    with cols[i % 3]:

                        emoji = emoji_list[
                            i % len(emoji_list)
                        ]

                        st.markdown(
                            f"""
                            <div class='menu-card'>

                                <div class='menu-image'>
                                    {emoji}
                                </div>

                                <div class='menu-title'>
                                    {item['nama']}
                                </div>

                                <br>

                                <div class='price'>
                                    Rp {item['harga_1']:,.0f}
                                </div>

                                <div class='paket'>
                                    Paket 2 = Rp {item['harga_2']:,.0f}
                                </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

        # =================================
        # PENGELUARAN
        # =================================
        elif menu == "Pengeluaran":

            st.subheader("💸 Modal / Pengeluaran")

            tanggal = st.date_input("Tanggal")

            barang = st.text_input(
                "Membeli Apa"
            )

            harga = st.number_input(
                "Harga",
                min_value=0,
                step=1000
            )

            if st.button(
                "Tambah Pengeluaran"
            ):

                data = {
                    "tanggal": str(tanggal),
                    "barang": barang,
                    "harga": harga,
                    "user":
                    st.session_state.username
                }

                pengeluaran_data.append(data)

                save_json(
                    PENGELUARAN_FILE,
                    pengeluaran_data
                )

                st.success(
                    "Pengeluaran berhasil"
                )

            df = pd.DataFrame(
                pengeluaran_data
            )

            if not df.empty:
                st.dataframe(
                    df,
                    use_container_width=True
                )

        # =================================
        # PENDAPATAN
        # =================================
        elif menu == "Pendapatan":

            st.subheader("💰 Pendapatan")

            tanggal = st.date_input(
                "Tanggal"
            )

            pilihan_menu = [
                x["nama"]
                for x in menu_data
            ]

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

            st.info(
                f"Total : Rp {total:,.0f}"
            )

            if st.button(
                "Tambah Pendapatan"
            ):

                data = {
                    "tanggal": str(tanggal),
                    "menu": nama_menu,
                    "jumlah": jumlah,
                    "total": total
                }

                pendapatan_data.append(data)

                save_json(
                    PENDAPATAN_FILE,
                    pendapatan_data
                )

                st.success(
                    "Pendapatan berhasil"
                )
