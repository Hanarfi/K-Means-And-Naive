import streamlit as st


# ==========================================
# CEK STATUS LOGIN
# ==========================================

def is_login():
    """
    Mengembalikan True jika user sudah login.
    """

    return st.session_state.get(
        "login",
        False
    )


# ==========================================
# WAJIB LOGIN
# ==========================================

def login_required():
    """
    Menghentikan halaman apabila user
    belum login.
    """

    if not is_login():

        st.warning(
            "Silakan login terlebih dahulu."
        )

        st.stop()


# ==========================================
# CEK ROLE ADMIN
# ==========================================

def is_admin():
    """
    True jika role = admin.
    """

    return (
        st.session_state.get(
            "role"
        ) == "admin"
    )


# ==========================================
# WAJIB ADMIN
# ==========================================

def admin_required():
    """
    Halaman hanya boleh diakses admin.
    """

    login_required()

    if not is_admin():

        st.error(
            "Anda tidak memiliki hak akses ke halaman ini."
        )

        st.stop()


# ==========================================
# DATA USER
# ==========================================

def get_user():

    """
    Mengembalikan data user
    dalam bentuk dictionary.
    """

    return {

        "id_pengguna":
            st.session_state.get(
                "id_pengguna"
            ),

        "nama_lengkap":
            st.session_state.get(
                "nama_lengkap"
            ),

        "role":
            st.session_state.get(
                "role"
            )

    }


# ==========================================
# ID USER
# ==========================================

def get_user_id():

    return st.session_state.get(
        "id_pengguna"
    )


# ==========================================
# NAMA USER
# ==========================================

def get_nama():

    return st.session_state.get(
        "nama_lengkap",
        ""
    )


# ==========================================
# ROLE USER
# ==========================================

def get_role():

    return st.session_state.get(
        "role",
        ""
    )


# ==========================================
# LOGOUT
# ==========================================

def logout():
    """
    Menghapus seluruh session login.
    """

    st.session_state["login"] = False

    st.session_state["id_pengguna"] = None

    st.session_state["nama_lengkap"] = ""

    st.session_state["role"] = ""

    st.session_state["menu"] = "dashboard"

    st.session_state["auth_page"] = "login"
