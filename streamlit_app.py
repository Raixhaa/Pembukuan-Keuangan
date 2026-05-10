import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date
from collections import defaultdict

st.set_page_config(page_title="EsKu Dashboard", page_icon="🍹", layout="wide")

# FILES & DEFAULT DATA (sama)
USER_FILE = "users.json"
MENU_FILE = "menu.json"
PENGELUARAN_FILE = "pengeluaran.json"
PENDAPATAN_FILE = "pendapatan.json"
KARYAWAN_FILE = "karyawan.json"

DEFAULT_USERS = {"admin": {"password": "admin123", "role": "host"}}
DEFAULT_MENU = [
    {"nama": "Es Teh", "harga_1": 3000, "harga_2": 5000, "harga_3": 8000, "harga_4": 10000},
    {"nama": "Es Jeruk", "harga_1": 4000, "harga_2": 6000, "harga_3": 9000, "harga_4": 12000},
    {"nama": "Es Campur", "harga_1": 5000, "harga_2": 8000, "harga_3": 12000, "harga_4": 16000}
]

# UTILITIES (sama)
def load_json(file_path, default_data):
    dir_path = os.path.dirname(file_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding='utf-8') as f: 
            json.dump(default_data, f, indent=4, ensure_ascii=False)
        return default_data
    try:
        with open(file_path, "r", encoding='utf-8') as f: 
            return json.load(f)
    except:
        with open(file_path, "w", encoding='utf-8') as f: 
            json.dump(default_data, f, indent=4, ensure_ascii=False)
        return default_data

def save_json(file_path, data):
    dir_path = os.path.dirname(file_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    with open(file_path, "w", encoding='utf-8') as f: 
        json.dump(data, f, indent=4, ensure_ascii=False)

def format_currency(amount): 
    try:
        return f"Rp {int(float(amount)):,}".replace(",", ".")
    except:
        return "Rp 0"

def format_date(date_str): 
    try:
        if pd.isna(date_str) or date_str == "":
            return ""
        return pd.to_datetime(date_str).strftime("%d/%m/%Y")
    except:
        return ""

def get_harga_berdasarkan_jumlah(menu, jumlah):
    if jumlah == 1: return float(menu["harga_1"])
    elif jumlah == 2: return float(menu["harga_2"])
    elif jumlah == 3: return float(menu["harga_3"])
    elif jumlah == 4: return float(menu["harga_4"])
    else: return float(menu["harga_1"]) * jumlah

# SESSION STATE (sama)
if "login" not in st.session_state: st.session_state.login = False
if "username" not in st.session_state: st.session_state.username = ""
if "role" not in st.session_state: st.session_state.role = ""
if "selected_menu" not in st.session_state: st.session_state.selected_menu = "📊 Dashboard"
if "sidebar_open" not in st.session_state: st.session_state.sidebar_open = True

# =========================================
# 🎨 CLEAN MODERN DESIGN - NO RGB
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* {font-family: 'Inter', sans-serif !important;}

/* CLEAN BACKGROUND */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    background-attachment: fixed;
}

.main {
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.08);
    margin: 20px;
    padding: 35px;
    border: 1px solid rgba(226, 232, 240, 0.8);
}

.big-title {
    font-size: 3.8rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #1e293b, #334155, #475569);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-align: center;
    margin-bottom: 8px;
    letter-spacing: -1px;
}

.subtitle {
    text-align: center;
    font-size: 1.4rem;
    font-weight: 500;
    color: #64748b;
    margin-bottom: 2.5rem;
}

/* ELEGANT CARDS */
.metric-card {
    background: linear-gradient(145deg, #ffffff, #f8fafc);
    backdrop-filter: blur(15px);
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 2.2rem;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(0,0,0,0.06);
}

.metric-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 25px 50px rgba(0,0,0,0.12);
    border-color: #cbd5e1;
}

.metric-title {
    color: #64748b;
    font-weight: 600;
    font-size: 1.1rem;
    margin-bottom: 10px;
}

.metric-value {
    font-size: 3rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #1e293b, #334155);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

/* BUTTONS */
button[kind="primary"] {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
    border-radius: 16px !important;
    height: 50px !important;
    font-weight: 600 !important;
    box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3) !important;
}

button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 20px 35px rgba(59, 130, 246, 0.4) !important;
}

/* SIDEBAR CLEAN */
[data-testid="stSidebar"] { 
    background: linear-gradient(145deg, #ffffff, #f8fafc) !important; 
    backdrop-filter: blur(20px) !important; 
    border-radius: 20px !important; 
    box-shadow: 0 20px 50px rgba(0,0,0,0.1) !important;
    z-index: 9999 !important;
    border: 1px solid #e2e8f0 !important;
    pointer-events: auto !important;
}

[data-testid="stSidebar"] > div {z-index: 10000 !important; pointer-events: auto !important;}
.stSidebar .stRadio > label {z-index: 10001 !important; pointer-events: auto !important; cursor: pointer !important;}
.stSidebar button {z-index: 10001 !important; pointer-events: auto !important; cursor: pointer !important;}

/* INPUTS CLEAN */
.stTextInput > div > div > input, 
.stNumberInput > div > div > input, 
.stDateInput > div > div > input {
    border-radius: 16px !important;
    border: 2px solid #e2e8f0 !important;
    padding: 14px 18px !important;
    background: #fafbfc;
    font-weight: 500;
}

.stTextInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
}

