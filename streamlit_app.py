# Streamlit Pembukuan Modern UI

Berikut contoh pengembangan tampilan agar website pembukuan terlihat lebih modern, profesional, dan menarik.

## Fitur Tampilan yang Ditambahkan

* Sidebar modern
* Warna gradient
* Card statistik
* Grafik interaktif
* Tampilan menu lebih rapi
* Emoji & icon
* CSS custom
* Layout responsive
* Tabel lebih elegan
* Header dashboard modern

---

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from datetime import datetime

# =====================================
# KONFIGURASI PAGE
# =====================================
st.set_page_config(
    page_title="Pembukuan Es Modern",
    page_icon="🍹",
    layout="wide"
)

# =====================================
# CUSTOM CSS
# =====================================
st.markdown(
    """
    <style>

    .main {
        background-color: #f5f7fb;
    }

    .title {
        font-size: 40px;
        font-weight: bold;
        color: #1f2937;
    }

    .subtitle {
        color: gray;
        margin-bottom: 30px;
    }

    .card {
        background: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    .metric-card {
        background: linear-gradient(135deg,#4facfe,#00f2fe);
        padding: 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.1);
    }

    .metric-title {
        font-size: 18px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================
# FILE DATABASE
# =====================================
MENU_FILE = "menu.json"
PENDAPATAN_FILE = "pendapatan.json"
PENGELUARAN_FILE = "pengeluaran.json"

# =====================================
# LOAD JSON
# =====================================
def load_json(file, default):

    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump(default, f)

    with open(file, "r") as f:
        return json.load(f)

menu_data = load_json(MENU_FILE, [])
pendapatan_data = load_json(PENDAPATAN_FILE, [])
pengeluaran_data = load_json(PENGELUARAN_FILE, [])

# =====================================
# HEADER
# =====================================
st.markdown(
    "<div class='title'>🍹 Dashboard Pembukuan Es</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Sistem pembukuan modern untuk usaha minuman dan UMKM</div>",
    unsafe_allow_html=True
)

# =====================================
# HITUNG DATA
# =====================================
pendapatan_total = 0
pengeluaran_total = 0

for x in pendapatan_data:
    pendapatan_total += x["total"]

for x in pengeluaran_data:
    pengeluaran_total += x["harga"]

keuntungan = pendapatan_total - pengeluaran_total

# =====================================
# CARD STATISTIK
# =====================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class='metric-card'>
            <div class='metric-title'>💰 Pendapatan</div>
            <div class='metric-value'>Rp {pendapatan_total:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class='metric-card'>
            <div class='metric-title'>💸 Pengeluaran</div>
            <div class='metric-value'>Rp {pengeluaran_total:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class='metric-card'>
            <div class='metric-title'>📈 Keuntungan</div>
            <div class='metric-value'>Rp {keuntungan:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# =====================================
# SIDEBAR
# =====================================
st.sidebar.title("📋 Menu")

menu = st.sidebar.radio(
    "Pilih Menu",
    [
        "Dashboard",
        "Menu Jualan",
        "Pendapatan",
        "Pengeluaran",
        "Grafik"
    ]
)

# =====================================
# DASHBOARD
# =====================================
if menu == "Dashboard":

    st.markdown("### 📊 Ringkasan Penjualan")

    if len(pendapatan_data) > 0:

        df = pd.DataFrame(pendapatan_data)

        st.dataframe(
            df,
            use_container_width=True
        )

# =====================================
# MENU JUALAN
# =====================================
elif menu == "Menu Jualan":

    st.markdown("### 🍹 Daftar Menu")

    if len(menu_data) > 0:

        df = pd.DataFrame(menu_data)

        st.dataframe(
            df,
            use_container_width=True
        )

    else:
        st.info("Belum ada menu jualan")

# =====================================
# PENDAPATAN
# =====================================
elif menu == "Pendapatan":

    st.markdown("### 💰 Data Pendapatan")

    if len(pendapatan_data) > 0:

        df = pd.DataFrame(pendapatan_data)

        st.dataframe(
            df,
            use_container_width=True
        )

    else:
        st.warning("Belum ada data pendapatan")

# =====================================
# PENGELUARAN
# =====================================
elif menu == "Pengeluaran":

    st.markdown("### 💸 Data Pengeluaran")

    if len(pengeluaran_data) > 0:

        df = pd.DataFrame(pengeluaran_data)

        st.dataframe(
            df,
            use_container_width=True
        )

    else:
        st.warning("Belum ada data pengeluaran")

# =====================================
# GRAFIK
# =====================================
elif menu == "Grafik":

    st.markdown("### 📈 Grafik Pendapatan")

    if len(pendapatan_data) > 0:

        df = pd.DataFrame(pendapatan_data)

        df["tanggal"] = pd.to_datetime(df["tanggal"])

        grafik = df.groupby(
            df["tanggal"].dt.day
        )["total"].sum().reset_index()

        fig = px.bar(
            grafik,
            x="tanggal",
            y="total",
            title="Pendapatan Harian"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        fig2 = px.line(
            grafik,
            x="tanggal",
            y="total",
            markers=True,
            title="Trend Pendapatan"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    else:
        st.info("Belum ada data grafik")

# =====================================
# FOOTER
# =====================================
st.write("")
st.write("")

st.markdown(
    "---"
)

st.caption("© 2026 Sistem Pembukuan Modern | Streamlit App")
```

---

## Install Library Tambahan

```bash
pip install streamlit pandas plotly
```

---

## Menjalankan Program

```bash
streamlit run app.py
```

---

## Hasil Tampilan

Tampilan website akan memiliki:

* Dashboard modern
* Warna lebih menarik
* Card statistik seperti aplikasi kasir profesional
* Grafik interaktif
* Sidebar modern
* Layout lebih clean
* UI lebih cocok untuk presentasi maupun UMKM
