# pages/register.py

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
# SIMPAN USER BARU
# ==========================================

def register_user(
    nama_lengkap,
    username,
    email,
    password
):

    conn = get_connection()

    cursor = conn.cursor()

    # Cek username

    cursor.execute(
        """
        SELECT *
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

    # Cek email

    cursor.execute(
        """
        SELECT *
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
            "Daftar"
        )

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

        else:

            st.error(
                pesan
            )


if __name__ == "__main__":
    show()