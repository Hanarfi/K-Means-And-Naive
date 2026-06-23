# models/preprocessing.py

import pandas as pd


class Preprocessing:

    def __init__(self):
        pass

    # ==================================================
    # VALIDASI KOLOM
    # ==================================================

    def validasi_kolom(self, dataframe):

        kolom_wajib = [
            "No. Rekam Medis",
            "JK",
            "LD",
            "Kelas Rawatan",
            "Usia",
            "Cara Keluar",
            "Ruang Rawat",
            "Diagnosa Utama"
        ]

        kolom_tidak_ada = []

        for kolom in kolom_wajib:

            if kolom not in dataframe.columns:
                kolom_tidak_ada.append(kolom)

        return kolom_tidak_ada

    # ==================================================
    # MEMBERSIHKAN DATA
    # ==================================================

    def bersihkan_data(self, dataframe):

        df = dataframe.copy()

        # Hapus spasi awal dan akhir
        df.columns = df.columns.str.strip()

        # Hapus baris kosong
        df = df.dropna(how="all")

        # Hapus duplikat
        df = df.drop_duplicates()

        return df

    # ==================================================
    # NORMALISASI JK
    # ==================================================

    def normalisasi_jk(self, nilai):

        mapping = {
            "L": "Laki-Laki",
            "P": "Perempuan"
        }

        return mapping.get(
            str(nilai).strip().upper(),
            str(nilai).strip()
        )

    # ==================================================
    # KATEGORI LAMA RAWAT
    # ==================================================

    def kategori_lama_rawat(self, hari):

        try:

            hari = int(hari)

            if hari <= 10:
                return "1-10 Hari"

            elif hari <= 20:
                return "11-20 Hari"

            else:
                return ">20 Hari"

        except:
            return None

    # ==================================================
    # KATEGORI USIA
    # ==================================================

    def kategori_usia(self, usia):

        try:

            usia = int(usia)

            if usia <= 5:
                return "0-5 Tahun"

            elif usia <= 12:
                return "6-12 Tahun"

            else:
                return "13-18 Tahun"

        except:
            return None

    # ==================================================
    # NORMALISASI DIAGNOSA
    # ==================================================

    def normalisasi_diagnosa(self, diagnosa):

        diagnosa = str(diagnosa).strip().upper()

        mapping = {
            "KANKER": "Kanker",
            "PERNAFASAN": "Pernafasan",
            "PARU-PARU": "Paru-paru",
            "PENCERNAAN": "Pencernaan",
            "CAMPAK": "Campak"
        }

        return mapping.get(
            diagnosa,
            diagnosa.title()
        )

    # ==================================================
    # NORMALISASI RUANG RAWAT
    # ==================================================

    def normalisasi_ruang_rawat(self, ruang):

        ruang = str(ruang).strip().upper()

        mapping = {
            "SAKURA 1 (AKUT)": "Sakura 1 (Akut)",
            "SAKURA 2 (KRONIS)": "Sakura 2 (Kronis)",
            "LAVENDER 11 (HCU SCN)": "Lavender 11 (HCU SCN)"
        }

        return mapping.get(
            ruang,
            ruang.title()
        )
    def normalisasi_kelas_rawat(self, kelas):
        """
        Menyamakan format penulisan kelas rawatan
        """

        kelas = str(kelas).strip().upper()

        mapping = {
            "KELAS II": "Kelas II",
            "KELAS III": "Kelas III",
            "PICU": "PICU",
            "ISOLASI": "Isolasi"
        }

        return mapping.get(
            kelas,
            str(kelas).title()
        )

    # ==================================================
    # PROSES UTAMA PREPROCESSING
    # ==================================================

    def proses(self, dataframe):

        df = dataframe.copy()

        # Bersihkan data
        df = self.bersihkan_data(df)

        # Normalisasi JK
        df["JK"] = (
            df["JK"]
            .apply(self.normalisasi_jk)
        )

        # Kategori Lama Rawat
        df["LD_KATEGORI"] = (
            df["LD"]
            .apply(self.kategori_lama_rawat)
        )

        # Kategori Usia
        df["USIA_KATEGORI"] = (
            df["Usia"]
            .apply(self.kategori_usia)
        )

        # Normalisasi Kelas Rawatan
        df["Kelas Rawatan"] = (
            df["Kelas Rawatan"]
            .apply(self.normalisasi_kelas_rawat)
        )

        # Normalisasi Diagnosa
        df["Diagnosa Utama"] = (
            df["Diagnosa Utama"]
            .apply(self.normalisasi_diagnosa)
        )

        # Normalisasi Ruang Rawat
        df["Ruang Rawat"] = (
            df["Ruang Rawat"]
            .apply(self.normalisasi_ruang_rawat)
        )

        return df
    
    def validasi_diagnosa(self, dataframe):
        """
        Memastikan hanya diagnosa yang
        diperbolehkan dalam penelitian
        """

        diagnosa_valid = {
            "Kanker",
            "Pernafasan",
            "Paru-paru",
            "Pencernaan",
            "Campak"
        }

        diagnosa_dataset = set(
            dataframe["Diagnosa Utama"]
            .dropna()
            .unique()
        )

        diagnosa_tidak_valid = (
            diagnosa_dataset
            - diagnosa_valid
        )

        return list(diagnosa_tidak_valid)