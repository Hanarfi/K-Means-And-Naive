import streamlit as st

from database.koneksi import get_connection


# ==========================================
# TOTAL DATASET
# ==========================================

def total_dataset(id_pengguna):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute("""

            SELECT COUNT(*)

            FROM dataset

            WHERE id_pengguna = ?

        """, (id_pengguna,))

        total = cursor.fetchone()[0]

    except:

        total = 0

    conn.close()

    return total


# ==========================================
# TOTAL KMEANS
# ==========================================

def total_kmeans(id_pengguna):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute("""

            SELECT COUNT(*)

            FROM hasil_kmeans

            WHERE id_pengguna = ?

        """, (id_pengguna,))

        total = cursor.fetchone()[0]

    except:

        total = 0

    conn.close()

    return total


# ==========================================
# TOTAL NAIVE BAYES
# ==========================================

def total_naive_bayes(id_pengguna):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute("""

            SELECT COUNT(*)

            FROM hasil_naive_bayes

            WHERE id_pengguna = ?

        """, (id_pengguna,))

        total = cursor.fetchone()[0]

    except:

        total = 0

    conn.close()

    return total


# ==========================================
# TOTAL RIWAYAT
# ==========================================

def total_riwayat(id_pengguna):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute("""

            SELECT COUNT(*)

            FROM riwayat_analisis

            WHERE id_pengguna = ?

        """, (id_pengguna,))

        total = cursor.fetchone()[0]

    except:

        total = 0

    conn.close()

    return total


# ==========================================
# DASHBOARD
# ==========================================

def show():

    nama = st.session_state["nama_lengkap"]

    id_pengguna = st.session_state["id_pengguna"]

    st.title("🏥 Dashboard")

    st.write(

        f"Selamat datang **{nama}**"

    )

    st.caption(

        "Sistem K-Means Clustering dan Naive Bayes"

    )

    st.divider()

    dataset = total_dataset(id_pengguna)

    kmeans = total_kmeans(id_pengguna)

    nb = total_naive_bayes(id_pengguna)

    riwayat = total_riwayat(id_pengguna)

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(

            "Dataset",

            dataset

        )

    with col2:

        st.metric(

            "K-Means",

            kmeans

        )

    with col3:

        st.metric(

            "Naive Bayes",

            nb

        )

    with col4:

        st.metric(

            "Riwayat",

            riwayat

        )

    st.divider()

    st.subheader("Informasi Sistem")

    st.info(

        f"""

Versi Sistem : 1.0

Role : {st.session_state['role'].title()}

Database : SQLite

Status : Aktif

        """

    )

    st.divider()

    st.subheader("Aktivitas")

    st.write(

        "Belum ada aktivitas yang ditampilkan."

    )
