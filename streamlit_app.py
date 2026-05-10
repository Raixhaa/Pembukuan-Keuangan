import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date
from collections import defaultdict

# =========================================
# KONFIGURASI
# =========================================
st.set_page_config(page_title="EsKu Dashboard", page_icon="🍹", layout="wide")

# FILES
USER_FILE = "users.json"
MENU_FILE = "menu.json"
PENGELUARAN_FILE = "pengeluaran.json"
PENDAPATAN_FILE = "pendapatan.json"
KARYAWAN_FILE = "karyawan.json"

# DEFAULT DATA
DEFAULT_USERS = {"admin": {"password": "admin123", "role": "host"}}
DEFAULT_MENU = [
    {"nama": "Es Teh", "harga_1": 3000, "harga_2": 5000, "stok": 50},
    {"nama": "Es Jeruk", "harga_1": 4000, "harga_2": 6000, "stok": 40},
    {"nama": "Es Campur", "harga_1": 5000, "harga_2": 8000, "stok": 30}
]

# UTILITIES
@st.cache_data
def load_json(file_path, default_data):
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)
        with open(file_path, "w") as f: 
            json.dump(default_data, f, indent=4)
    try:
        with open(file_path, "r") as f: 
            return json.load(f)
    except: 
        with open(file_path, "w") as f: 
            json.dump(default_data, f, indent=4)
        return default_data

def save_json(file_path, data):
    os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)
    with open(file_path, "w") as f: 
        json.dump(data, f, indent=4)

def format_currency(amount): 
    return f"Rp {int(amount):,}".replace(",", ".")

def format_date(date_str): 
    return pd.to_datetime(date_str).strftime("%d/%m/%Y") if date_str else ""

# LOAD DATA
users = load_json(USER_FILE, DEFAULT_USERS)
menu_data = load_json(MENU_FILE, DEFAULT_MENU)
pengeluaran_data = load_json(PENGELUARAN_FILE, [])
pendapatan_data = load_json(PENDAPATAN_FILE, [])
karyawan_data = load_json(KARYAWAN_FILE, [])

# SESSION STATE
if "login" not in st.session_state: 
    st.session_state.login = False
if "username" not in st.session_state: 
    st.session_state.username = ""
if "role" not in st.session_state: 
    st.session_state.role = ""
if "selected_menu" not in st.session_state: 
    st.session_state.selected_menu = "📊 Dashboard"
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True

