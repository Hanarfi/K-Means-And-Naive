# database/init_db.py

import hashlib
from koneksi import get_connection


def hash_password(password):
    """
    Mengubah password menjadi SHA256
    """
    return hashlib.sha256(password.encode()).hexdigest()


def buat_tabel():
    conn = get_connection()
    cursor = conn.cursor()

    # =========================
    # TABEL PENGGUNA
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pengguna (
        id_pengguna INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_lengkap TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user',
        status_akun TEXT NOT NULL DEFAULT 'aktif',
        tanggal_daftar TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =========================
    # TABEL DATASET
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dataset (
        id_dataset INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pengguna INTEGER NOT NULL,
        nama_dataset TEXT NOT NULL,
        nama_file TEXT NOT NULL,
        tanggal_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_pengguna)
            REFERENCES pengguna(id_pengguna)
    )
    """)

    # =========================
    # TABEL DATA PASIEN
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS data_pasien (
        id_pasien INTEGER PRIMARY KEY AUTOINCREMENT,
        id_dataset INTEGER NOT NULL,
        no_rekam_medis TEXT NOT NULL,

        jenis_kelamin INTEGER,
        lama_rawat INTEGER,
        kelas_rawat INTEGER,
        usia INTEGER,
        cara_keluar INTEGER,
        ruang_rawat INTEGER,
        diagnosa_utama INTEGER,

        FOREIGN KEY (id_dataset)
            REFERENCES dataset(id_dataset)
    )
    """)

    # =========================
    # HASIL KMEANS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hasil_kmeans (
        id_hasil_kmeans INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pengguna INTEGER NOT NULL,
        id_dataset INTEGER NOT NULL,
        jumlah_cluster INTEGER NOT NULL,
        tanggal_proses TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (id_pengguna)
            REFERENCES pengguna(id_pengguna),

        FOREIGN KEY (id_dataset)
            REFERENCES dataset(id_dataset)
    )
    """)

    # =========================
    # DETAIL KMEANS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detail_kmeans (
        id_detail INTEGER PRIMARY KEY AUTOINCREMENT,
        id_hasil_kmeans INTEGER NOT NULL,
        no_rekam_medis TEXT NOT NULL,
        cluster INTEGER NOT NULL,
        label_cluster TEXT NOT NULL,

        FOREIGN KEY (id_hasil_kmeans)
            REFERENCES hasil_kmeans(id_hasil_kmeans)
    )
    """)

    # =========================
    # HASIL NAIVE BAYES
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hasil_naive_bayes (
        id_hasil_nb INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pengguna INTEGER NOT NULL,
        id_dataset INTEGER NOT NULL,

        akurasi REAL,
        presisi REAL,
        recall REAL,
        f1_score REAL,

        rasio_training INTEGER,
        rasio_testing INTEGER,

        tanggal_proses TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (id_pengguna)
            REFERENCES pengguna(id_pengguna),

        FOREIGN KEY (id_dataset)
            REFERENCES dataset(id_dataset)
    )
    """)

    # =========================
    # DETAIL NAIVE BAYES
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detail_naive_bayes (
        id_detail_nb INTEGER PRIMARY KEY AUTOINCREMENT,
        id_hasil_nb INTEGER NOT NULL,
        no_rekam_medis TEXT NOT NULL,
        hasil_prediksi TEXT NOT NULL,

        FOREIGN KEY (id_hasil_nb)
            REFERENCES hasil_naive_bayes(id_hasil_nb)
    )
    """)

    # =========================
    # BOBOT ATRIBUT
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bobot_atribut (
        id_bobot INTEGER PRIMARY KEY AUTOINCREMENT,
        atribut TEXT NOT NULL,
        kategori TEXT NOT NULL,
        bobot INTEGER NOT NULL
    )
    """)

    # =========================
    # LOG AKTIVITAS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS log_aktivitas (
        id_log INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pengguna INTEGER,
        aktivitas TEXT NOT NULL,
        waktu_aktivitas TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (id_pengguna)
            REFERENCES pengguna(id_pengguna)
    )
    """)

    conn.commit()
    conn.close()

    print("Semua tabel berhasil dibuat.")


def buat_admin_default():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM pengguna
    WHERE username = ?
    """, ("admin",))

    admin = cursor.fetchone()

    if not admin:
        password_hash = hash_password("Admin123!")

        cursor.execute("""
        INSERT INTO pengguna (
            nama_lengkap,
            username,
            email,
            password,
            role,
            status_akun
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Administrator",
            "admin",
            "admin@gmail.com",
            password_hash,
            "admin",
            "aktif"
        ))

        conn.commit()
        print("Admin default berhasil dibuat.")

    conn.close()


def isi_bobot_default():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM bobot_atribut")
    jumlah = cursor.fetchone()[0]

    if jumlah == 0:

        data_bobot = [

            # Jenis Kelamin
            ("jenis_kelamin", "Perempuan", 1),
            ("jenis_kelamin", "Laki-Laki", 2),

            # Lama Rawat
            ("lama_rawat", "1-10 Hari", 1),
            ("lama_rawat", "11-20 Hari", 2),
            ("lama_rawat", ">20 Hari", 3),

            # Kelas Rawat
            ("kelas_rawat", "Kelas II", 1),
            ("kelas_rawat", "Kelas III", 2),
            ("kelas_rawat", "PICU", 3),
            ("kelas_rawat", "Isolasi", 4),

            # Usia
            ("usia", "0-5 Tahun", 1),
            ("usia", "6-12 Tahun", 2),
            ("usia", "13-18 Tahun", 3),

            # Cara Keluar
            ("cara_keluar", "Dipulangkan", 1),
            ("cara_keluar", "Meninggal", 2),

            # Ruang Rawat
            ("ruang_rawat", "Sakura 1 (Akut)", 1),
            ("ruang_rawat", "Sakura 2 (Kronis)", 2),
            ("ruang_rawat", "Lavender 11 (HCU SCN)", 3),

            # Diagnosa
            ("diagnosa_utama", "Kanker", 1),
            ("diagnosa_utama", "Pernafasan", 2),
            ("diagnosa_utama", "Paru-paru", 3),
            ("diagnosa_utama", "Pencernaan", 4),
            ("diagnosa_utama", "Campak", 5)
        ]

        cursor.executemany("""
        INSERT INTO bobot_atribut (
            atribut,
            kategori,
            bobot
        )
        VALUES (?, ?, ?)
        """, data_bobot)

        conn.commit()

        print("Bobot atribut berhasil ditambahkan.")

    conn.close()


if __name__ == "__main__":

    print("=" * 50)
    print("INISIALISASI DATABASE")
    print("=" * 50)

    buat_tabel()
    buat_admin_default()
    isi_bobot_default()

    print("=" * 50)
    print("DATABASE SIAP DIGUNAKAN")
    print("=" * 50)
