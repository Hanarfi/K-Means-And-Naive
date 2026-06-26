import streamlit as st
import pandas as pd

from models.auth import login_required
from models.database_helper import simpan_dataset
from models.auth import get_user_id

from models.preprocessing import preprocessing_data
from models.pembobotan import pembobotan_data

from models.database_helper import (
    simpan_dataset,
    simpan_data_bobot
)

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

def validasi_kolom(df):

    kolom_file = list(df.columns)

    kolom_tidak_ada = []

    for kolom in KOLOM_WAJIB:

        if kolom not in kolom_file:

            kolom_tidak_ada.append(kolom)

    return kolom_tidak_ada


# ==========================================
# PREVIEW
# ==========================================

def preview_dataset(df):

    st.subheader("Preview Dataset")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.success(
        f"Jumlah data : {len(df)} pasien"
    )


# ==========================================
# HALAMAN DATASET
# ==========================================

def show():

    if "dataset_preview" not in st.session_state:
        st.session_state.dataset_preview = None

    if "nama_file" not in st.session_state:
        st.session_state.nama_file = None

    login_required()

    st.title("📂 Dataset Saya")

    st.write(
        "Upload dataset pasien rawat inap."
    )

    st.divider()

    nama_dataset = st.text_input(
        "Nama Dataset"
    )

    deskripsi = st.text_area(
        "Deskripsi (Opsional)"
    )

    file = st.file_uploader(

        "Upload Dataset Excel",

        type=[
            "xlsx",
            "xls"
        ]

    )

    if st.button(

        "Preview Dataset",

        use_container_width=True

    ):

        if nama_dataset == "":

            st.error(
                "Nama dataset wajib diisi."
            )

            return

        if file is None:

            st.error(
                "Silakan pilih file."
            )

            return

        try:

            df = pd.read_excel(file)

        except Exception as e:

            st.error(e)

            return

        kolom_error = validasi_kolom(df)

        if len(kolom_error) > 0:

            st.error(
                "Kolom berikut tidak ditemukan:"
            )

            for kolom in kolom_error:

                st.write(
                    f"- {kolom}"
                )

            return

        st.success(
            "Struktur dataset valid."
        )

        preview_dataset(df)
