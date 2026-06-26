# app.py

import streamlit as st

from pages.login import show as login_page
from pages.register import show as register_page
from pages.dashboard import show as dashboard_page
from pages.dataset import show as dataset_page
from assets.load_css import load_css
st.markdown(
    load_css(),
    unsafe_allow_html=True
)


if "login" not in st.session_state:
    st.session_state["login"] = False

if "halaman" not in st.session_state:
    st.session_state["halaman"] = "login"


# Sudah login
if st.session_state["login"]:
    dashboard_page()

# Belum login
else:

    if st.session_state["halaman"] == "login":
        login_page()

    elif st.session_state["halaman"] == "register":
        register_page()
