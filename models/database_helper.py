# ==========================================
# models/database_helper.py
# ==========================================

from database.koneksi import get_connection


# ==========================================
# EXECUTE QUERY
# ==========================================

def execute_query(query, params=()):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(query, params)

        conn.commit()

    finally:

        conn.close()


# ==========================================
# FETCH ONE
# ==========================================

def fetch_one(query, params=()):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(query, params)

        return cursor.fetchone()

    finally:

        conn.close()


# ==========================================
# FETCH ALL
# ==========================================

def fetch_all(query, params=()):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(query, params)

        return cursor.fetchall()

    finally:

        conn.close()


# ==========================================
# INSERT
# ==========================================

def insert(query, params=()):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(query, params)

        conn.commit()

        return cursor.lastrowid

    finally:

        conn.close()


# ==========================================
# UPDATE
# ==========================================

def update(query, params=()):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(query, params)

        conn.commit()

        return cursor.rowcount

    finally:

        conn.close()


# ==========================================
# DELETE
# ==========================================

def delete(query, params=()):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(query, params)

        conn.commit()

        return cursor.rowcount

    finally:

        conn.close()


# ==========================================
# CEK TABEL
# ==========================================

def table_exists(nama_tabel):

    hasil = fetch_one(

        """

        SELECT name

        FROM sqlite_master

        WHERE type='table'

        AND name=?

        """,

        (nama_tabel,)

    )

    return hasil is not None


# ==========================================
# TOTAL DATASET
# ==========================================

def get_total_dataset(id_pengguna):

    hasil = fetch_one(

        """

        SELECT COUNT(*)

        FROM dataset

        WHERE id_pengguna=?

        """,

        (id_pengguna,)

    )

    return hasil[0] if hasil else 0


# ==========================================
# TOTAL KMEANS
# ==========================================

def get_total_kmeans(id_pengguna):

    hasil = fetch_one(

        """

        SELECT COUNT(*)

        FROM hasil_kmeans

        WHERE id_pengguna=?

        """,

        (id_pengguna,)

    )

    return hasil[0] if hasil else 0


# ==========================================
# TOTAL NAIVE BAYES
# ==========================================

def get_total_naive_bayes(id_pengguna):

    hasil = fetch_one(

        """

        SELECT COUNT(*)

        FROM hasil_naive_bayes

        WHERE id_pengguna=?

        """,

        (id_pengguna,)

    )

    return hasil[0] if hasil else 0


# ==========================================
# TOTAL RIWAYAT
# ==========================================

def get_total_riwayat(id_pengguna):

    hasil = fetch_one(

        """

        SELECT COUNT(*)

        FROM riwayat_analisis

        WHERE id_pengguna=?

        """,

        (id_pengguna,)

    )

    return hasil[0] if hasil else 0

# ==========================================
# CEK NAMA DATASET
# ==========================================

def cek_nama_dataset(id_pengguna, nama_dataset):

    hasil = fetch_one(

        """

        SELECT id_dataset

        FROM dataset

        WHERE id_pengguna = ?

        AND nama_dataset = ?

        """,

        (

            id_pengguna,

            nama_dataset

        )

    )

    return hasil is not None


# ==========================================
# SIMPAN DATASET
# ==========================================

def simpan_dataset(

    id_pengguna,

    nama_dataset,

    deskripsi,

    nama_file,

    dataframe

):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        conn.execute("BEGIN")

        # -------------------------
        # Cek nama dataset
        # -------------------------

        if cek_nama_dataset(
            id_pengguna,
            nama_dataset
        ):

            raise Exception(
                "Nama dataset sudah digunakan."
            )

        # -------------------------
        # Simpan metadata dataset
        # -------------------------

        cursor.execute(

            """

            INSERT INTO dataset(

                id_pengguna,

                nama_dataset,

                deskripsi,

                nama_file,

                jumlah_data

            )

            VALUES (?, ?, ?, ?, ?)

            """,

            (

                id_pengguna,

                nama_dataset,

                deskripsi,

                nama_file,

                len(dataframe)

            )

        )

        id_dataset = cursor.lastrowid

        # -------------------------
        # Simpan data pasien
        # -------------------------

        for _, row in dataframe.iterrows():

            cursor.execute(

                """

                INSERT INTO data_pasien(

                    id_dataset,

                    no_rekam_medis,

                    jk,

                    tgl_masuk,

                    tgl_keluar,

                    lama_rawat,

                    kelas_rawatan,

                    usia,

                    cara_keluar,

                    ruang_rawat,

                    diagnosa_utama

                )

                VALUES

                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

                """,

                (

                    id_dataset,

                    str(row["No. Rekam Medis"]),

                    row["JK"],

                    str(row["TGL MSK"]),

                    str(row["TGL KELUAR"]),

                    int(row["LD"]),

                    row["Kelas Rawatan"],

                    int(row["Usia"]),

                    row["Cara Keluar"],

                    row["Ruang Rawat"],

                    row["Diagnosa Utama"]

                )

            )

        conn.commit()

        return (

            True,

            id_dataset

        )

    except Exception as e:

        conn.rollback()

        return (

            False,

            str(e)

        )

    finally:

        conn.close()


