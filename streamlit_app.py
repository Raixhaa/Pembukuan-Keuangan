import streamlit as st
import json
import os

# =========================
# FILE PENYIMPANAN USER
# =========================
USER_FILE = "users.json"

# =========================
# DEFAULT HOST / ADMIN
# =========================
DEFAULT_HOST = {
    "admin": {
        "password": "admin123",
        "role": "host"
    }
}

# =========================
# LOAD USER
# =========================
def load_users():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump(DEFAULT_HOST, f)

    with open(USER_FILE, "r") as f:
        return json.load(f)

# =========================
# SAVE USER
# =========================
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

# =========================
# SESSION LOGIN
# =========================
if "login" not in st.session_state:
    st.session_state.login = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

users = load_users()

# =========================
# LOGIN PAGE
# =========================
if not st.session_state.login:

    st.title("🔐 Login Pembukuan")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username in users:

            if users[username]["password"] == password:

                st.session_state.login = True
                st.session_state.username = username
                st.session_state.role = users[username]["role"]

                st.success("Login berhasil!")
                st.rerun()

            else:
                st.error("Password salah")

        else:
            st.error("Username tidak ditemukan")

# =========================
# DASHBOARD
# =========================
else:

    st.sidebar.success(f"Login sebagai: {st.session_state.username}")
    st.sidebar.info(f"Role: {st.session_state.role}")

    # LOGOUT
    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()

    st.title("📒 Sistem Pembukuan Keuangan")

    # =========================
    # MENU HOST
    # =========================
    if st.session_state.role == "host":

        st.subheader("👨‍💼 Tambah Akun Karyawan")

        new_user = st.text_input("Username Baru")
        new_pass = st.text_input("Password Baru", type="password")

        if st.button("Tambah Karyawan"):

            if new_user in users:
                st.warning("Username sudah digunakan")

            elif new_user == "" or new_pass == "":
                st.warning("Isi semua data")

            else:

                users[new_user] = {
                    "password": new_pass,
                    "role": "karyawan"
                }

                save_users(users)

                st.success("Akun karyawan berhasil ditambahkan")

        st.divider()

        st.subheader("📋 Data User")

        for user, data in users.items():
            st.write(f"👤 {user} | Role: {data['role']}")

    # =========================
    # MENU KARYAWAN
    # =========================
    elif st.session_state.role == "karyawan":

        st.subheader("👨‍🔧 Dashboard Karyawan")
        st.write("Selamat datang di sistem pembukuan.")
