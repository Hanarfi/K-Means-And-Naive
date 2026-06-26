import re
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
# VALIDASI PASSWORD
# ==========================================

def validasi_password(password):

    if len(password) < 8:

        return (
            False,
            "Password minimal 8 karakter."
        )

    if not re.search(r"[A-Z]", password):

        return (
            False,
            "Password harus memiliki minimal 1 huruf besar."
        )

    if not re.search(r"\d", password):

        return (
            False,
            "Password harus memiliki minimal 1 angka."
        )

    return (
        True,
        "Valid"
    )


# ==========================================
# VALIDASI EMAIL
# ==========================================

def validasi_email(email):

    pola = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    return re.match(
        pola,
        email
    ) is not None


# ==========================================
# REGISTER USER
# ==========================================

def register_user(

    nama_lengkap,

    username,

    email,

    password

):

    conn = get_connection()

    cursor = conn.cursor()

    # ===============================
    # CEK USERNAME
    # ===============================

    cursor.execute(
        """
        SELECT id_pengguna
        FROM pengguna
        WHERE username = ?
        """,
        (username,)
    )

    if cursor.fetchone():

        conn.close()

        return (
            False,
            "Username sudah digunakan."
        )

    # ===============================
    # CEK EMAIL
    # ===============================

    cursor.execute(
        """
        SELECT id_pengguna
        FROM pengguna
        WHERE email = ?
        """,
        (email,)
    )

    if cursor.fetchone():

        conn.close()

        return (
            False,
            "Email sudah digunakan."
        )

    # ===============================
    # INSERT USER
    # ===============================

    password_hash = hash_password(
        password
    )

    cursor.execute(
        """
        INSERT INTO pengguna
        (

            nama_lengkap,

            username,

            email,

            password_hash,

            role,

            status_akun

        )

        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (

            nama_lengkap,

            username,

            email,

            password_hash,

            "user",

            "aktif"

        )
    )

    conn.commit()

    conn.close()

    return (
        True,
        "Registrasi berhasil."
    )


# ==========================================
# HALAMAN REGISTER
# ==========================================

def show():

    st.title(
        "📝 Registrasi Akun"
    )

    st.write(
        "Silakan buat akun baru."
    )

    with st.form(
        "form_register"
    ):

        nama_lengkap = st.text_input(
            "Nama Lengkap"
        )

        username = st.text_input(
            "Username"
        )

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        konfirmasi = st.text_input(
            "Konfirmasi Password",
            type="password"
        )

        submit = st.form_submit_button(
            "Daftar",
            use_container_width=True
        )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Sudah punya akun?"
        ):

            st.session_state[
                "auth_page"
            ] = "login"

            st.rerun()

    # ======================================

    if submit:

        if not nama_lengkap:

            st.error(
                "Nama lengkap wajib diisi."
            )

            return

        if not username:

            st.error(
                "Username wajib diisi."
            )

            return

        if not email:

            st.error(
                "Email wajib diisi."
            )

            return

        if not validasi_email(
            email
        ):

            st.error(
                "Format email tidak valid."
            )

            return

        if not password:

            st.error(
                "Password wajib diisi."
            )

            return

        if password != konfirmasi:

            st.error(
                "Konfirmasi password tidak sesuai."
            )

            return

        valid, pesan = validasi_password(
            password
        )

        if not valid:

            st.error(
                pesan
            )

            return

        berhasil, pesan = register_user(

            nama_lengkap,

            username,

            email,

            password

        )

        if berhasil:

            st.success(
                pesan
            )

            st.session_state[
                "auth_page"
            ] = "login"

            st.rerun()

        else:

            st.error(
                pesan
            )
