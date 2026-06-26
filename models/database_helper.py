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




# ==========================================
# SIMPAN DATASET + DATA PASIEN
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

        # Simpan metadata dataset
        cursor.execute(
            """
            INSERT INTO dataset
            (
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

        # Simpan seluruh data pasien
        for _, row in dataframe.iterrows():

            cursor.execute(
                """
                INSERT INTO data_pasien
                (
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

def simpan_data_bobot(id_dataset, dataframe):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        conn.execute("BEGIN")

        # Hapus data lama jika ada
        cursor.execute(
            """
            DELETE FROM data_pasien_bobot
            WHERE id_dataset = ?
            """,
            (id_dataset,)
        )

        # Ambil pasangan id_data sesuai urutan input
        cursor.execute(
            """
            SELECT id_data
            FROM data_pasien
            WHERE id_dataset = ?
            ORDER BY id_data
            """,
            (id_dataset,)
        )

        daftar_id = cursor.fetchall()

        if len(daftar_id) != len(dataframe):
            raise Exception(
                "Jumlah data tidak sesuai."
            )

        for index, (_, row) in enumerate(dataframe.iterrows()):

            id_data = daftar_id[index]["id_data"]

            cursor.execute(
                """
                INSERT INTO data_pasien_bobot
                (
                    id_dataset,
                    id_data,
                    jk,
                    lama_rawat,
                    kelas_rawatan,
                    usia,
                    cara_keluar,
                    ruang_rawat,
                    diagnosa_utama
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    id_dataset,
                    id_data,
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

    except Exception as e:

        conn.rollback()

        raise e

    finally:

        conn.close()


# ==========================================
# AMBIL DATASET USER
# ==========================================

def ambil_dataset_user(id_pengguna):

    return fetch_all(
        """
        SELECT *

        FROM dataset

        WHERE id_pengguna = ?

        ORDER BY id_dataset DESC
        """,
        (id_pengguna,)
    )


# ==========================================
# AMBIL SEMUA DATASET
# ==========================================

def ambil_semua_dataset():

    return fetch_all(
        """
        SELECT *

        FROM dataset

        ORDER BY id_dataset DESC
        """
    )


# ==========================================
# AMBIL SEMUA DATASET
# ==========================================

def ambil_semua_dataset():

    return fetch_all(
        """
        SELECT *

        FROM dataset

        ORDER BY id_dataset DESC
        """
    )


# ==========================================
# DETAIL DATASET
# ==========================================

def ambil_dataset(id_dataset):

    return fetch_one(
        """
        SELECT *

        FROM dataset

        WHERE id_dataset = ?
        """,
        (id_dataset,)
    )


# ==========================================
# DATA PASIEN
# ==========================================

def ambil_data_pasien(id_dataset):

    return fetch_all(
        """
        SELECT *

        FROM data_pasien

        WHERE id_dataset = ?

        ORDER BY id_data
        """,
        (id_dataset,)
    )


# ==========================================
# DATA BOBOT
# ==========================================

def ambil_data_bobot(id_dataset):

    return fetch_all(
        """
        SELECT *

        FROM data_pasien_bobot

        WHERE id_dataset = ?

        ORDER BY id_bobot
        """,
        (id_dataset,)
    )



# ==========================================
# HAPUS DATASET
# ==========================================

def hapus_dataset(id_dataset):

    return delete(
        """
        DELETE

        FROM dataset

        WHERE id_dataset = ?
        """,
        (id_dataset,)
    )


# ==========================================
# UPDATE DATASET
# ==========================================

def update_dataset(

    id_dataset,

    nama_dataset,

    deskripsi

):

    return update(
        """
        UPDATE dataset

        SET

            nama_dataset = ?,

            deskripsi = ?

        WHERE id_dataset = ?
        """,
        (
            nama_dataset,
            deskripsi,
            id_dataset
        )
    )


# ==========================================
# TOTAL PASIEN
# ==========================================

def get_total_pasien(id_dataset):

    hasil = fetch_one(
        """
        SELECT COUNT(*)

        FROM data_pasien

        WHERE id_dataset = ?
        """,
        (id_dataset,)
    )

    return hasil[0]
