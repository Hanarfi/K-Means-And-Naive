# database/koneksi.py

import sqlite3
from pathlib import Path

# Lokasi database
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database.db"


def get_connection():
    """
    Membuat koneksi ke database SQLite
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
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
