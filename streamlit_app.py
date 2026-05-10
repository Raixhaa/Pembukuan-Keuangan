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

/* BACKGROUND LEBIH CERAH */
.main {
    background: linear-gradient(
        135deg,
        #ffffff,
        #f0f9ff,
        #dbeafe
    );
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #2563eb,
        #38bdf8
    );
    padding-top: 20px;
}

[data-testid="stSidebar"] * {
    color: white;
}

/* TITLE */
.big-title {
    font-size: 52px;
    font-weight: 800;
    color: #1e3a8a;
    text-align: center;
}

.sub-title {
    text-align: center;
    color: #64748b;
    font-size: 18px;
    margin-bottom: 30px;
}

/* LOGIN */
.login-box {
    background: rgba(255,255,255,0.9);
    padding: 40px;
    border-radius: 25px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.08);
}

/* CARD */
.metric-card {
    background: linear-gradient(
        135deg,
        #38bdf8,
        #60a5fa
    );
    padding: 30px;
    border-radius: 25px;
    color: white;
    text-align: center;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.10);
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
    background: rgba(255,255,255,0.95);
    border-radius: 25px;
    padding: 25px;
    text-align: center;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.06);
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
    color: #1e3a8a;
}

.price {
    color: #2563eb;
    font-size: 30px;
    font-weight: bold;
}

.paket {
    background: #e0f2fe;
    padding: 10px;
    border-radius: 12px;
    margin-top: 10px;
    color: #0369a1;
    font-weight: bold;
}

/* BUTTON */
.stButton>button {
    width: 100%;
    border-radius: 15px;
    height: 50px;
    border: none;
    background: linear-gradient(
        90deg,
        #38bdf8,
        #60a5fa
    );
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
.stNumberInput input,
.stDateInput input {
    border-radius: 12px !important;
    border: 2px solid #bae6fd !important;
}

/* TABLE */
[data-testid="stDataFrame"] {
    border-radius: 20px;
    overflow: hidden;
    background: white;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# PERHITUNGAN TOTAL YANG BENAR
# =========================================

harga = 0
total = 0

for x in menu_data:

    if x["nama"] == nama_menu:

        # =================================
        # HITUNG PAKET
        # =================================

        if jumlah >= 2:

            paket = jumlah // 2
            sisa = jumlah % 2

            total = (
                paket * x["harga_2"]
            ) + (
                sisa * x["harga_1"]
            )

        else:

            total = (
                jumlah * x["harga_1"]
            )

# =========================================
# TAMPILKAN TOTAL
# =========================================

st.info(
    f"💰 Total Pendapatan : Rp {total:,.0f}"
)