# ==========================================
# SIMPAN DATA BOBOT
# ==========================================

def simpan_data_bobot(

    id_dataset,

    dataframe

):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        conn.execute("BEGIN")

        # -------------------------
        # Hapus data lama
        # -------------------------

        cursor.execute(

            """

            DELETE

            FROM data_pasien_bobot

            WHERE id_dataset = ?

            """,

            (id_dataset,)

        )

        # -------------------------
        # Ambil seluruh id_pasien
        # -------------------------

        cursor.execute(

            """

            SELECT id_pasien

            FROM data_pasien

            WHERE id_dataset = ?

            ORDER BY id_pasien

            """,

            (id_dataset,)

        )

        daftar_pasien = cursor.fetchall()

        if len(daftar_pasien) != len(dataframe):

            raise Exception(

                "Jumlah data pasien tidak sesuai."

            )

        # -------------------------
        # Simpan bobot
        # -------------------------

        for index, (_, row) in enumerate(

            dataframe.iterrows()

        ):

            id_pasien = daftar_pasien[index][0]

            cursor.execute(

                """

                INSERT INTO data_pasien_bobot(

                    id_dataset,

                    id_pasien,

                    jk,

                    lama_rawat,

                    kelas_rawatan,

                    usia,

                    cara_keluar,

                    ruang_rawat,

                    diagnosa_utama

                )

                VALUES

                (?, ?, ?, ?, ?, ?, ?, ?, ?)

                """,

                (

                    id_dataset,

                    id_pasien,

                    int(row["JK"]),

                    int(row["LD"]),

                    int(row["Kelas Rawatan"]),

                    int(row["Usia"]),

                    int(row["Cara Keluar"]),

                    int(row["Ruang Rawat"]),

                    int(row["Diagnosa Utama"])

                )

            )

        conn.commit()

        return True

    except Exception:

        conn.rollback()

        raise

    finally:

        conn.close()


# ==========================================
# DAFTAR DATASET USER
# ==========================================

def get_dataset_user(id_pengguna):

    return fetch_all(

        """

        SELECT

            id_dataset,

            nama_dataset,

            deskripsi,

            nama_file,

            jumlah_data,

            tanggal_upload

        FROM dataset

        WHERE id_pengguna = ?

        ORDER BY tanggal_upload DESC

        """,

        (id_pengguna,)

    )


# ==========================================
# DETAIL DATASET
# ==========================================

def get_detail_dataset(id_dataset):

    return fetch_one(

        """

        SELECT

            *

        FROM dataset

        WHERE id_dataset = ?

        """,

        (id_dataset,)

    )


# ==========================================
# DATA PASIEN BERDASARKAN DATASET
# ==========================================

def get_data_pasien(id_dataset):

    return fetch_all(

        """

        SELECT

            *

        FROM data_pasien

        WHERE id_dataset = ?

        ORDER BY id_pasien

        """,

        (id_dataset,)

    )


# ==========================================
# DATA BOBOT BERDASARKAN DATASET
# ==========================================

def get_data_bobot(id_dataset):

    return fetch_all(

        """

        SELECT

            *

        FROM data_pasien_bobot

        WHERE id_dataset = ?

        ORDER BY id_pasien

        """,

        (id_dataset,)

    )



# ==========================================
# HAPUS DATASET
# ==========================================

def hapus_dataset(id_dataset):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(

            """

            DELETE

            FROM dataset

            WHERE id_dataset = ?

            """,

            (id_dataset,)

        )

        conn.commit()

        return True, None

    except Exception as e:

        conn.rollback()

        return False, str(e)

    finally:

        conn.close()


# ==========================================
# RIWAYAT DATASET USER
# ==========================================

def get_riwayat_user(id_pengguna):

    return fetch_all(

        """

        SELECT

            r.id_riwayat,

            r.jenis_analisis,

            r.tanggal_analisis,

            d.nama_dataset

        FROM riwayat_analisis r

        JOIN dataset d

        ON r.id_dataset = d.id_dataset

        WHERE r.id_pengguna = ?

        ORDER BY r.tanggal_analisis DESC

        """,

        (id_pengguna,)

    )


# ==========================================
# PREVIEW DATASET
# ==========================================

def preview_dataset(id_dataset, limit=10):

    return fetch_all(

        """

        SELECT *

        FROM data_pasien

        WHERE id_dataset = ?

        LIMIT ?

        """,

        (

            id_dataset,

            limit

        )

    )


# ==========================================
# CEK HASIL KMEANS
# ==========================================

# def cek_hasil_kmeans(id_dataset):

#     hasil = fetch_one(

#         """

#         SELECT COUNT(*)

#         FROM hasil_kmeans

#         WHERE id_dataset = ?

#         """,

#         (id_dataset,)

#     )

#     return hasil[0] > 0


# ==========================================
# CEK HASIL NAIVE BAYES
# ==========================================

# def cek_hasil_naive_bayes(id_dataset):

#     hasil = fetch_one(

#         """

#         SELECT COUNT(*)

#         FROM hasil_naive_bayes

#         WHERE id_dataset = ?

#         """,

#         (id_dataset,)

#     )

#     return hasil[0] > 0
