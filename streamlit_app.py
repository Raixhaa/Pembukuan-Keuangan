import streamlit as st
import pandas as pd
import json
import os
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
# FILE DATABASE
# =========================================
USER_FILE = "users.json"
MENU_FILE = "menu.json"
PENGELUARAN_FILE = "pengeluaran.json"
PENDAPATAN_FILE = "pendapatan.json"
KARYAWAN_FILE = "karyawan.json"

# =========================================
# DEFAULT DATA
# =========================================
DEFAULT_USERS = {
    "admin": {
        "password": "admin123",
        "role": "host"
    }
}

DEFAULT_KARYAWAN = []

# =========================================
# UTILITY FUNCTIONS
# =========================================
def load_json(file_path, default_data):
    """Load JSON file with default data if not exists"""
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(default_data, f, indent=4)
    
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        with open(file_path, "w") as f:
            json.dump(default_data, f, indent=4)
        return default_data

def save_json(file_path, data):
    """Save data to JSON file"""
    os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def format_currency(amount):
    """Format number to Indonesian currency"""
    return f"Rp {amount:,.0f}".replace(",", ".")

# =========================================
# LOAD DATA
# =========================================
users = load_json(USER_FILE, DEFAULT_USERS)
menu_data = load_json(MENU_FILE, [])
pengeluaran_data = load_json(PENGELUARAN_FILE, [])
pendapatan_data = load_json(PENDAPATAN_FILE, [])
karyawan_data = load_json(KARYAWAN_FILE, DEFAULT_KARYAWAN)

# =========================================
# SESSION STATE
# =========================================
if "login" not in st.session_state:
    st.session_state.login = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "selected_menu" not in st.session_state:
    st.session_state.selected_menu = "🍹 Menu Jualan"

# =========================================
# ENHANCED CSS - Termasuk Sidebar
# =========================================
st.markdown("""
<style>
/* 🌈 Light Mode - Warna Menarik & Elegan */
.main { 
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 25%, #ffecd2 50%, #fcb69f 75%, #a8e6cf 100%);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    color: #1a202c;
    min-height: 100vh;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Typography */
.big-title {
    font-size: 65px; font-weight: 900; 
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #f9ca24, #ff9ff3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center; 
    text-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 10px;
    animation: textGlow 3s ease-in-out infinite alternate;
}

@keyframes textGlow {
    from { filter: drop-shadow(0 0 5px rgba(255,107,107,0.5)); }
    to { filter: drop-shadow(0 0 20px rgba(79,205,196,0.8)); }
}

.sub-title {
    background: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 24px; font-weight: 600;
    text-align: center;
    margin-bottom: 40px;
}

/* Glass Cards */
.glass-card {
    background: rgba(255,255,255,0.95);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255,255,255,0.4);
    box-shadow: 0 25px 50px rgba(0,0,0,0.15);
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9));
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255,255,255,0.5);
    color: #1a202c;
    position: relative;
    overflow: hidden;
    padding: 40px;
    border-radius: 30px;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, rgba(255,107,107,0.1), rgba(79,205,196,0.1));
    opacity: 0;
    transition: opacity 0.3s ease;
}

.metric-card:hover::before { opacity: 1; }
.metric-card:hover { transform: translateY(-12px) scale(1.02); }

.metric-title { 
    color: #4a5568; font-weight: 600; font-size: 16px; 
    margin-bottom: 8px;
}
.metric-value { 
    font-size: 48px; font-weight: 900; 
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Menu Cards */
.menu-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.98), rgba(255,255,255,0.9));
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255,255,255,0.6);
    color: #1a202c;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    padding: 40px;
    border-radius: 30px;
    text-align: center;
}

.menu-card:hover {
    transform: translateY(-15px) scale(1.03);
    box-shadow: 0 35px 70px rgba(0,0,0,0.2);
}

.menu-image { 
    font-size: 80px; margin-bottom: 20px; 
    filter: drop-shadow(0 8px 16px rgba(0,0,0,0.1));
}
.menu-title { 
    font-size: 30px; font-weight: 800; 
    background: linear-gradient(45deg, #2d3748, #4a5568);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 15px;
}
.price { 
    font-size: 36px; font-weight: 900; 
    background: linear-gradient(45deg, #10b981, #059669, #047857);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.paket { 
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white; 
    border: none;
    padding: 15px 25px; 
    border-radius: 25px; 
    margin-top: 20px; 
    font-weight: 700; 
    font-size: 20px;
    box-shadow: 0 10px 25px rgba(59,130,246,0.3);
}

/* Inputs */
.stTextInput input, 
.stNumberInput input, 
.stSelectbox div, 
.stDateInput input {
    background: rgba(255,255,255,0.95) !important;
    border: 2px solid rgba(255,255,255,0.6) !important;
    border-radius: 15px !important;
    color: #1a202c !important;
    padding: 12px 16px !important;
    font-size: 16px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
}

.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: #4ecdc4 !important;
    box-shadow: 0 0 0 3px rgba(78,205,196,0.2) !important;
}

/* ENHANCED SIDEBAR BUTTONS */
button[kind="primary"] {
    background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1) !important;
    background-size: 200% 200% !important;
    animation: buttonGradient 3s ease infinite !important;
    box-shadow: 0 10px 25px rgba(255,107,107,0.3) !important;
    border: none !important;
    border-radius: 20px !important;
    height: 55px !important;
    color: white !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    margin-bottom: 12px !important;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    position: relative !important;
    overflow: hidden !important;
}

button[kind="primary"]:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 20px 40px rgba(255,107,107,0.4) !important;
}

@keyframes buttonGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9));
    backdrop-filter: blur(25px);
    border-right: 1px solid rgba(255,255,255,0.5);
    box-shadow: 5px 0 25px rgba(0,0,0,0.1);
}

[data-testid="stSidebar"] * { 
    color: #1a202c !important; 
}

/* Dataframe */
[data-testid="stDataFrame"] { 
    border-radius: 20px; 
    overflow: hidden; 
    border: 1px solid rgba(255,255,255,0.5);
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

/* Hide Streamlit elements */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* Success & Error Messages */
.stSuccess > div > div > div {
    background: linear-gradient(135deg, #10b981, #059669);
    border-radius: 15px;
    padding: 15px;
}
.stError > div > div > div {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    border-radius: 15px;
    padding: 15px;
}

/* Sidebar Floating Animation */
@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(180deg); }
}
</style>
""", unsafe_allow_html=True)

