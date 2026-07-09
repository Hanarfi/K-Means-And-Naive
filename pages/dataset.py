import pandas as pd
import streamlit as st

from models.auth import (
    login_required,
    get_user_id
)

from models.preprocessing import (
    preprocessing_data,
    validasi_kolom
)

from models.pembobotan import (
    pembobotan_data
)

from models.database_helper import (
    simpan_dataset,
    simpan_data_bobot
)


# ==========================================
# SESSION STATE
# ==========================================

def init_session():

    if "dataset_preview" not in st.session_state:
        st.session_state.dataset_preview = None

    if "nama_file" not in st.session_state:
        st.session_state.nama_file = None

    if "nama_dataset" not in st.session_state:
        st.session_state.nama_dataset = ""

    if "deskripsi_dataset" not in st.session_state:
        st.session_state.deskripsi_dataset = ""

    if "last_uploaded_file" not in st.session_state:
        st.session_state.last_uploaded_file = None
    
    if "dataset_detail" not in st.session_state:
        st.session_state.dataset_detail = None




# ==========================================
# RESET SESSION
# ==========================================

def reset_session():

    st.session_state.dataset_preview = None

    st.session_state.nama_file = None

    st.session_state.nama_dataset = ""

    st.session_state.deskripsi_dataset = "" 
    
    st.session_state.last_uploaded_file = None
    
    st.session_state.dataset_detail = None




# ==========================================
# PREVIEW DATASET
# ==========================================

def preview_dataset(df):

    st.subheader("📄 Preview Dataset")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            f"Jumlah Data : {len(df)}"
        )

    with col2:

        st.success(
            f"Jumlah Kolom : {len(df.columns)}"
        )


# ==========================================
# DAFTAR DATASET
# ==========================================

def tampil_daftar_dataset():

    st.divider()

    st.subheader("📚 Dataset Saya")

    daftar = get_dataset_user(
        get_user_id()
    )

    if len(daftar) == 0:

        st.info(
            "Belum ada dataset yang tersimpan."
        )

        return

    for data in daftar:

        with st.container(border=True):

            st.markdown(
                f"### 📁 {data['nama_dataset']}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Jumlah Data :** {data['jumlah_data']}"
                )

                st.write(
                    f"**File :** {data['nama_file']}"
                )

            with col2:

                st.write(
                    f"**Tanggal Upload :** {data['tanggal_upload']}"
                )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(

                    "📄 Detail",

                    key=f"detail_{data['id_dataset']}"

                ):

                    st.session_state.dataset_detail = (
                        data["id_dataset"]
                    )

            with col2:

                if st.button(

                    "🗑 Hapus",

                    key=f"hapus_{data['id_dataset']}"

                ):

                    berhasil = hapus_dataset(
                        data["id_dataset"]
                    )

                    if berhasil:

                        st.success(
                            "Dataset berhasil dihapus."
                        )

                        st.rerun()



# ==========================================
# BACA FILE EXCEL
# ==========================================

def baca_excel(file):

    try:

        df = pd.read_excel(file)

        return True, df

    except Exception as e:

        return False, str(e)


# ==========================================
# VALIDASI DATASET
# ==========================================

def validasi_dataset(df):

    kolom_error = validasi_kolom(df)

    if len(kolom_error) > 0:

        return False, kolom_error

    return True, None




# ==========================================
# HALAMAN DATASET
# ==========================================

def show():

    # ------------------------------
    # Validasi Login
    # ------------------------------

    login_required()

    # ------------------------------
    # Session
    # ------------------------------

    init_session()

    # ------------------------------
    # Header
    # ------------------------------

    st.title("📂 Dataset Saya")

    st.write(
        "Upload dataset pasien rawat inap dalam format Microsoft Excel (*.xlsx)."
    )

    st.divider()

    # ------------------------------
    # Form Input
    # ------------------------------

    nama_dataset = st.text_input(
        "Nama Dataset",
        value=st.session_state.nama_dataset
    )

    deskripsi = st.text_area(
        "Deskripsi Dataset",
        value=st.session_state.deskripsi_dataset
    )

    file = st.file_uploader(
        "Upload File Excel",
        type=["xlsx", "xls"]
    )

    # Simpan input sementara

    st.session_state.nama_dataset = nama_dataset
    st.session_state.deskripsi_dataset = deskripsi

    # ------------------------------
    # Jika user mengganti file
    # ------------------------------

    if file is not None:

        if (
            st.session_state.last_uploaded_file is not None
            and
            file.name != st.session_state.last_uploaded_file
        ):

            st.session_state.dataset_preview = None
            st.session_state.nama_file = None

    # ------------------------------
    # Tombol Preview
    # ------------------------------

    if st.button(
        "📄 Preview Dataset",
        use_container_width=True
    ):

        # Nama dataset

        if nama_dataset.strip() == "":

            st.error(
                "Nama dataset wajib diisi."
            )

            st.stop()

        # File

        if file is None:

            st.error(
                "Silakan pilih file Excel."
            )

            st.stop()

        # Membaca Excel

        berhasil, hasil = baca_excel(file)

        if not berhasil:

            st.error(hasil)

            st.stop()

        df = hasil

        # Validasi Kolom

        valid, kolom_error = validasi_dataset(df)

        if not valid:

            st.error(
                "Struktur dataset tidak sesuai."
            )

            st.write(
                "Kolom berikut tidak ditemukan:"
            )

            for kolom in kolom_error:

                st.write(
                    f"• {kolom}"
                )

            st.stop()

        # Simpan ke session

        st.session_state.dataset_preview = df

        st.session_state.nama_file = file.name

        st.session_state.last_uploaded_file = file.name

        st.info(
            "Dataset berhasil dibaca dan siap dipreview."
        )

    # ------------------------------
    # Preview Dataset
    # ------------------------------
    
    if st.session_state.dataset_preview is not None:
    
        st.divider()
    
        preview_dataset(
            st.session_state.dataset_preview
        )
    
        st.divider()
    
        if st.button(
            "💾 Simpan Dataset",
            use_container_width=True
        ):
    
            progress = st.progress(0)
    
            status = st.empty()
    
            df = st.session_state.dataset_preview
    
            # ------------------------------
            # Preprocessing
            # ------------------------------
    
            status.write("Melakukan preprocessing...")
    
            progress.progress(20)
    
            df_bersih = preprocessing_data(df)
    
            # ------------------------------
            # Pembobotan
            # ------------------------------
    
            status.write("Melakukan pembobotan...")
    
            progress.progress(40)
    
            df_bobot = pembobotan_data(df_bersih)
    
            # ------------------------------
            # Simpan Dataset
            # ------------------------------
    
            status.write("Menyimpan dataset...")
    
            progress.progress(70)
            st.write("ID USER :", get_user_id())
            berhasil, hasil = simpan_dataset(
    
                get_user_id(),
    
                nama_dataset,
    
                deskripsi,
    
                st.session_state.nama_file,
    
                df_bersih
    
            )
    
            if berhasil:
    
                status.write(
                    "Menyimpan data berbobot..."
                )
    
                progress.progress(90)
    
                simpan_data_bobot(
                    hasil,
                    df_bobot
                )
    
                progress.progress(100)
    
                status.success(
                    "Dataset berhasil disimpan."
                )
    
                st.success(
                    "Dataset berhasil diproses."
                )
    
                st.balloons()
    
                reset_session()
    
                st.rerun()
    
            else:
    
                progress.empty()
    
                st.error(
                    hasil
                )

    tampil_daftar_dataset()

        

