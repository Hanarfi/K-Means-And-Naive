import pandas as pd


# ==========================================
# MASTER BOBOT
# ==========================================

BOBOT = {

    "JK": {

        "Perempuan": 1,

        "Laki-Laki": 2

    },

    "LD": {

        "1-10 Hari": 1,

        "11-20 Hari": 2,

        ">20 Hari": 3

    },

    "Kelas Rawatan": {

        "Kelas II": 1,

        "Kelas III": 2,

        "PICU": 3,

        "Isolasi": 4

    },

    "Usia": {

        "0-5 Tahun": 1,

        "6-12 Tahun": 2,

        "13-18 Tahun": 3

    },

    "Cara Keluar": {

        "Dipulangkan": 1,

        "Meninggal": 2

    },

    "Ruang Rawat": {

        "Sakura 1 (Akut)": 1,

        "Sakura 2 (Kronis)": 2,

        "Lavender 11 (HCU SCN)": 3

    },

    "Diagnosa Utama": {

        "Kanker": 1,

        "Pernafasan": 2,

        "Paru-paru": 3,

        "Pencernaan": 4,

        "Campak": 5

    }

}

# ==========================================
# PEMBOBOTAN SATU KOLOM
# ==========================================

def bobot_kolom(series, mapping):

    return series.map(mapping)


# ==========================================
# VALIDASI
# ==========================================

def validasi_bobot(df):

    error = {}

    for kolom, mapping in BOBOT.items():

        sumber = kolom

        if kolom == "LD":

            sumber = "LD_KATEGORI"

        elif kolom == "Usia":

            sumber = "USIA_KATEGORI"

        nilai = set(

            df[sumber]

            .dropna()

            .unique()

        )

        tidak_ditemukan = nilai - set(mapping.keys())

        if tidak_ditemukan:

            error[kolom] = list(tidak_ditemukan)

    return error


# ==========================================
# PEMBOBOTAN DATA
# ==========================================

def pembobotan_data(dataframe):

    df = dataframe.copy()

    df_bobot = pd.DataFrame()

    df_bobot["JK"] = bobot_kolom(

        df["JK"],

        BOBOT["JK"]

    )

    df_bobot["LD"] = bobot_kolom(

        df["LD_KATEGORI"],

        BOBOT["LD"]

    )

    df_bobot["Kelas Rawatan"] = bobot_kolom(

        df["Kelas Rawatan"],

        BOBOT["Kelas Rawatan"]

    )

    df_bobot["Usia"] = bobot_kolom(

        df["USIA_KATEGORI"],

        BOBOT["Usia"]

    )

    df_bobot["Cara Keluar"] = bobot_kolom(

        df["Cara Keluar"],

        BOBOT["Cara Keluar"]

    )

    df_bobot["Ruang Rawat"] = bobot_kolom(

        df["Ruang Rawat"],

        BOBOT["Ruang Rawat"]

    )

    df_bobot["Diagnosa Utama"] = bobot_kolom(

        df["Diagnosa Utama"],

        BOBOT["Diagnosa Utama"]

    )

    return df_bobot
