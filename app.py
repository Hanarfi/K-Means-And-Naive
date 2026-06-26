import streamlit as st

# ==========================================
# IMPORT CSS
# ==========================================

from assets.load_css import load_css

# ==========================================
# IMPORT HALAMAN
# ==========================================

from pages.login import show as login_page
from pages.register import show as register_page

from pages.dashboard import show as dashboard_page
from pages.dataset import show as dataset_page

# Halaman berikutnya (aktifkan setelah dibuat)
# from pages.visualisasi import show as visualisasi_page
# from pages.kmeans import show as kmeans_page
# from pages.naive_bayes import show as naive_bayes_page
# from pages.riwayat import show as riwayat_page
# from pages.profil import show as profil_page

# Admin
# from pages.admin_user import show as admin_user_page
# from pages.admin_dataset import show as admin_dataset_page
# from pages.admin_statistik import show as admin_statistik_page
# from pages.admin_log import show as admin_log_page

from models.auth import logout

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(

    page_title="Sistem K-Means dan Naive Bayes",

    page_icon="🏥",

    layout="wide",

    initial_sidebar_state="expanded"

)

# ==========================================
# LOAD CSS
# ==========================================

st.markdown(

    load_css(),

    unsafe_allow_html=True

)

# ==========================================
# SESSION DEFAULT
# ==========================================

DEFAULT_SESSION = {

    "login": False,

    "auth_page": "login",

    "menu": "dashboard",

    "id_pengguna": None,

    "nama_lengkap": "",

    "role": ""

}

for key, value in DEFAULT_SESSION.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ==========================================
# SIDEBAR
# ==========================================

def sidebar():

    with st.sidebar:

        st.title("🏥 Sistem")

        st.caption("K-Means & Naive Bayes")

        st.divider()

        st.write(f"👤 **{st.session_state['nama_lengkap']}**")

        st.caption(
            f"Role : {st.session_state['role'].title()}"
        )

        st.divider()

        if st.button(
            "📊 Dashboard",
            use_container_width=True
        ):

            st.session_state["menu"] = "dashboard"

            st.rerun()

        if st.button(
            "📂 Dataset Saya",
            use_container_width=True
        ):

            st.session_state["menu"] = "dataset"

            st.rerun()

        # Aktifkan nanti

        # if st.button("📈 K-Means", use_container_width=True):
        #     st.session_state["menu"] = "kmeans"
        #     st.rerun()

        # if st.button("🧠 Naive Bayes", use_container_width=True):
        #     st.session_state["menu"] = "naive_bayes"
        #     st.rerun()

        # if st.button("📜 Riwayat", use_container_width=True):
        #     st.session_state["menu"] = "riwayat"
        #     st.rerun()

        # if st.button("👤 Profil", use_container_width=True):
        #     st.session_state["menu"] = "profil"
        #     st.rerun()

        # ======================================

        # MENU ADMIN

        # ======================================

        if st.session_state["role"] == "admin":

            st.divider()

            st.subheader("Admin")

            # nanti diaktifkan

            # if st.button("👥 Manajemen User"):
            #     ...

            # if st.button("🗂 Semua Dataset"):
            #     ...

            # if st.button("📊 Statistik"):
            #     ...

            # if st.button("📜 Log Aktivitas"):
            #     ...

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            logout()

            st.rerun()

# ==========================================
# ROUTING
# ==========================================

def halaman_user():

    menu = st.session_state["menu"]

    if menu == "dashboard":

        dashboard_page()

    elif menu == "dataset":

        dataset_page()

    else:

        st.warning(
            "Halaman belum tersedia."
        )

# ==========================================
# MAIN
# ==========================================

if not st.session_state["login"]:

    if st.session_state["auth_page"] == "login":

        login_page()

    else:

        register_page()

else:

    sidebar()

    halaman_user()
