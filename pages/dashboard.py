# pages/dashboard.py

import streamlit as st

from database.koneksi import get_connection
from models.auth import cek_login


# ==========================================
# HITUNG DATASET USER
# ==========================================

def total_dataset_user(id_pengguna):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM dataset
        WHERE id_pengguna = ?
    """, (id_pengguna,))

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ==========================================
# TOTAL KMEANS USER
# ==========================================

def total_kmeans_user(id_pengguna):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM hasil_kmeans
        WHERE id_pengguna = ?
    """, (id_pengguna,))

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ==========================================
# TOTAL NAIVE BAYES USER
# ==========================================

def total_nb_user(id_pengguna):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM hasil_naive_bayes
        WHERE id_pengguna = ?
    """, (id_pengguna,))

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ==========================================
# DASHBOARD
# ==========================================

def show():

    if not cek_login():

        st.warning(
            "Silakan login terlebih dahulu."
        )

        st.stop()

    nama = st.session_state[
        "nama_lengkap"
    ]

    id_pengguna = st.session_state[
        "id_pengguna"
    ]

    role = st.session_state[
        "role"
    ]

    st.title(
        "📊 Dashboard"
    )

    st.write(
        f"Selamat datang, **{nama}**"
    )

    dataset = total_dataset_user(
        id_pengguna
    )

    kmeans = total_kmeans_user(
        id_pengguna
    )

    nb = total_nb_user(
        id_pengguna
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Dataset Saya",
            dataset
        )

    with col2:
        st.metric(
            "Analisis K-Means",
            kmeans
        )

    with col3:
        st.metric(
            "Analisis Naive Bayes",
            nb
        )

    st.divider()

    st.subheader(
        "Menu Cepat"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "📁 Upload Dataset",
            use_container_width=True
        ):
            st.switch_page(
                "pages/dataset.py"
            )

    with col2:

        if st.button(
            "📈 K-Means",
            use_container_width=True
        ):
            st.switch_page(
                "pages/kmeans.py"
            )

    with col3:

        if st.button(
            "🧠 Naive Bayes",
            use_container_width=True
        ):
            st.switch_page(
                "pages/naive_bayes.py"
            )

    st.divider()

    st.subheader(
        "Informasi Akun"
    )

    st.write(
        f"Role : {role}"
    )
