import pandas as pd


# ==========================================
# KOLOM WAJIB
# ==========================================

KOLOM_WAJIB = [
    "No. Rekam Medis",
    "JK",
    "TGL MSK",
    "TGL KELUAR",
    "LD",
    "Kelas Rawatan",
    "Usia",
    "Cara Keluar",
    "Ruang Rawat",
    "Diagnosa Utama"
]


# ==========================================
# VALIDASI KOLOM
# ==========================================

def validasi_kolom(dataframe):

    kolom_hilang = [
        kolom
        for kolom in KOLOM_WAJIB
        if kolom not in dataframe.columns
    ]

    return kolom_hilang


# ==========================================
# MEMBERSIHKAN DATA
# ==========================================

def bersihkan_data(dataframe):

    df = dataframe.copy()

    df.columns = df.columns.str.strip()

    df = df.dropna(how="all")

    df = df.drop_duplicates()

    return df


# ==========================================
# NORMALISASI JK
# ==========================================

def normalisasi_jk(nilai):

    mapping = {

        "L": "Laki-Laki",

        "P": "Perempuan"

    }

    return mapping.get(

        str(nilai).strip().upper(),

        str(nilai).strip()

    )


# ==========================================
# KATEGORI LAMA RAWAT
# ==========================================

def kategori_lama_rawat(hari):

    try:

        hari = int(hari)

    except (TypeError, ValueError):

        return None

    if hari <= 10:

        return "1-10 Hari"

    elif hari <= 20:

        return "11-20 Hari"

    else:

        return ">20 Hari"


# ==========================================
# KATEGORI USIA
# ==========================================

def kategori_usia(usia):

    try:

        usia = int(usia)

    except (TypeError, ValueError):

        return None

    if usia <= 5:

        return "0-5 Tahun"

    elif usia <= 12:

        return "6-12 Tahun"

    else:

        return "13-18 Tahun"


# ==========================================
# NORMALISASI KELAS RAWATAN
# ==========================================

def normalisasi_kelas_rawatan(kelas):

    mapping = {

        "KELAS II": "Kelas II",

        "KELAS III": "Kelas III",

        "PICU": "PICU",

        "ISOLASI": "Isolasi"

    }

    return mapping.get(

        str(kelas).strip().upper(),

        str(kelas).strip().title()

    )


# ==========================================
# NORMALISASI DIAGNOSA
# ==========================================

def normalisasi_diagnosa(diagnosa):

    mapping = {

        "KANKER": "Kanker",

        "PERNAPASAN": "Pernapasan",

        "PARU-PARU": "Paru-paru",

        "PENCERNAAN": "Pencernaan",

        "CAMPAK": "Campak"

    }

    return mapping.get(

        str(diagnosa).strip().upper(),

        str(diagnosa).strip().title()

    )


# ==========================================
# NORMALISASI RUANG RAWAT
# ==========================================

def normalisasi_ruang_rawat(ruang):

    mapping = {

        "SAKURA 1 (AKUT)": "Sakura 1 (Akut)",

        "SAKURA 2 (KRONIS)": "Sakura 2 (Kronis)",

        "LAVENDER 11 (HCU SCN)": "Lavender 11 (HCU SCN)"

    }

    return mapping.get(

        str(ruang).strip().upper(),

        str(ruang).strip().title()

    )


# ==========================================
# VALIDASI DIAGNOSA
# ==========================================

def validasi_diagnosa(dataframe):

    diagnosa_valid = {

        "Kanker",

        "Pernapasan",

        "Paru-paru",

        "Pencernaan",

        "Campak"

    }

    diagnosa_dataset = set(

        dataframe["Diagnosa Utama"]

        .dropna()

        .unique()

    )

    return list(

        diagnosa_dataset

        - diagnosa_valid

    )


# ==========================================
# PREPROCESSING UTAMA
# ==========================================

def preprocessing_data(dataframe):

    df = bersihkan_data(dataframe)

    df["JK"] = df["JK"].apply(normalisasi_jk)

    df["LD"] = df["LD"].astype(int)

    df["Usia"] = df["Usia"].astype(int)

    df["LD_KATEGORI"] = df["LD"].apply(kategori_lama_rawat)

    df["USIA_KATEGORI"] = df["Usia"].apply(kategori_usia)

    df["Kelas Rawatan"] = (

        df["Kelas Rawatan"]

        .apply(normalisasi_kelas_rawatan)

    )

    df["Diagnosa Utama"] = (

        df["Diagnosa Utama"]

        .apply(normalisasi_diagnosa)

    )

    df["Ruang Rawat"] = (

        df["Ruang Rawat"]

        .apply(normalisasi_ruang_rawat)

    )

    return df
