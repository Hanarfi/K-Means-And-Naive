from database.koneksi import get_connection


# ==========================================
# EXECUTE QUERY
# ==========================================

def execute_query(query, params=()):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(query, params)

    conn.commit()

    conn.close()


# ==========================================
# FETCH ONE
# ==========================================

def fetch_one(query, params=()):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(query, params)

    data = cursor.fetchone()

    conn.close()

    return data


# ==========================================
# FETCH ALL
# ==========================================

def fetch_all(query, params=()):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(query, params)

    data = cursor.fetchall()

    conn.close()

    return data


# ==========================================
# TOTAL DATASET
# ==========================================

def get_total_dataset(id_pengguna):

    try:

        hasil = fetch_one(
            """
            SELECT COUNT(*)

            FROM dataset

            WHERE id_pengguna = ?
            """,
            (id_pengguna,)
        )

        return hasil[0]

    except:

        return 0


# ==========================================
# TOTAL KMEANS
# ==========================================

def get_total_kmeans(id_pengguna):

    try:

        hasil = fetch_one(
            """
            SELECT COUNT(*)

            FROM hasil_kmeans

            WHERE id_pengguna = ?
            """,
            (id_pengguna,)
        )

        return hasil[0]

    except:

        return 0


# ==========================================
# TOTAL NAIVE BAYES
# ==========================================

def get_total_naive_bayes(id_pengguna):

    try:

        hasil = fetch_one(
            """
            SELECT COUNT(*)

            FROM hasil_naive_bayes

            WHERE id_pengguna = ?
            """,
            (id_pengguna,)
        )

        return hasil[0]

    except:

        return 0


# ==========================================
# TOTAL RIWAYAT
# ==========================================

def get_total_riwayat(id_pengguna):

    try:

        hasil = fetch_one(
            """
            SELECT COUNT(*)

            FROM riwayat_analisis

            WHERE id_pengguna = ?
            """,
            (id_pengguna,)
        )

        return hasil[0]

    except:

        return 0



# ==========================================
# CEK TABEL
# ==========================================

def table_exists(nama_tabel):

    hasil = fetch_one(
        """
        SELECT name

        FROM sqlite_master

        WHERE type='table'

        AND name = ?
        """,
        (nama_tabel,)
    )

    return hasil is not None


# ==========================================
# INSERT
# ==========================================

def insert(query, params=()):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(query, params)

    conn.commit()

    last_id = cursor.lastrowid

    conn.close()

    return last_id


# ==========================================
# UPDATE
# ==========================================

def update(query, params=()):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(query, params)

    conn.commit()

    jumlah = cursor.rowcount

    conn.close()

    return jumlah


# ==========================================
# DELETE
# ==========================================

def delete(query, params=()):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(query, params)

    conn.commit()

    jumlah = cursor.rowcount

    conn.close()

    return jumlah


