# pages/register.py
import re
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

def validasi_password(password):
    """
    Validasi kekuatan password
    """

    if len(password) < 8:
        return (
            False,
            "Password minimal 8 karakter."
        )

    if not re.search(r"[A-Z]", password):
        return (
            False,
            "Password harus mengandung minimal 1 huruf besar."
        )

    if not re.search(r"\d", password):
        return (
            False,
            "Password harus mengandung minimal 1 angka."
        )

    return (
        True,
        "Valid"
    )


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

    from database.koneksi import DB_PATH

    print("=" * 50)
    print("DATABASE DIGUNAKAN:")
    print(DB_PATH)
    print("=" * 50)

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

    print("DATA YANG AKAN DISIMPAN:")
    print("Nama :", nama_lengkap)
    print("Username :", username)
    print("Email :", email)
    print("Role : user")

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
    print("COMMIT BERHASIL")
    cursor.execute("""
    SELECT COUNT(*)
    FROM pengguna
    """)
    
    total = cursor.fetchone()[0]
    
    print("TOTAL USER:", total)
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

        else:

            st.error(
                pesan
            )


if __name__ == "__main__":
    show()