# =========================================
# 🌈 PREMIUM CSS DESIGN
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
* {font-family: 'Poppins', sans-serif;}
html, body, [data-testid="stAppViewContainer"] {background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab); background-size: 400% 400%; animation: gradientBG 15s ease infinite;}
@keyframes gradientBG {0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.main {background: rgba(255,255,255,0.95); backdrop-filter: blur(20px); border-radius: 25px; box-shadow: 0 25px 50px rgba(0,0,0,0.2); margin: 20px; padding: 30px;}
.stAppViewContainer {padding-top: 2rem;}
.big-title {font-size: 4rem !important; font-weight: 900 !important; background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #f093fb, #f9ca24); -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; text-align: center !important; text-shadow: 0 10px 30px rgba(0,0,0,0.3);}
.metric-card {background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(248,250,252,0.8)); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.5); border-radius: 25px; padding: 2.5rem; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.15); transition: all 0.3s ease; position: relative; overflow: hidden;}
.metric-card:hover {transform: translateY(-10px) scale(1.02); box-shadow: 0 30px 60px rgba(0,0,0,0.25);}
.metric-card::before {content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent); transition: left 0.5s;}
.metric-card:hover::before {left: 100%;}
.metric-title {color: #64748b; font-weight: 600; font-size: 1.1rem; margin-bottom: 10px;}
.metric-value {font-size: 3rem !important; font-weight: 800 !important; background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1); -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;}
button[kind="primary"] {background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1) !important; border-radius: 20px !important; height: 50px !important; font-weight: 700 !important; box-shadow: 0 10px 30px rgba(255,107,107,0.4) !important;}
button[kind="primary"]:hover {transform: translateY(-2px) !important; box-shadow: 0 15px 40px rgba(255,107,107,0.5) !important;}
[data-testid="stSidebar"] {background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(255,255,255,0.85)) !important; backdrop-filter: blur(25px) !important; border-radius: 20px !important; box-shadow: 10px 0 40px rgba(0,0,0,0.1) !important;}
.stTextInput > div > div > input, .stNumberInput > div > div > input, .stDateInput > div > div > input {border-radius: 15px !important; border: 2px solid #e2e8f0 !important; padding: 12px 16px !important; background: rgba(255,255,255,0.9) !important;}
.stSelectbox > div > div > div, .stNumberInput > div > div > div {border-radius: 15px !important; border: 2px solid #e2e8f0 !important;}
[data-testid="stDataFrame"] {border-radius: 20px !important; border: 2px solid #e2e8f0 !important; box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;}
.stMetric > label {font-size: 1.1rem !important; font-weight: 600 !important; color: #64748b !important;}
.stMetric > div > div {font-size: 2rem !important; font-weight: 700 !important;}
#MainMenu, footer, header {visibility: hidden !important;}
</style>
""", unsafe_allow_html=True)

# =========================================
# LOGIN PAGE
# =========================================
if not st.session_state.login:
    st.markdown("<div class='big-title'>🍹 EsKu Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-size: 1.8rem; font-weight: 600; color: #64748b; margin-bottom: 3rem;'>Sistem Pembukuan Modern untuk UMKM Minuman</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1: 
        username = st.text_input("👤 Username", placeholder="admin")
    with col2: 
        password = st.text_input("🔑 Password", type="password", placeholder="admin123")
    
    if st.button("🚀 Masuk ke Dashboard", use_container_width=True):
        if username in users and users[username]["password"] == password:
            st.session_state.update(login=True, username=username, role=users[username]["role"])
            st.success("✅ Selamat datang!")
            st.rerun()
        else:
            st.error("❌ Username atau password salah!")

# =========================================
# MAIN DASHBOARD
# =========================================
else:
    # CALCULATE TOTALS
    total_pendapatan = sum(d.get("total", 0) for d in pendapatan_data)
    total_pengeluaran = sum(d.get("harga", 0) for d in pengeluaran_data)
    total_gaji = sum(d.get("gaji", 0) for d in karyawan_data)
    keuntungan = total_pendapatan - total_pengeluaran - total_gaji

    # TOP BAR - SIDEBAR TOGGLE
    top_col1, top_col2 = st.columns([1, 10])
    with top_col1:
        if not st.session_state.sidebar_open:
            if st.button("📱"):
                st.session_state.sidebar_open = True
                st.rerun()

    # SIDEBAR
    if st.session_state.sidebar_open:
        with st.sidebar:
            # CLOSE BUTTON
            if st.button("❌ Tutup Sidebar", use_container_width=True):
                st.session_state.sidebar_open = False
                st.rerun()

            # PROFILE CARD
            st.markdown(f"""
            <div style='text-align: center; padding: 25px;
            background: linear-gradient(135deg,
            rgba(255,107,107,0.2),
            rgba(78,205,196,0.2));
            border-radius: 20px;
            margin-bottom: 25px;'>

                <div style='font-size: 4rem;'>
                    {'👑' if st.session_state.role == 'host' else '👤'}
                </div>

                <div style='font-size: 1.6rem;
                font-weight: 800;
                margin-bottom: 5px;'>
                    {st.session_state.username}
                </div>

                <div style='font-size: 1rem;
                font-weight: 700;
                background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;'>
                    {st.session_state.role.upper()}
                </div>

            </div>
            """, unsafe_allow_html=True)

            # QUICK METRICS
            st.metric("💰 Pendapatan", format_currency(total_pendapatan))
            st.metric("💸 Pengeluaran", format_currency(total_pengeluaran))
            st.metric("💚 Keuntungan", format_currency(keuntungan))

            # MENU OPTIONS
            if st.session_state.role == "host":
                menu_options = [
                    "📊 Dashboard",
                    "🍹 Menu Jualan",
                    "💰 Pendapatan",
                    "💸 Pengeluaran",
                    "👥 Karyawan",
                    "📈 Laporan"
                ]
            else:
                menu_options = [
                    "💰 Pendapatan",
                    "💸 Pengeluaran",
                    "📈 Laporan Harian"
                ]

            selected = st.radio("📋 Pilih Menu:", menu_options, key="sidebar_menu", index=menu_options.index(st.session_state.selected_menu))

            if selected != st.session_state.selected_menu:
                st.session_state.selected_menu = selected
                st.rerun()

            # LOGOUT
            if st.button("🚪 Logout", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

    # MAIN CONTENT TITLE
    st.markdown(f"<div class='big-title'>{st.session_state.selected_menu}</div>", unsafe_allow_html=True)

    # CONTENT PAGES
    if st.session_state.selected_menu == "📊 Dashboard":
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-title'>💰 Total Pendapatan</div>
                <div class='metric-value'>{format_currency(total_pendapatan)}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-title'>💸 Total Pengeluaran</div>
                <div class='metric-value'>{format_currency(total_pengeluaran + total_gaji)}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-title'>💚 Keuntungan Bersih</div>
                <div class='metric-value'>{format_currency(keuntungan)}</div>
            </div>
            """, unsafe_allow_html=True)

    elif st.session_state.selected_menu == "🍹 Menu Jualan" and st.session_state.role == "host":
        st.header("➕ Tambah Menu Baru")
        col1, col2, col3 = st.columns(3)
        with col1: nama = st.text_input("Nama Menu")
        with col2: harga1 = st.number_input("Harga 1 Gelas", min_value=1000, value=3000)
        with col3: harga2 = st.number_input("Harga 2 Gelas", min_value=2000, value=5000)
        
        if st.button("💾 Tambah Menu", use_container_width=True):
            menu_data.append({"nama": nama, "harga_1": harga1, "harga_2": harga2, "stok": 50})
            save_json(MENU_FILE, menu_data)
            st.success("✅ Menu ditambahkan!")
            st.rerun()

        st.header("📋 Daftar Menu")
        if menu_data:
            df_menu = pd.DataFrame(menu_data)
            df_menu["Harga 1"] = df_menu["harga_1"].apply(format_currency)
            df_menu["Harga 2"] = df_menu["harga_2"].apply(format_currency)
            df_menu = df_menu[["nama", "Harga 1", "Harga 2", "stok"]]
            st.dataframe(df_menu, use_container_width=True, hide_index=True)

    elif st.session_state.selected_menu == "💰 Pendapatan":
        st.header("➕ Input Penjualan")
        col1, col2, col3 = st.columns(3)
        with col1: 
            menu_options = [""] + [m["nama"] for m in menu_data]
            menu_pilih = st.selectbox("Menu", menu_options)
        with col2: jumlah = st.number_input("Jumlah Gelas", min_value=1, value=1, step=1)
        with col3: tanggal = st.date_input("Tanggal", value=date.today())
        
        if menu_pilih:
            menu = next(m for m in menu_data if m["nama"] == menu_pilih)
            harga_per_gelas = menu["harga_1"]
            total = harga_per_gelas * jumlah
            st.success(f"💰 **Harga per gelas: {format_currency(harga_per_gelas)}**")
            st.success(f"💰 **Total ({jumlah} gelas): {format_currency(total)}**")
            
            if st.button("✅ Simpan Penjualan", use_container_width=True):
                pendapatan_data.append({
                    "tanggal": tanggal.strftime("%Y-%m-%d"),
                    "menu": menu_pilih,
                    "jumlah": jumlah,
                    "harga_per_gelas": harga_per_gelas,
                    "total": total,
                    "oleh": st.session_state.username
                })
                save_json(PENDAPATAN_FILE, pendapatan_data)
                st.success("✅ Penjualan tersimpan!")
                st.rerun()

        st.header("📊 Riwayat Penjualan")
        if pendapatan_data:
            df = pd.DataFrame(pendapatan_data)
            df["tanggal"] = df["tanggal"].apply(format_date)
            df["total"] = df["total"].apply(format_currency)
            df["harga_per_gelas"] = df["harga_per_gelas"].apply(format_currency)
            df = df[["tanggal", "menu", "jumlah", "harga_per_gelas", "total", "oleh"]]
            df.columns = ["Tanggal", "Menu", "Jumlah", "Harga/Gelas", "Total", "Oleh"]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("📝 Belum ada data penjualan")

    elif st.session_state.selected_menu == "💸 Pengeluaran":
        st.header("➕ Input Pengeluaran")
        col1, col2, col3 = st.columns([1.5, 3, 1.5])
        with col1: tanggal = st.date_input("Tanggal", value=date.today())
        with col2: barang = st.text_input("Nama Barang", placeholder="Gula 5kg, Es Batu, dll")
        with col3: harga = st.number_input("Harga", min_value=0.0, value=0.0, step=1000.0)
        
        if st.button("💸 Simpan Pengeluaran", use_container_width=True):
            pengeluaran_data.append({
                "tanggal": tanggal.strftime("%Y-%m-%d"),
                "barang": barang,
                "harga": float(harga),
                "oleh": st.session_state.username
            })
            save_json(PENGELUARAN_FILE, pengeluaran_data)
            st.success("✅ Pengeluaran tersimpan!")
            st.rerun()

        st.header("💰 Riwayat Pengeluaran")
        if pengeluaran_data:
            df = pd.DataFrame(pengeluaran_data)
            df["tanggal"] = df["tanggal"].apply(format_date)
            df["harga"] = df["harga"].apply(format_currency)
            df = df[["tanggal", "barang", "harga", "oleh"]]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("📝 Belum ada data pengeluaran")

    elif st.session_state.selected_menu == "👥 Karyawan" and st.session_state.role == "host":
        st.header("👑 Buat Akun Karyawan")
        col1, col2, col3, col4 = st.columns(4)
        with col1: nama = st.text_input("Nama Lengkap")
        with col2: username = st.text_input("Username")
        with col3: password = st.text_input("Password", type="password")
        with col4: gaji = st.number_input("Gaji/Bulan", min_value=0.0, value=1000000.0)
        
        if st.button("👤 Buat Akun Karyawan", use_container_width=True):
            if username not in users:
                users[username] = {"password": password, "role": "karyawan", "nama": nama, "gaji": gaji}
                karyawan_data.append({"username": username, "nama": nama, "gaji": gaji, "status": "aktif"})
                save_json(USER_FILE, users)
                save_json(KARYAWAN_FILE, karyawan_data)
                st.success(f"✅ Akun {username} berhasil dibuat!")
                st.rerun()
            else:
                st.error("❌ Username sudah ada!")

        st.header("👥 Daftar Karyawan")
        if karyawan_data:
            df = pd.DataFrame(karyawan_data)
            df["gaji"] = df["gaji"].apply(format_currency)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("📝 Belum ada karyawan")

    elif st.session_state.selected_menu in ["📈 Laporan", "📈 Laporan Harian"]:
        st.header("📊 Laporan Keuangan")
        
        if pendapatan_data:
            df_pendapatan = pd.DataFrame(pendapatan_data)
            df_pendapatan['tanggal'] = pd.to_datetime(df_pendapatan['tanggal'])
            
            # HARIAN
            daily = df_pendapatan.groupby(df_pendapatan['tanggal'].dt.date)['total'].sum()
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📅 Grafik Harian")
                st.line_chart(daily)
            with col2:
                st.subheader("📋 Tabel Harian")
                df_daily = daily.reset_index()
                df_daily['total'] = df_daily['total'].apply(format_currency)
                df_daily.columns = ['Tanggal', 'Pendapatan']
                st.dataframe(df_daily, use_container_width=True, hide_index=True)
            
            # BULANAN
            st.subheader("📊 Grafik Bulanan")
            monthly = df_pendapatan.groupby(df_pendapatan['tanggal'].dt.to_period('M'))['total'].sum()
            st.bar_chart(monthly)
            
            # SUMMARY
            st.subheader("💼 Ringkasan")
            summary_data = {
                "Kategori": ["Total Pendapatan", "Total Pengeluaran", "Total Gaji", "Keuntungan Bersih"],
                "Nominal": [format_currency(total_pendapatan), format_currency(total_pengeluaran), 
                           format_currency(total_gaji), format_currency(keuntungan)]
            }
            st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)
        else:
            st.info("📝 Catat penjualan dulu untuk melihat laporan!")

    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #64748b; font-weight: 500;'>🍹 EsKu Dashboard Premium - UMKM Minuman Modern</div>", unsafe_allow_html=True)
