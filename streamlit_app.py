import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date

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
def load_json(file_path, default_data):
    """Load JSON file with proper error handling and directory creation"""
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
    if dir_path: os.makedirs(dir_path, exist_ok=True)
    with open(file_path, "w", encoding='utf-8') as f: 
        json.dump(data, f, indent=4, ensure_ascii=False)

def format_currency(amount): 
    try: return f"Rp {int(float(amount)):,}".replace(",", ".")
    except: return "Rp 0"

def format_date(date_str): 
    try:
        if pd.isna(date_str) or date_str == "": return ""
        return pd.to_datetime(date_str).strftime("%d/%m/%Y")
    except: return ""

def get_harga_berdasarkan_jumlah(menu, jumlah):
    if jumlah == 1: return float(menu["harga_1"])
    elif jumlah == 2: return float(menu["harga_2"])
    elif jumlah == 3: return float(menu["harga_3"])
    elif jumlah == 4: return float(menu["harga_4"])
    else: return float(menu["harga_1"]) * jumlah

# EMOJI MAP
EMOJI_MAP = {
    "Dashboard": "📊",
    "Menu Jualan": "🍹",
    "Pendapatan": "💰",
    "Pengeluaran": "💸",
    "Karyawan": "👥",
    "Laporan": "📈"
}

# SESSION STATE - FIXED
if "login" not in st.session_state: 
    st.session_state.login = False
if "username" not in st.session_state: 
    st.session_state.username = ""
if "role" not in st.session_state: 
    st.session_state.role = ""
if "selected_menu" not in st.session_state: 
    st.session_state.selected_menu = "📊 Dashboard"
if "sidebar_open" not in st.session_state: 
    st.session_state.sidebar_open = False

# =========================================
# 🎨 FIXED CSS - MENU NAVIGASI BISA DIKLIK
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* {font-family: 'Inter', sans-serif !important;}

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
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    line-height: 1.1;
}

.big-title[data-emoji]:before {
    content: attr(data-emoji) " ";
    font-size: 3.8rem !important;
    font-weight: 400 !important;
    background: none !important;
    -webkit-background-clip: initial !important;
    -webkit-text-fill-color: #10b981 !important;
    margin-right: 12px;
    line-height: 1;
    flex-shrink: 0;
}

.subtitle {
    text-align: center;
    font-size: 1.4rem;
    font-weight: 500;
    color: #64748b;
    margin-bottom: 2.5rem;
}

