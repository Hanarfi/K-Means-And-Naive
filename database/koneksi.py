# database/koneksi.py

import sqlite3
from pathlib import Path

# Lokasi database
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database.db"


def get_connection():
    """
    Membuat koneksi ke database SQLite
    dan mengaktifkan Foreign Key
    """

    try:
        conn = sqlite3.connect(DB_PATH)

        # Mengembalikan hasil query dalam bentuk dictionary
        conn.row_factory = sqlite3.Row

        # Mengaktifkan Foreign Key SQLite
        conn.execute("PRAGMA foreign_keys = ON")

        return conn

    except sqlite3.Error as e:
        print(f"Terjadi kesalahan koneksi database: {e}")
        return None


def close_connection(conn):
    """
    Menutup koneksi database
    """
    if conn:
        conn.close()
