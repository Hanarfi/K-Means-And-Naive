# app.py

import streamlit as st

from pages.login import show as login_page
from pages.dashboard import show as dashboard_page


# Inisialisasi session
if "login" not in st.session_state:
    st.session_state["login"] = False


# Routing sederhana
if st.session_state["login"]:
    dashboard_page()
else:
    login_page()