# =========================================
# LOGIN PAGE
# =========================================
if not st.session_state.login:
    st.markdown("<div class='big-title'>🍹 EsKu Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Sistem Pembukuan Modern UMKM Minuman</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='position: relative; display: flex; justify-content: center; margin: 50px 0;'>
        <div style='position: relative;'>
            <img src='https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?ixlib=rb-4.0.3&fit=crop&w=1200&q=80' 
                 style='width: 100%; max-width: 850px; border-radius: 35px; box-shadow: 0 35px 70px rgba(0,0,0,0.25);'>
            <div style='position: absolute; top: 20px; right: 20px; background: linear-gradient(135deg, #ff6b6b, #4ecdc4); padding: 15px 25px; border-radius: 25px; color: white; font-weight: 700; font-size: 18px; box-shadow: 0 10px 25px rgba(255,107,107,0.4);'>
                ✨ Dashboard Modern
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='glass-card' style='max-width: 500px; margin: 0 auto; padding: 60px; border-radius: 30px;'>
        <div style='font-size: 36px; font-weight: 800; text-align: center; margin-bottom: 35px; background: linear-gradient(45deg, #ff6b6b, #4ecdc4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🔐 Masuk ke Dashboard
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        username = st.text_input("👤 Username", placeholder="admin", key="login_username")
    with col2:
        password = st.text_input("🔑 Password", type="password", placeholder="admin123", key="login_password")
    
    if st.button("🚀 Masuk Sekarang", key="login_btn"):
        if username in users and users[username]["password"] == password:
            st.session_state.login = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.success("✅ Selamat datang di EsKu Dashboard!")
            st.rerun()
        else:
            st.error("❌ Username atau password salah!")
    
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# MAIN DASHBOARD dengan SUPER SIDEBAR
# =========================================
else:
    # Calculate totals dulu untuk sidebar
    total_pendapatan = sum(item.get("total", 0) for item in pendapatan_data)
    total_pengeluaran = sum(item.get("harga", 0) for item in pengeluaran_data)
    keuntungan = total_pendapatan - total_pengeluaran

    # 🔥 ENHANCED SIDEBAR - SUPER INTERAKTIF 🔥
    with st.sidebar:
        # Profile Card dengan animasi
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, rgba(255,107,107,0.15), rgba(78,205,196,0.15), rgba(69,183,209,0.15)); 
            padding: 30px; 
            border-radius: 25px; 
            margin-bottom: 25px; 
            border: 2px solid rgba(255,255,255,0.3);
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
            position: relative;
            overflow: hidden;
        '>
            <div style='position: absolute; top: -50%; right: -50%; width: 200%; height: 200%; 
                        background: radial-gradient(circle, rgba(255,107,107,0.1) 0%, transparent 70%);
                        animation: float 6s ease-in-out infinite;'>
            </div>
            <div style='font-size: 65px; margin-bottom: 20px; filter: drop-shadow(0 8px 16px rgba(255,107,107,0.3));'>👤</div>
            <div style='font-size: 28px; font-weight: 900; background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1); 
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px;'>
                {st.session_state.username}
            </div>
            <div style='font-size: 20px; font-weight: 700; color: #1a202c; 
                        background: linear-gradient(135deg, #3b82f6, #1d4ed8); 
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                {st.session_state.role.title()}
            </div>
            <div style='margin-top: 15px; padding: 8px 20px; background: rgba(255,255,255,0.3); 
                        border-radius: 20px; font-size: 14px; color: #4a5568; font-weight: 600;'>
                ✨ Dashboard Aktif
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Quick Stats Cards
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.9); padding: 25px; border-radius: 20px; margin-bottom: 25px; 
                    border: 1px solid rgba(255,255,255,0.5); box-shadow: 0 15px 35px rgba(0,0,0,0.08);'>
            <div style='font-size: 22px; font-weight: 800; text-align: center; margin-bottom: 20px;
                        background: linear-gradient(45deg, #10b981, #059669); 
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                📊
 Quick Stats
            </div>
            <div style='display: flex; flex-direction: column; gap: 15px;'>
                <div style='display: flex; justify-content: space-between; align-items: center; padding: 12px; 
                            background: linear-gradient(135deg, rgba(16,185,129,0.1), rgba(5,150,105,0.1)); 
                            border-radius: 15px;'>
                    <span style='font-size: 16px;'>💰 Pendapatan</span>
                    <span style='font-size: 20px; font-weight: 700; color: #10b981;'>
                        {format_currency(total_pendapatan)}
                    </span>
                </div>
                <div style='display: flex; justify-content: space-between; align-items:import streamlit as st
import pandas as pd
import json
import os
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
# FILE DATABASE
# =========================================
USER_FILE = "users.json"
MENU_FILE = "menu.json"
PENGELUARAN_FILE = "pengeluaran.json"
PENDAPATAN_FILE = "pendapatan.json"
KARYAWAN_FILE = "karyawan.json"

# =========================================
# DEFAULT DATA
# =========================================
DEFAULT_USERS = {
    "admin": {
        "password": "admin123",
        "role": "host"
    }
}

DEFAULT_KARYAWAN = []

# =========================================
# UTILITY FUNCTIONS
# =========================================
def load_json(file_path, default_data):
    """Load JSON file with default data if not exists"""
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(default_data, f, indent=4)
    
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        with open(file_path, "w") as f:
            json.dump(default_data, f, indent=4)
        return default_data

def save_json(file_path, data):
    """Save data to JSON file"""
    os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def format_currency(amount):
    """Format number to Indonesian currency"""
    return f"Rp {amount:,.0f}".replace(",", ".")

# =========================================
# LOAD DATA
# =========================================
users = load_json(USER_FILE, DEFAULT_USERS)
menu_data = load_json(MENU_FILE, [])
pengeluaran_data = load_json(PENGELUARAN_FILE, [])
pendapatan_data = load_json(PENDAPATAN_FILE, [])
karyawan_data = load_json(KARYAWAN_FILE, DEFAULT_KARYAWAN)

# =========================================
# SESSION STATE
# =========================================
if "login" not in st.session_state:
    st.session_state.login = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "selected_menu" not in st.session_state:
    st.session_state.selected_menu = "🍹 Menu Jualan"

# =========================================
# ENHANCED CSS - Termasuk Sidebar
# =========================================
st.markdown("""
<style>
/* 🌈 Light Mode - Warna Menarik & Elegan */
.main { 
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 25%, #ffecd2 50%, #fcb69f 75%, #a8e6cf 100%);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    color: #1a202c;
    min-height: 100vh;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Typography */
.big-title {
    font-size: 65px; font-weight: 900; 
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #f9ca24, #ff9ff3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center; 
    text-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 10px;
    animation: textGlow 3s ease-in-out infinite alternate;
}

@keyframes textGlow {
    from { filter: drop-shadow(0 0 5px rgba(255,107,107,0.5)); }
    to { filter: drop-shadow(0 0 20px rgba(79,205,196,0.8)); }
}

.sub-title {
    background: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 24px; font-weight: 600;
    text-align: center;
    margin-bottom: 40px;
}

/* Glass Cards */
.glass-card {
    background: rgba(255,255,255,0.95);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255,255,255,0.4);
    box-shadow: 0 25px 50px rgba(0,0,0,0.15);
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9));
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255,255,255,0.5);
    color: #1a202c;
    position: relative;
    overflow: hidden;
    padding: 40px;
    border-radius: 30px;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, rgba(255,107,107,0.1), rgba(79,205,196,0.1));
    opacity: 0;
    transition: opacity 0.3s ease;
}

.metric-card:hover::before { opacity: 1; }
.metric-card:hover { transform: translateY(-12px) scale(1.02); }

.metric-title { 
    color: #4a5568; font-weight: 600; font-size: 16px; 
    margin-bottom: 8px;
}
.metric-value { 
    font-size: 48px; font-weight: 900; 
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Menu Cards */
.menu-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.98), rgba(255,255,255,0.9));
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255,255,255,0.6);
    color: #1a202c;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    padding: 40px;
    border-radius: 30px;
    text-align: center;
}

.menu-card:hover {
    transform: translateY(-15px) scale(1.03);
    box-shadow: 0 35px 70px rgba(0,0,0,0.2);
}

.menu-image { 
    font-size: 80px; margin-bottom: 20px; 
    filter: drop-shadow(0 8px 16px rgba(0,0,0,0.1));
}
.menu-title { 
    font-size: 30px; font-weight: 800; 
    background: linear-gradient(45deg, #2d3748, #4a5568);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 15px;
}
.price { 
    font-size: 36px; font-weight: 900; 
    background: linear-gradient(45deg, #10b981, #059669, #047857);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.paket { 
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white; 
    border: none;
    padding: 15px 25px; 
    border-radius: 25px; 
    margin-top: 20px; 
    font-weight: 700; 
    font-size: 20px;
    box-shadow: 0 10px 25px rgba(59,130,246,0.3);
}

/* Inputs */
.stTextInput input, 
.stNumberInput input, 
.stSelectbox div, 
.stDateInput input {
    background: rgba(255,255,255,0.95) !important;
    border: 2px solid rgba(255,255,255,0.6) !important;
    border-radius: 15px !important;
    color: #1a202c !important;
    padding: 12px 16px !important;
    font-size: 16px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
}

.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: #4ecdc4 !important;
    box-shadow: 0 0 0 3px rgba(78,205,196,0.2) !important;
}

/* ENHANCED SIDEBAR BUTTONS */
button[kind="primary"] {
    background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1) !important;
    background-size: 200% 200% !important;
    animation: buttonGradient 3s ease infinite !important;
    box-shadow: 0 10px 25px rgba(255,107,107,0.3) !important;
    border: none !important;
    border-radius: 20px !important;
    height: 55px !important;
    color: white !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    margin-bottom: 12px !important;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    position: relative !important;
    overflow: hidden !important;
}

button[kind="primary"]:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 20px 40px rgba(255,107,107,0.4) !important;
}

@keyframes buttonGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9));
    backdrop-filter: blur(25px);
    border-right: 1px solid rgba(255,255,255,0.5);
    box-shadow: 5px 0 25px rgba(0,0,0,0.1);
}

[data-testid="stSidebar"] * { 
    color: #1a202c !important; 
}

/* Dataframe */
[data-testid="stDataFrame"] { 
    border-radius: 20px; 
    overflow: hidden; 
    border: 1px solid rgba(255,255,255,0.5);
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

/* Hide Streamlit elements */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* Success & Error Messages */
.stSuccess > div > div > div {
    background: linear-gradient(135deg, #10b981, #059669);
    border-radius: 15px;
    padding: 15px;
}
.stError > div > div > div {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    border-radius: 15px;
    padding: 15px;
}

/* Sidebar Floating Animation */
@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(180deg); }
}
</style>
""", unsafe_allow_html=True)

# =========================================
# LOGIN PAGE
# =========================================
if not st.session_state.login:
    st.markdown("<div class='big-title'>🍹 EsKu Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Sistem Pembukuan Modern UMKM Minuman</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='position: relative; display: flex; justify-content: center; margin: 50px 0;'>
        <div style='position: relative;'>
            <img src='https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?ixlib=rb-4.0.3&fit=crop&w=1200&q=80' 
                 style='width: 100%; max-width: 850px; border-radius: 35px; box-shadow: 0 35px 70px rgba(0,0,0,0.25);'>
            <div style='position: absolute; top: 20px; right: 20px; background: linear-gradient(135deg, #ff6b6b, #4ecdc4); padding: 15px 25px; border-radius: 25px; color: white; font-weight: 700; font-size: 18px; box-shadow: 0 10px 25px rgba(255,107,107,0.4);'>
                ✨ Dashboard Modern
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='glass-card' style='max-width: 500px; margin: 0 auto; padding: 60px; border-radius: 30px;'>
        <div style='font-size: 36px; font-weight: 800; text-align: center; margin-bottom: 35px; background: linear-gradient(45deg, #ff6b6b, #4ecdc4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🔐 Masuk ke Dashboard
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        username = st.text_input("👤 Username", placeholder="admin", key="login_username")
    with col2:
        password = st.text_input("🔑 Password", type="password", placeholder="admin123", key="login_password")
    
    if st.button("🚀 Masuk Sekarang", key="login_btn"):
        if username in users and users[username]["password"] == password:
            st.session_state.login = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.success("✅ Selamat datang di EsKu Dashboard!")
            st.rerun()
        else:
            st.error("❌ Username atau password salah!")
    
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# MAIN DASHBOARD dengan SUPER SIDEBAR
# =========================================
else:
    # Calculate totals dulu untuk sidebar
    total_pendapatan = sum(item.get("total", 0) for item in pendapatan_data)
    total_pengeluaran = sum(item.get("harga", 0) for item in pengeluaran_data)
    keuntungan = total_pendapatan - total_pengeluaran

    # 🔥 ENHANCED SIDEBAR - SUPER INTERAKTIF 🔥
    with st.sidebar:
        # Profile Card dengan animasi
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, rgba(255,107,107,0.15), rgba(78,205,196,0.15), rgba(69,183,209,0.15)); 
            padding: 30px; 
            border-radius: 25px; 
            margin-bottom: 25px; 
            border: 2px solid rgba(255,255,255,0.3);
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
            position: relative;
            overflow: hidden;
        '>
            <div style='position: absolute; top: -50%; right: -50%; width: 200%; height: 200%; 
                        background: radial-gradient(circle, rgba(255,107,107,0.1) 0%, transparent 70%);
                        animation: float 6s ease-in-out infinite;'>
            </div>
            <div style='font-size: 65px; margin-bottom: 20px; filter: drop-shadow(0 8px 16px rgba(255,107,107,0.3));'>👤</div>
            <div style='font-size: 28px; font-weight: 900; background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1); 
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px;'>
                {st.session_state.username}
            </div>
            <div style='font-size: 20px; font-weight: 700; color: #1a202c; 
                        background: linear-gradient(135deg, #3b82f6, #1d4ed8); 
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                {st.session_state.role.title()}
            </div>
            <div style='margin-top: 15px; padding: 8px 20px; background: rgba(255,255,255,0.3); 
                        border-radius: 20px; font-size: 14px; color: #4a5568; font-weight: 600;'>
                ✨ Dashboard Aktif
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Quick Stats Cards
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.9); padding: 25px; border-radius: 20px; margin-bottom: 25px; 
                    border: 1px solid rgba(255,255,255,0.5); box-shadow: 0 15px 35px rgba(0,0,0,0.08);'>
            <div style='font-size: 22px; font-weight: 800; text-align: center; margin-bottom: 20px;
                        background: linear-gradient(45deg, #10b981, #059669); 
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                📊
 Quick Stats
            </div>
            <div style='display: flex; flex-direction: column; gap: 15px;'>
                <div style='display: flex; justify-content: space-between; align-items: center; padding: 12px; 
                            background: linear-gradient(135deg, rgba(16,185,129,0.1), rgba(5,150,105,0.1)); 
                            border-radius: 15px;'>
                    <span style='font-size: 16px;'>💰 Pendapatan</span>
                    <span style='font-size: 20px; font-weight: 700; color: #10b981;'>
                        {format_currency(total_pendapatan)}
                    </span>
                </div>
                <div style='display: flex; justify-content: space-between; align-items:
