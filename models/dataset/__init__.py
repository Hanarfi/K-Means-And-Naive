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
