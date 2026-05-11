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
DEFAULT_USERS = {"admin": {"password": "admin1234admin*", "role": "host"}}
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

# =========================================
# 🎨 FIXED CSS - MENU NAVIGASI BISA DIKLIK
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* {font-family: 'Inter', sans-serif !important;}

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #fff7ed 0%, #fef3c7 45%, #ede9fe 100%);
    color: #0f172a;
    min-height: 100vh;
}

.main {
    background: #ffffffdd;
    backdrop-filter: blur(18px);
    border-radius: 28px;
    box-shadow: 0 30px 80px #94a3b83d;
    margin: 24px;
    padding: 32px;
    border: 1px solid #94a3b47d;
}

.big-title {
    font-size: 3.5rem !important;
    font-weight: 800 !important;
    color: #0f172a !important;
    text-align: left;
    margin-bottom: 6px;
    letter-spacing: -1px;
    line-height: 1.05;
}

.big-title[data-emoji]:before {
    content: attr(data-emoji) " ";
    font-size: 3.5rem !important;
    font-weight: 400 !important;
    margin-right: 10px;
    color: #ec4899 !important;
}

.subtitle {
    text-align: left;
    font-size: 1.15rem;
    font-weight: 500;
    color: #475569;
    margin-bottom: 2rem;
}

.metric-card {
    background: linear-gradient(135deg, #fffffff0, #eff6fff0);
    border: 1px solid #3b82f626;
    border-radius: 22px;
    padding: 2rem;
    transition: all 0.25s ease;
    box-shadow: 0 18px 40px #94a3b828;
    height: 170px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 45px #94a3b83d;
    border-color: #3b82f64a;
}

.menu-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
    margin-top: 0.75rem;
}

.menu-card {
    background: #ffffff;
    border: 1px solid #bfdbfe;
    border-radius: 22px;
    padding: 1.35rem;
    transition: all 0.2s ease;
    box-shadow: 0 14px 30px #c7d2fe40;
}

.menu-card.selected {
    border-color: #0ea5e9;
    box-shadow: 0 18px 40px #38bdf84d;
}

.menu-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 18px 36px #c7d2fe60;
}

.menu-card-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 0.55rem;
}

.menu-card-price {
    font-size: 0.95rem;
    color: #475569;
    margin-bottom: 0.35rem;
}

.menu-card-selected-note {
    margin-top: 0.8rem;
    color: #0ea5e9;
    font-weight: 700;
}

.metric-title {color: #475569; font-weight: 600; font-size: 1rem; margin-bottom: 12px;}
.metric-value {
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    color: #0f172a !important;
}

[data-testid="stSidebar"] {
    background: #fffffff8 !important;
    backdrop-filter: blur(18px) !important;
    border-radius: 28px !important;
    box-shadow: 0 25px 75px #94a3b83d !important;
    border: 1px solid #94a3b43d !important;
    padding: 24px 18px 24px 18px !important;
}

[data-testid="stSidebar"] ::placeholder,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] span {
    color: #0f172a !important;
}

.stRadio > div,
.stRadio > label,
.stRadio > div > label > div,
[data-testid="stSidebar"] button {
    z-index: 10001 !important;
    pointer-events: auto !important;
    cursor: pointer !important;
}

button[kind="primary"] {
    background: linear-gradient(135deg, #38bdf8, #22c55e) !important;
    border-radius: 16px !important;
    height: 50px !important;
    font-weight: 700 !important;
    box-shadow: 0 12px 30px #10b98137 !important;
    color: #ffffff !important;
}

button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 18px 38px #10b98151 !important;
}

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stDateInput > div > div > input,
.stSelectbox > div > div > div {
    border-radius: 16px !important;
    border: 1px solid #94a3b44d !important;
    padding: 14px 18px !important;
    background: #ffffffea !important;
    color: #0f172a !important;
    font-weight: 500;
}

.stTextInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px #3b82f61f !important;
}

[data-testid="stDataFrame"] {
    border-radius: 22px !important;
    border: 1px solid #94a3b43d !important;
    box-shadow: 0 16px 40px #94a3b41f !important;
}