.metric-card {
    background: linear-gradient(145deg, #ffffff, #f8fafc);
    backdrop-filter: blur(15px);
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 2.2rem;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(0,0,0,0.06);
    height: 160px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.metric-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 25px 50px rgba(0,0,0,0.12);
    border-color: #cbd5e1;
}

.metric-title {color: #64748b; font-weight: 600; font-size: 1.1rem; margin-bottom: 10px;}
.metric-value {
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #1e293b, #334155);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

/* FIXED SIDEBAR - MENU BISA DIKLIK */
[data-testid="stSidebar"] { 
    background: linear-gradient(145deg, #ffffff, #f8fafc) !important; 
    backdrop-filter: blur(20px) !important; 
    border-radius: 20px !important; 
    box-shadow: 0 20px 50px rgba(0,0,0,0.1) !important;
    border: 1px solid #e2e8f0 !important;
    z-index: 9999 !important;
    position: relative !important;
}

/* FIX RADIO BUTTON INTERACTIVITY */
.stRadio > div {
    z-index: 10001 !important;
    pointer-events: auto !important;
}

.stRadio > label {
    z-index: 10001 !important;
    pointer-events: auto !important;
    cursor: pointer !important;
    user-select: none !important;
}

.stRadio > div > label > div {
    pointer-events: auto !important;
    cursor: pointer !important;
}

/* FIX SIDEBAR BUTTONS */
[data-testid="stSidebar"] button {
    z-index: 10001 !important;
    pointer-events: auto !important;
    cursor: pointer !important;
    position: relative !important;
}

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

.stSuccess > div {border-radius: 12px !important; border-left: 4px solid #10b981 !important; background: #ecfdf5 !important;}
.stError > div {border-radius: 12px !important; border-left: 4px solid #ef4444 !important; background: #fef2f2 !important;}
.stInfo > div {border-radius: 12px !important; border-left: 4px solid #3b82f6 !important; background: #eff6ff !important;}
</style>
""", unsafe_allow_html=True)

# LOGIN PAGE
if not st.session_state.login:
    st.markdown("""
    <div class='big-title' data-emoji='🍹'>EsKu Dashboard</div>
    <div class='subtitle'>Sistem Pembukuan Minuman Modern & Simpel</div>
    """, unsafe_allow_html=True)
    
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

else:
    # FIXED: Load data ONCE after login
    users = load_json(USER_FILE, DEFAULT_USERS)
    menu_data = load_json(MENU_FILE, DEFAULT_MENU)
    pengeluaran_data = load_json(PENGELUARAN_FILE, [])
    pendapatan_data = load_json(PENDAPATAN_FILE, [])
    karyawan_data = load_json(KARYAWAN_FILE, [])
    
    # FIXED: Safe calculations
    total_pendapatan = sum(float(d.get("total", 0)) for d in pendapatan_data)
    total_pengeluaran = sum(float(d.get("harga", 0)) for d in pengeluaran_data)
    total_gaji = sum(float(d.get("gaji", 0)) for d in karyawan_data)
    keuntungan = total_pendapatan - total_pengeluaran - total_gaji

    # TOP BAR - FIXED
    top_col1, top_col2, top_col3 = st.columns([1, 10, 1])
    with top_col1:
        if not st.session_state.sidebar_open:
            if st.button("📱 Menu", key="open_menu_btn"):
                st.session_state.sidebar_open = True
                st.rerun()
    with top_col2:
        st.markdown(f"👋 Selamat datang, **{st.session_state.username}**!", unsafe_allow_html=True)
    with top_col3:
        if st.button("🚪 Keluar", key="logout_btn"):
            # FIXED: Proper logout reset
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.login = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.session_state.selected_menu = "📊 Dashboard"
            st.session_state.sidebar_open = False
            st.rerun()

    # FIXED SIDEBAR - MENU NAVIGASI
    if st.session_state.sidebar_open:
        with st.sidebar:
            # Tutup menu button
            if st.button("❌ Tutup Menu", key="close_menu"):
                st.session_state.sidebar_open = False
                st.rerun()

            # User info card
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

            # QUICK METRICS
            st.metric("💰 Pendapatan", format_currency(total_pendapatan))
            st.metric("💸 Pengeluaran", format_currency(total_pengeluaran))
            st.metric("💚 Keuntungan", format_currency(keuntungan))

            # FIXED MENU OPTIONS - Role-based and consistent
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
                    "📈 Laporan"
                ]
            
            # FIXED: Ensure selected_menu is always valid
            if st.session_state.selected_menu not in menu_options:
                st.session_state.selected_menu = menu_options[0]

            selected = st.radio("📋 Pilih Menu:", menu_options, 
                              key="sidebar_menu", 
                              index=menu_options.index(st.session_state.selected_menu))

            if selected != st.session_state.selected_menu:
                st.session_state.selected_menu = selected
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
            if nama.strip():  # Validate input
                menu_data.append({"nama": nama, "harga_1": float(harga1), "harga_2": float(harga2), "stok": 50})
                save_json(MENU_FILE, menu_data)
                st.success("✅ Menu ditambahkan!")
                st.rerun()
            else:
                st.error("❌ Nama menu tidak boleh kosong!")

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
            menu_pilih = st.selectbox("Menu", menu_options, key="menu_select")
        with col2: 
            jumlah = st.number_input("Jumlah", min_value=1, value=1, step=1, key="jumlah")
        with col3: 
            tanggal = st.date_input("Tanggal", value=date.today(), key="tanggal")
        
        if menu_pilih:
            try:
                menu = next(m for m in menu_data if m["nama"] == menu_pilih)
                
                # FIXED: Proper price calculation
                harga_1 = float(menu["harga_1"])
                harga_2 = float(menu["harga_2"])
                
                if jumlah == 1:
                    total = harga_1
                    ukuran = "1 Gelas"
                elif jumlah == 2:
                    total = harga_2
                    ukuran = "2 Gelas"
                else:
                    # For 3+ items: pairs of 2 + remaining singles
                    pairs = jumlah // 2
                    singles = jumlah % 2
                    total = (harga_2 * pairs) + (harga_1 * singles)
                    ukuran = f"{jumlah} Gelas"
                
                harga_per_item = total / jumlah
                
                st.success(f"💰 **Harga per gelas: {format_currency(harga_per_item)}**")
                st.success(f"💰 **Total ({jumlah} gelas): {format_currency(total)}**")
                
                if st.button("✅ Simpan Penjualan", use_container_width=True):
                    pendapatan_data.append({
                        "tanggal": tanggal.strftime("%Y-%m-%d"),
                        "menu": menu_pilih,
                        "ukuran": ukuran,
                        "jumlah": jumlah,
                        "harga_per_gelas": harga_per_item,
                        "total": total,
                        "oleh": st.session_state.username
                    })
                    save_json(PENDAPATAN_FILE, pendapatan_data)
                    st.success("✅ Penjualan tersimpan!")
                    st.rerun()
                    
            except StopIteration:
                st.error("❌ Menu tidak ditemukan!")
        else:
            st.info("👆 Pilih menu terlebih dahulu")

        st.header("📊 Riwayat Penjualan")
        if pendapatan_data:
            df = pd.DataFrame(pendapatan_data)
            df["tanggal"] = df["tanggal"].apply(format_date)
            df["total"] = df["total"].apply(format_currency)
            df["harga_per_gelas"] = df["harga_per_gelas"].apply(format_currency)
            
            # FIXED: Safe column handling
            display_cols = ["tanggal", "menu", "ukuran", "jumlah", "harga_per_gelas", "total", "oleh"]
            available_cols = [col for col in display_cols if col in df.columns]
            df_display = df[available_cols].copy()
            
            col_names = ["Tanggal", "Menu", "Ukuran", "Jumlah", "Harga/Gelas", "Total", "Oleh"]
            df_display.columns = col_names[:len(available_cols)]
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            st.info("📝 Belum ada data penjualan")

    elif st.session_state.selected_menu == "💸 Pengeluaran":
        st.header("➕ Input Pengeluaran")
        col1, col2, col3 = st.columns([1.5, 3, 1.5])
        with col1: tanggal = st.date_input("Tanggal", value=date.today(), key="exp_date")
        with col2: barang = st.text_input("Nama Barang", placeholder="Gula 5kg, Es Batu, dll", key="exp_barang")
        with col3: harga = st.number_input("Harga", min_value=0.0, value=0.0, step=1000.0, key="exp_harga")
        
        if st.button("💸 Simpan Pengeluaran", use_container_width=True):
            if barang.strip():
                pengeluaran_data.append({
                    "tanggal": tanggal.strftime("%Y-%m-%d"),
                    "barang": barang,
                    "harga": float(harga),
                    "oleh": st.session_state.username
                })
                save_json(PENGELUARAN_FILE, pengeluaran_data)
                st.success("✅ Pengeluaran tersimpan!")
                st.rerun()
            else:
                st.error("❌ Nama barang tidak boleh kosong!")

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
        with col1: nama = st.text_input("Nama Lengkap", key="emp_nama")
        with col2: username = st.text_input("Username", key="emp_username")
        with col3: password = st.text_input("Password", type="password", key="emp_password")
        with col4: gaji = st.number_input("Gaji/Bulan", min_value=0.0, value=1000000.0, key="emp_gaji")
        
        if st.button("👤 Buat Akun Karyawan", use_container_width=True):
            if username.strip() and username not in users:
                users[username] = {"password": password, "role": "karyawan", "nama": nama, "gaji": float(gaji)}
                karyawan_data.append({"username": username, "nama": nama, "gaji": float(gaji), "status": "aktif"})
                save_json(USER_FILE, users)
                save_json(KARYAWAN_FILE, karyawan_data)
                st.success(f"✅ Akun {username} berhasil dibuat!")
                st.rerun()
            elif not username.strip():
                st.error("❌ Username tidak boleh kosong!")
            else:
                st.error("❌ Username sudah ada!")

        st.header("👥 Daftar Karyawan")
        if karyawan_data:
            df = pd.DataFrame(karyawan_data)
            df["gaji"] = df["gaji"].apply(format_currency)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("📝 Belum ada karyawan")

    elif st.session_state.selected_menu in ["📈 Laporan", "📈 Laporan"]:
        st.header("📊 Laporan Keuangan")
        
        if pendapatan_data:
            try:
                df_pendapatan = pd.DataFrame(pendapatan_data)
                df_pendapatan['tanggal'] = pd.to_datetime(df_pendapatan['tanggal'], errors='coerce')
                df_pendapatan = df_pendapatan.dropna(subset=['tanggal'])
                
                if not df_pendapatan.empty:
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
                    st.warning("⚠️ Tidak ada data penjualan yang valid untuk laporan")
            except Exception as e:
                st.error(f"❌ Error membaca data laporan: {str(e)}")
        else:
            st.info("📝 Catat penjualan dulu untuk melihat laporan!")

    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #64748b; font-weight: 500;'>🍹 EsKu Dashboard Premium - UMKM Minuman Modern</div>", unsafe_allow_html=True)
