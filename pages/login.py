# pages/login.py

import streamlit as st
import hashlib

from database.koneksi import get_connection


# ==========================================
# HASH PASSWORD
# ==========================================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# ==========================================
# CEK LOGIN
# ==========================================

def login_user(username, password):

    conn = get_connection()

    cursor = conn.cursor()

    password_hash = hash_password(
        password
    )

    cursor.execute("""
        SELECT *
        FROM pengguna
        WHERE username = ?
        AND password_hash = ?
        AND status_akun = 'aktif'
    """, (
        username,
        password_hash
    ))

    user = cursor.fetchone()

    conn.close()

    return user


# ==========================================
# SIMPAN SESSION
# ==========================================

def simpan_session(user):

    st.session_state["login"] = True

    st.session_state["id_pengguna"] = (
        user["id_pengguna"]
    )

    st.session_state["nama_lengkap"] = (
        user["nama_lengkap"]
    )

    st.session_state["username"] = (
        user["username"]
    )

    st.session_state["role"] = (
        user["role"]
    )


# ==========================================
# LOGOUT
# ==========================================

def logout():

    keys = list(
        st.session_state.keys()
    )

    for key in keys:
        del st.session_state[key]


# ==========================================
# HALAMAN LOGIN
# ==========================================

def show():

    st.title(
        "🔐 Login Sistem"
    )

    st.write(
        "Masukkan username dan password."
    )

    with st.form("form_login"):

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        submit = st.form_submit_button(
            "Login"
        )

    if submit:

        if not username:

            st.error(
                "Username wajib diisi."
            )

            return

        if not password:

            st.error(
                "Password wajib diisi."
            )

            return

        user = login_user(
            username,
            password
        )

        if user:

            simpan_session(user)

            st.success(
                f"Selamat datang, {user['nama_lengkap']}"
            )

            st.rerun()

        else:

            st.error(
                "Username atau password salah."
            )


if __name__ == "__main__":
    show()
