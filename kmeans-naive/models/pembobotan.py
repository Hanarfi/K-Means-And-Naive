# models/pembobotan.py

from database.koneksi import get_connection


class Pembobotan:

    def __init__(self):
        self.conn = get_connection()

    def ambil_mapping_bobot(self, atribut):
        """
        Mengambil mapping bobot dari database

        Contoh:
        {
            'Laki-Laki': 2,
            'Perempuan': 1
        }
        """

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT kategori, bobot
            FROM bobot_atribut
            WHERE atribut = ?
        """, (atribut,))

        hasil = cursor.fetchall()

        mapping = {
            row["kategori"]: row["bobot"]
            for row in hasil
        }

        return mapping

    def validasi_kategori(self, dataframe):
        """
        Memastikan seluruh kategori
        tersedia pada tabel bobot_atribut
        """

        kolom_mapping = {
            "JK": "jenis_kelamin",
            "LD_KATEGORI": "lama_rawat",
            "Kelas Rawatan": "kelas_rawat",
            "USIA_KATEGORI": "usia",
            "Cara Keluar": "cara_keluar",
            "Ruang Rawat": "ruang_rawat",
            "Diagnosa Utama": "diagnosa_utama"
        }

        daftar_error = []

        for kolom, atribut in kolom_mapping.items():

            mapping = self.ambil_mapping_bobot(
                atribut
            )

            kategori_database = set(
                mapping.keys()
            )

            kategori_dataset = set(
                dataframe[kolom]
                .dropna()
                .unique()
            )

            kategori_tidak_ditemukan = (
                kategori_dataset
                - kategori_database
            )

            if kategori_tidak_ditemukan:

                daftar_error.append({
                    "kolom": kolom,
                    "kategori": list(
                        kategori_tidak_ditemukan
                    )
                })

        return daftar_error

    def transformasi_dataset(self, dataframe):
        """
        Mengubah kategori menjadi bobot
        """

        df = dataframe.copy()

        # Simpan data kategori asli

        df["jenis_kelamin_asli"] = df["JK"]
        df["lama_rawat_asli"] = df["LD_KATEGORI"]
        df["kelas_rawat_asli"] = df["Kelas Rawatan"]
        df["usia_asli"] = df["USIA_KATEGORI"]
        df["cara_keluar_asli"] = df["Cara Keluar"]
        df["ruang_rawat_asli"] = df["Ruang Rawat"]
        df["diagnosa_utama_asli"] = df["Diagnosa Utama"]

        # Mapping bobot

        map_jk = self.ambil_mapping_bobot(
            "jenis_kelamin"
        )

        map_ld = self.ambil_mapping_bobot(
            "lama_rawat"
        )

        map_kelas = self.ambil_mapping_bobot(
            "kelas_rawat"
        )

        map_usia = self.ambil_mapping_bobot(
            "usia"
        )

        map_keluar = self.ambil_mapping_bobot(
            "cara_keluar"
        )

        map_ruang = self.ambil_mapping_bobot(
            "ruang_rawat"
        )

        map_diagnosa = self.ambil_mapping_bobot(
            "diagnosa_utama"
        )

        # Konversi menjadi bobot

        df["jenis_kelamin"] = (
            df["JK"]
            .map(map_jk)
        )

        df["lama_rawat"] = (
            df["LD_KATEGORI"]
            .map(map_ld)
        )

        df["kelas_rawat"] = (
            df["Kelas Rawatan"]
            .map(map_kelas)
        )

        df["usia"] = (
            df["USIA_KATEGORI"]
            .map(map_usia)
        )

        df["cara_keluar"] = (
            df["Cara Keluar"]
            .map(map_keluar)
        )

        df["ruang_rawat"] = (
            df["Ruang Rawat"]
            .map(map_ruang)
        )

        df["diagnosa_utama"] = (
            df["Diagnosa Utama"]
            .map(map_diagnosa)
        )

        return df

    def ambil_fitur_kmeans(self, dataframe):
        """
        Mengambil fitur numerik
        untuk proses K-Means
        """

        return dataframe[
            [
                "jenis_kelamin",
                "lama_rawat",
                "kelas_rawat",
                "usia",
                "cara_keluar",
                "ruang_rawat",
                "diagnosa_utama"
            ]
        ]

    def tutup_koneksi(self):

        if self.conn:
            self.conn.close()