.stMetric > label {font-size: 1rem !important; font-weight: 600 !important; color: #475569 !important;}
.stMetric > div > div {font-size: 1.9rem !important; font-weight: 700 !important; color: #0f172a !important;}

#MainMenu, footer, header {visibility: hidden !important;}

.stSuccess > div {border-radius: 14px !important; border-left: 4px solid #16a34a !important; background: #a7f3d018 !important; color: #166534 !important;}
.stError > div {border-radius: 14px !important; border-left: 4px solid #dc2626 !important; background: #fee2e21e !important; color: #991b1b !important;}
.stInfo > div {border-radius: 14px !important; border-left: 4px solid #2563eb !important; background: #bfdbfe8c !important; color: #1e3a8a !important;}

.stSidebar .css-1v0mbdj.e16nr0p31 {
    padding-top: 0 !important;
}

.stSidebar .css-1umwnxn.egzxvld3 {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)

# LOGIN PAGE - CENTERED WITH LOGO
if not st.session_state.login:
    # CENTERED HEADER WITH LOGO
    st.markdown("""
    <div style='text-align: center; padding: 3rem 2rem;'>
        <div class='big-title' style='font-size: 4.2rem !important; margin-bottom: 1rem; display: inline-block;'>
            🍹 EsKu Dashboard
        </div>
        <div style='font-size: 1.4rem; font-weight: 600; color: #64748b; margin-bottom: 2.5rem; letter-spacing: 0.5px;'>
            Sistem Pembukuan Minuman Modern & Simpel
        </div>
        <div style='width: 300px; height: 300px; margin: 0 auto 3rem auto;'>
            <img src='https://raw.githubusercontent.com/Raixhaa/Pembukuan-Keuangan/main/Hijau%20Ceria%20Ilustratsi%20Modern%20Es%20Kuwut%20Logo_20260511_191409_0000.png' 
                 alt='EsKu Logo' style='width: 100%; height: 100%; object-fit: contain; border-radius: 20px; box-shadow: 0 12px 30px #10b98133;'>
        </div>
    </div>
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
    keuntungan_operasional = total_pendapatan - total_pengeluaran
    keuntungan_bersih = total_pendapatan - total_pengeluaran - total_gaji

    # TOP BAR - FIXED
    top_col1, top_col2, top_col3 = st.columns([1, 10, 1])
    with top_col1:
        st.markdown("")
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
            st.rerun()

    # NAVIGASI PANEL - SELALU TERLIHAT
    nav_col, content_col = st.columns([2.5, 9.5])
    with nav_col:
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
        st.metric("💚 Keuntungan", format_currency(keuntungan_operasional))

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

    with content_col:
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
                    <div class='metric-value'>{format_currency(total_pengeluaran)}</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-title'>💚 Keuntungan Bersih</div>
                    <div class='metric-value'>{format_currency(keuntungan_operasional)}</div>
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
                df_menu = df_menu[["nama", "Harga 1", "Harga 2"]]
                st.dataframe(df_menu, use_container_width=True, hide_index=True)

                st.subheader("🗑️ Hapus Menu")
                for i, item in enumerate(menu_data):
                    row_col1, row_col2, row_col3, row_col4 = st.columns([3, 2, 2, 1])
                    row_col1.write(f"**{item['nama']}**")
                    row_col2.write(format_currency(item['harga_1']))
                    row_col3.write(format_currency(item['harga_2']))
                    if row_col4.button("Hapus", key=f"delete_menu_{i}", use_container_width=True):
                        menu_data.pop(i)
                        save_json(MENU_FILE, menu_data)
                        st.success(f"✅ Menu '{item['nama']}' berhasil dihapus")
                        st.rerun()

        elif st.session_state.selected_menu == "💰 Pendapatan":
            st.header("➕ Input Penjualan")
            if "selected_menu_item" not in st.session_state:
                st.session_state.selected_menu_item = menu_data[0]["nama"] if menu_data else ""

            if menu_data:
                st.markdown("<div style='display:flex; align-items:center; gap:1rem; margin-bottom:0.75rem;'><div style='font-weight:700; color:#0f172a;'>Pilih Menu</div><div style='color:#475569;'>Klik kotak untuk memilih menu penjualan.</div></div>", unsafe_allow_html=True)
                for row_start in range(0, len(menu_data), 3):
                    row_cols = st.columns(3)
                    for j, m in enumerate(menu_data[row_start:row_start + 3]):
                        selected_item = st.session_state.selected_menu_item == m["nama"]
                        card_class = "menu-card selected" if selected_item else "menu-card"
                        with row_cols[j]:
                            st.markdown(f"""
                                <div class='{card_class}'>
                                    <div class='menu-card-title'>{m['nama']}</div>
                                    <div class='menu-card-price'>1 Gelas: {format_currency(m['harga_1'])}</div>
                                    <div class='menu-card-price'>2 Gelas: {format_currency(m['harga_2'])}</div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button("Pilih", key=f"menu_card_btn_{row_start + j}", use_container_width=True):
                                st.session_state.selected_menu_item = m["nama"]
                                st.rerun()
                menu_pilih = st.session_state.selected_menu_item
            else:
                menu_pilih = ""

            col1, col2 = st.columns([1.4, 1])
            with col1:
                jumlah = st.number_input("Jumlah", min_value=1, value=1, step=1, key="jumlah")
            with col2:
                tanggal = st.date_input("Tanggal", value=date.today(), key="tanggal")

            if menu_pilih:
                try:
                    menu = next(m for m in menu_data if m["nama"] == menu_pilih)
                    
                    harga_1 = float(menu["harga_1"])
                    harga_2 = float(menu["harga_2"])
                    
                    if jumlah == 1:
                        total = harga_1
                        ukuran = "1 Gelas"
                    elif jumlah == 2:
                        total = harga_2
                        ukuran = "2 Gelas"
                    else:
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
                st.info("👆 Tambahkan menu terlebih dahulu di Menu Jualan")

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

                st.subheader("🗑️ Hapus Penjualan")
                for i, item in enumerate(pendapatan_data):
                    tanggal = format_date(item.get('tanggal', ''))
                    total = format_currency(item.get('total', 0))
                    row_col1, row_col2, row_col3, row_col4 = st.columns([3, 2, 2, 1])
                    row_col1.write(f"**{tanggal} — {item.get('menu', '')}**")
                    row_col2.write(item.get('ukuran', ''))
                    row_col3.write(total)
                    if row_col4.button("Hapus", key=f"delete_sales_{i}", use_container_width=True):
                        pendapatan_data.pop(i)
                        save_json(PENDAPATAN_FILE, pendapatan_data)
                        st.success("✅ Data penjualan dihapus")
                        st.rerun()
            else:
                st.info("📝 Belum ada data penjualan")

        elif st.session_state.selected_menu == "💸 Pengeluaran":
            st.header("➕ Input Pengeluaran")
            col1, col2, col3, col4 = st.columns([1.5, 3, 1.5, 1.2])
            with col1: tanggal = st.date_input("Tanggal", value=date.today(), key="exp_date")
            with col2: barang = st.text_input("Nama Barang", placeholder="Gula 5kg, Es Batu, dll", key="exp_barang")
            with col3: jumlah_barang = st.text_input("Jumlah", placeholder="1 dus / 2 kg", key="exp_jumlah")
            with col4: harga = st.number_input("Harga", min_value=0.0, value=0.0, step=1000.0, key="exp_harga")
        
            if st.button("💸 Simpan Pengeluaran", use_container_width=True):
                if barang.strip() and jumlah_barang.strip():
                    pengeluaran_data.append({
                        "tanggal": tanggal.strftime("%Y-%m-%d"),
                        "barang": barang,
                        "jumlah": jumlah_barang.strip(),
                        "harga": float(harga),
                        "oleh": st.session_state.username
                    })
                    save_json(PENGELUARAN_FILE, pengeluaran_data)
                    st.success("✅ Pengeluaran tersimpan!")
                    st.rerun()
                elif not barang.strip():
                    st.error("❌ Nama barang tidak boleh kosong!")
                else:
                    st.error("❌ Jumlah tidak boleh kosong!")

            st.header("💰 Riwayat Pengeluaran")
            if pengeluaran_data:
                df = pd.DataFrame(pengeluaran_data)
                df["tanggal"] = df["tanggal"].apply(format_date)
                df["harga"] = df["harga"].apply(format_currency)
                if "jumlah" not in df.columns:
                    df["jumlah"] = 1
                df = df[["tanggal", "barang", "jumlah", "harga", "oleh"]]
                st.dataframe(df, use_container_width=True, hide_index=True)

                st.subheader("🗑️ Hapus Pengeluaran")
                for i, item in enumerate(pengeluaran_data):
                    tanggal = format_date(item.get('tanggal', ''))
                    row_col1, row_col2, row_col3, row_col4, row_col5 = st.columns([2.5, 1.5, 1.5, 1.5, 1])
                    row_col1.write(f"**{tanggal} — {item.get('barang', '')}**")
                    row_col2.write(f"Qty: {item.get('jumlah', 1)}")
                    row_col3.write(format_currency(item.get('harga', 0)))
                    row_col4.write(item.get('oleh', ''))
                    if row_col5.button("Hapus", key=f"delete_expense_{i}", use_container_width=True):
                        pengeluaran_data.pop(i)
                        save_json(PENGELUARAN_FILE, pengeluaran_data)
                        st.success("✅ Data pengeluaran dihapus")
                        st.rerun()
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

                st.subheader("🗑️ Hapus Karyawan")
                for i, item in enumerate(karyawan_data):
                    row_col1, row_col2, row_col3, row_col4 = st.columns([3, 2, 2, 1])
                    row_col1.write(f"**{item.get('nama', '')} ({item.get('username', '')})**")
                    row_col2.write(item.get('status', 'aktif'))
                    row_col3.write(format_currency(item.get('gaji', 0)))
                    if row_col4.button("Hapus", key=f"delete_employee_{i}", use_container_width=True):
                        username_to_delete = item.get('username', '')
                        if username_to_delete in users:
                            del users[username_to_delete]
                            save_json(USER_FILE, users)
                        karyawan_data.pop(i)
                        save_json(KARYAWAN_FILE, karyawan_data)
                        st.success(f"✅ Karyawan '{item.get('nama', '')}' berhasil dihapus")
                        st.rerun()
            else:
                st.info("📝 Belum ada karyawan")

        elif st.session_state.selected_menu in ["📈 Laporan", "📈 Laporan"]:
            st.header("📊 Laporan Keuangan")
        
            if pendapatan_data or pengeluaran_data:
                try:
                    df_pendapatan = pd.DataFrame(pendapatan_data)
                    df_pengeluaran = pd.DataFrame(pengeluaran_data)

                    if not df_pendapatan.empty and "tanggal" in df_pendapatan.columns:
                        df_pendapatan["tanggal"] = pd.to_datetime(df_pendapatan["tanggal"], errors="coerce")
                        df_pendapatan["total"] = pd.to_numeric(df_pendapatan.get("total", 0), errors="coerce").fillna(0)
                        df_pendapatan = df_pendapatan.dropna(subset=["tanggal"])
                    else:
                        df_pendapatan = pd.DataFrame({
                            "tanggal": pd.Series(dtype="datetime64[ns]"),
                            "total": pd.Series(dtype="float")
                        })

                    if not df_pengeluaran.empty and "tanggal" in df_pengeluaran.columns:
                        df_pengeluaran["tanggal"] = pd.to_datetime(df_pengeluaran["tanggal"], errors="coerce")
                        df_pengeluaran["harga"] = pd.to_numeric(df_pengeluaran.get("harga", 0), errors="coerce").fillna(0)
                        df_pengeluaran = df_pengeluaran.dropna(subset=["tanggal"])
                    else:
                        df_pengeluaran = pd.DataFrame({
                            "tanggal": pd.Series(dtype="datetime64[ns]"),
                            "harga": pd.Series(dtype="float")
                        })

                    # DAILY SUMMARY
                    daily_income = df_pendapatan.groupby(df_pendapatan["tanggal"].dt.date)["total"].sum()
                    daily_expense = df_pengeluaran.groupby(df_pengeluaran["tanggal"].dt.date)["harga"].sum()
                    daily_index = daily_income.index.union(daily_expense.index).sort_values()

                    daily_df = pd.DataFrame({
                        "Tanggal": daily_index,
                        "Pendapatan": daily_income.reindex(daily_index, fill_value=0).values,
                        "Pengeluaran": daily_expense.reindex(daily_index, fill_value=0).values,
                    })
                    daily_df["Keuntungan"] = daily_df["Pendapatan"] - daily_df["Pengeluaran"]
                    daily_df["Pendapatan"] = daily_df["Pendapatan"].astype(float)
                    daily_df["Pengeluaran"] = daily_df["Pengeluaran"].astype(float)
                    daily_df["Keuntungan"] = daily_df["Keuntungan"].astype(float)

                    st.subheader("📋 Tabel Harian")
                    df_daily_output = daily_df.copy()
                    df_daily_output["Pendapatan"] = df_daily_output["Pendapatan"].apply(format_currency)
                    df_daily_output["Pengeluaran"] = df_daily_output["Pengeluaran"].apply(format_currency)
                    df_daily_output["Keuntungan"] = df_daily_output["Keuntungan"].apply(format_currency)
                    st.dataframe(df_daily_output, use_container_width=True, hide_index=True)

                    st.subheader("📈 Grafik Harian")
                    daily_chart = daily_df.set_index("Tanggal")[['Pendapatan', 'Pengeluaran', 'Keuntungan']]
                    daily_chart.index = pd.to_datetime(daily_chart.index)
                    st.line_chart(daily_chart)

                    # MONTHLY SUMMARY
                    df_pendapatan["periode"] = df_pendapatan["tanggal"].dt.to_period("M")
                    df_pengeluaran["periode"] = df_pengeluaran["tanggal"].dt.to_period("M")
                    monthly_income = df_pendapatan.groupby("periode")["total"].sum()
                    monthly_expense = df_pengeluaran.groupby("periode")["harga"].sum()
                    monthly_index = monthly_income.index.union(monthly_expense.index).sort_values()

                    monthly_df = pd.DataFrame({
                        "Periode": monthly_index.astype(str),
                        "Pendapatan": monthly_income.reindex(monthly_index, fill_value=0).values,
                        "Pengeluaran": monthly_expense.reindex(monthly_index, fill_value=0).values,
                    })
                    monthly_df["Keuntungan"] = monthly_df["Pendapatan"] - monthly_df["Pengeluaran"]
                    monthly_df["Pendapatan"] = monthly_df["Pendapatan"].astype(float)
                    monthly_df["Pengeluaran"] = monthly_df["Pengeluaran"].astype(float)
                    monthly_df["Keuntungan"] = monthly_df["Keuntungan"].astype(float)

                    st.subheader("📋 Tabel Bulanan")
                    df_monthly_output = monthly_df.copy()
                    df_monthly_output["Pendapatan"] = df_monthly_output["Pendapatan"].apply(format_currency)
                    df_monthly_output["Pengeluaran"] = df_monthly_output["Pengeluaran"].apply(format_currency)
                    df_monthly_output["Keuntungan"] = df_monthly_output["Keuntungan"].apply(format_currency)
                    st.dataframe(df_monthly_output, use_container_width=True, hide_index=True)

                    st.subheader("📈 Grafik Bulanan")
                    monthly_chart = monthly_df.set_index("Periode")[['Pendapatan', 'Pengeluaran', 'Keuntungan']]
                    st.line_chart(monthly_chart)

                    if st.session_state.role == "host":
                        st.subheader("💼 Ringkasan")
                        if not monthly_index.empty:
                            latest_period = monthly_index.max()
                        else:
                            latest_period = pd.Period(date.today(), "M")
                        month_names = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                        summary_data = {
                            "Kategori": ["Bulan", "Tahun", "Pendapatan", "Pengeluaran", "Gaji Karyawan", "Keuntungan Bersih"],
                            "Nominal": [month_names[latest_period.month - 1], str(latest_period.year), format_currency(total_pendapatan), format_currency(total_pengeluaran), 
                                       format_currency(total_gaji), format_currency(keuntungan_bersih)]
                        }
                        st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)
                    else:
                        st.info("ℹ️ Ringkasan hanya ditampilkan untuk host. Laporan pendapatan, pengeluaran, dan keuntungan sudah menunjukkan nilai operasional tanpa potongan gaji.")
                except Exception as e:
                    st.error(f"❌ Error membaca data laporan: {str(e)}")
            else:
                st.info("📝 Catat penjualan atau pengeluaran dulu untuk melihat laporan!")

        st.markdown("---")
        st.markdown("<div style='text-align: center; color: #64748b; font-weight: 500;'>🍹 EsKu Dashboard Premium - UMKM Minuman Modern</div>", unsafe_allow_html=True)
