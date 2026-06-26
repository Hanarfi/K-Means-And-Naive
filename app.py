# app.py

import streamlit as st

from pages.login import show as login_page
from pages.register import show as register_page
from pages.dashboard import show as dashboard_page
from pages.dataset import show as dataset_page
from assets.load_css import load_css

from models.auth import logout

st.markdown(
    load_css(),
    unsafe_allow_html=True
)


if "login" not in st.session_state:
    st.session_state["login"] = False

if "menu" not in st.session_state:
    st.session_state["menu"] = "dashboard"


if not st.session_state["login"]:

    tampilkan_login()

else:

    tampilkan_sidebar()

    tampilkan_halaman()
