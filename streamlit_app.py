# =====================================
# CARD STATISTIK
# =====================================

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">
            💰 Pendapatan
        </div>

        <div class="metric-value">
            Rp {total_pendapatan:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">
            💸 Pengeluaran
        </div>

        <div class="metric-value">
            Rp {total_pengeluaran:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">
            📈 Keuntungan
        </div>

        <div class="metric-value">
            Rp {keuntungan:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

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

        # =================================
        # TAMBAH MENU
        # =================================
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

            st.rerun()

        st.write("")

        # =================================
        # DAFTAR MENU
        # =================================
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
        # HAPUS MENU
        # =================================
        st.divider()

        st.subheader("🗑 Hapus Menu")

        if len(menu_data) > 0:

            hapus_menu = st.selectbox(
                "Pilih menu yang ingin dihapus",
                [x["nama"] for x in menu_data]
            )

            if st.button("❌ Hapus Menu"):

                menu_data = [
                    x for x in menu_data
                    if x["nama"] != hapus_menu
                ]

                save_json(
                    MENU_FILE,
                    menu_data
                )

                st.success(
                    "Menu berhasil dihapus"
                )

                st.rerun()

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
        total = 0

        for x in menu_data:

            if x["nama"] == nama_menu:

                # =========================
                # HITUNG PAKET
                # =========================
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

        st.info(
            f"💰 Total : Rp {total:,.0f}"
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

            st.rerun()