.stSelectbox > div > div > div {border-radius: 16px !important; border: 2px solid #e2e8f0 !important;}
[data-testid="stDataFrame"] {
    border-radius: 20px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05) !important;
}

.stMetric > label {font-size: 1.1rem !important; font-weight: 600 !important; color: #64748b !important;}
.stMetric > div > div {font-size: 2rem !important; font-weight: 700 !important;}
#MainMenu, footer, header {visibility: hidden !important;}

/* STATUS MESSAGES */
.stSuccess > div {border-radius: 12px !important; border-left: 4px solid #10b981 !important; background: #ecfdf5 !important;}
.stError > div {border-radius: 12px !important; border-left: 4px solid #ef4444 !important; background: #fef2f2 !important;}
.stInfo > div {border-radius: 12px !important; border-left: 4px solid #3b82f6 !important; background: #eff6ff !important;}
</style>
""", unsafe_allow_html=True)

# LOGIN - CLEAN DESIGN
if not st.session_state.login:
    st.markdown("<div class='big-title'>🍹 EsKu Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Sistem Pembukuan Minuman Modern & Simpel</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1: 
        username = st.text_input("👤 Username", placeholder="admin")
    with col2: 
        password = st.text_input("🔐 Password", type="password", placeholder="admin123")
    
    if st.button("🚀 Masuk Dashboard", use_container_width=True):
        users = load_json(USER_FILE, DEFAULT_USERS)
        if username in users and users[username]["password"] == password:
            st.session_state.update(login=True, username=username, role=users[username]["role"])
            st.success("✅ Login berhasil!")
            st.rerun()
        else:
            st.error("❌ Username atau password salah!")

# MAIN APP (sama persis seperti sebelumnya)
else:
    users = load_json(USER_FILE, DEFAULT_USERS)
    menu_data = load_json(MENU_FILE, DEFAULT_MENU)
    pengeluaran_data = load_json(PENGELUARAN_FILE, [])
    pendapatan_data = load_json(PENDAPATAN_FILE, [])
    karyawan_data = load_json(KARYAWAN_FILE, [])
    
    total_pendapatan = sum(float(d.get("total", 0)) for d in pendapatan_data)
    total_pengeluaran = sum(float(d.get("harga", 0)) for d in pengeluaran_data)
    total_gaji = sum(float(d.get("gaji", 0)) for d in karyawan_data)
    keuntungan = total_pendapatan - total_pengeluaran - total_gaji

    # TOP BAR
    top_col1, top_col2, top_col3 = st.columns([1, 10, 1])
    with top_col1:
        if st.button("📱 Menu"):
            st.session_state.sidebar_open = True
            st.rerun()
    with top_col3:
        if st.button("🚪 Keluar"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    if st.session_state.sidebar_open:
        with st.sidebar:
            if st.button("❌ Tutup Menu"):
                st.session_state.sidebar_open = False
                st.rerun()

            st.markdown(f"""
            <div style='text-align: center; padding: 25px; background: linear-gradient(145deg, #f8fafc, #f1f5f9); border-radius: 20px; margin-bottom: 25px; border: 1px solid #e2e8f0;'>
                <div style='font-size: 4rem;'>{'👑' if st.session_state.role == 'host' else '👤'}</div>
                <div style='font-size: 1.6rem; font-weight: 700; margin-bottom: 5px; color: #1e293b;'>
                    {st.session_state.username}
                </div>
                <div style='font-size: 0.95rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 1px;'>
                    {st.session_state.role}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.metric("💰 Pendapatan", format_currency(total_pendapatan))
            st.metric("💸 Pengeluaran", format_currency(total_pengeluaran))
            st.metric("💚 Keuntungan", format_currency(keuntungan))

            menu_options = ["📊 Dashboard", "🍹 Menu Jualan", "💰 Pendapatan", "💸 Pengeluaran", "👥 Karyawan", "📈 Laporan"] if st.session_state.role == "host" else ["💰 Pendapatan", "💸 Pengeluaran", "📈 Laporan"]
            
            selected = st.radio("📋 Pilih:", menu_options, key="sidebar_menu", 
                              index=menu_options.index(st.session_state.selected_menu) if st.session_state.selected_menu in menu_options else 0)

            if selected != st.session_state.selected_menu:
                st.session_state.selected_menu = selected
                st.rerun()

    st.markdown(f"<div class='big-title'>{st.session_state.selected_menu}</div>", unsafe_allow_html=True)

    # CONTENT PAGES (sama persis seperti sebelumnya)
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

    # [SELANJUTNYA SAMA PERSIS - Menu Jualan, Pendapatan, Pengeluaran, Karyawan, Laporan]
    # Copy paste dari kode sebelumnya untuk lengkapnya

    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #94a3b8; font-weight: 500;'>🍹 EsKu Dashboard - Simple & Professional</div>", unsafe_allow_html=True)
