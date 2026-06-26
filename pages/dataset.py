import streamlit as st
import pandas as pd

from models.auth import cek_login


# ==========================================
# VALIDASI LOGIN
# ==========================================

def validasi_login():

    if not cek_login():

        st.warning(
            "Silakan login terlebih dahulu."
        )

        st.stop()


# ==========================================
# PREVIEW DATASET
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

    validasi_login()

    st.title("📂 Dataset Saya")

    st.write(
        "Upload dataset pasien untuk proses analisis."
    )

    st.divider()

    nama_dataset = st.text_input(
        "Nama Dataset"
    )

    deskripsi = st.text_area(
        "Deskripsi (Opsional)"
    )

    file = st.file_uploader(

        "Upload File Excel",

        type=[
            "xlsx",
            "xls"
        ]
    )

    if st.button(
        "Upload Dataset",
        use_container_width=True
    ):

        if not nama_dataset:

            st.error(
                "Nama dataset wajib diisi."
            )

            return

        if file is None:

            st.error(
                "Silakan pilih file Excel."
            )

            return

        try:

            df = pd.read_excel(
                file
            )

            st.success(
                "Dataset berhasil dibaca."
            )

            preview_dataset(df)

        except Exception as e:

            st.error(e)
