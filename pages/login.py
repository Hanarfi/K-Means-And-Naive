import hashlib
import streamlit as st

from database.koneksi import get_connection


# ==========================================
# HASH PASSWORD
# ==========================================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# ==========================================
# AUTENTIKASI USER
# ==========================================

def autentikasi_user(
    username_email,
    password
):

    conn = get_connection()

    cursor = conn.cursor()

    password_hash = hash_password(
        password
    )

    cursor.execute(
        """
        SELECT
            id_pengguna,
            nama_lengkap,
            username,
            email,
            role,
            status_akun
        FROM pengguna
        WHERE
            (
                username = ?
                OR email = ?
            )
            AND password_hash = ?
        """,
        (
            username_email,
            username_email,
            password_hash
        )
    )

    user = cursor.fetchone()

    conn.close()

    if user is None:

        return (
            False,
            "Username atau password salah.",
            None
        )

    if user["status_akun"] != "aktif":

        return (
            False,
            "Akun tidak aktif.",
            None
        )

    return (
        True,
        "Login berhasil.",
        user
    )


# ==========================================
# HALAMAN LOGIN
# ==========================================

def show():

    st.title(
        "🔐 Login Sistem"
    )

    st.write(
        "Masukkan username atau email dan password."
    )

    with st.form(
        "form_login"
    ):

        username_email = st.text_input(
            "Username atau Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        login = st.form_submit_button(
            "Login"
        )

    col1, col2 = st.columns(2)

    with col2:

        if st.button(
            "Belum punya akun?"
        ):

            st.session_state[
                "auth_page"
            ] = "register"

            st.rerun()

    if login:

        if not username_email:

            st.error(
                "Username atau Email wajib diisi."
            )

            return

        if not password:

            st.error(
                "Password wajib diisi."
            )

            return

        berhasil, pesan, user = autentikasi_user(

            username_email,

            password

        )

        if not berhasil:

            st.error(
                pesan
            )

            return

        st.session_state["login"] = True

        st.session_state["id_pengguna"] = user["id_pengguna"]

        st.session_state["nama_lengkap"] = user["nama_lengkap"]

        st.session_state["role"] = user["role"]

        st.session_state["menu"] = "dashboard"

        st.success(
            "Login berhasil."
        )

        st.rerun()
