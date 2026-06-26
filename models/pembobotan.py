import pandas as pd

from models.master_bobot import MASTER_BOBOT


# ==========================================
# PEMBOBOTAN SATU KOLOM
# ==========================================

def bobot_kolom(series, mapping):

    return series.map(mapping)


# ==========================================
# VALIDASI MASTER BOBOT
# ==========================================

def validasi_bobot(dataframe):

    sumber_kolom = {

        "JK": "JK",

        "LD": "LD_KATEGORI",

        "Kelas Rawatan": "Kelas Rawatan",

        "Usia": "USIA_KATEGORI",

        "Cara Keluar": "Cara Keluar",

        "Ruang Rawat": "Ruang Rawat",

        "Diagnosa Utama": "Diagnosa Utama"

    }

    error = {}

    for atribut, mapping in MASTER_BOBOT.items():

        kolom = sumber_kolom[atribut]

        nilai_dataset = set(

            dataframe[kolom]

            .dropna()

            .unique()

        )

        nilai_master = set(

            mapping.keys()

        )

        tidak_dikenal = nilai_dataset - nilai_master

        if tidak_dikenal:

            error[atribut] = list(tidak_dikenal)

    return error


# ==========================================
# PEMBOBOTAN DATASET
# ==========================================

def pembobotan_data(dataframe):

    error = validasi_bobot(dataframe)

    if error:

        raise ValueError(

            f"Nilai tidak terdapat pada master bobot : {error}"

        )

    df = pd.DataFrame()

    df["JK"] = bobot_kolom(

        dataframe["JK"],

        MASTER_BOBOT["JK"]

    )

    df["LD"] = bobot_kolom(

        dataframe["LD_KATEGORI"],

        MASTER_BOBOT["LD"]

    )

    df["Kelas Rawatan"] = bobot_kolom(

        dataframe["Kelas Rawatan"],

        MASTER_BOBOT["Kelas Rawatan"]

    )

    df["Usia"] = bobot_kolom(

        dataframe["USIA_KATEGORI"],

        MASTER_BOBOT["Usia"]

    )

    df["Cara Keluar"] = bobot_kolom(

        dataframe["Cara Keluar"],

        MASTER_BOBOT["Cara Keluar"]

    )

    df["Ruang Rawat"] = bobot_kolom(

        dataframe["Ruang Rawat"],

        MASTER_BOBOT["Ruang Rawat"]

    )

    df["Diagnosa Utama"] = bobot_kolom(

        dataframe["Diagnosa Utama"],

        MASTER_BOBOT["Diagnosa Utama"]

    )

    return df
