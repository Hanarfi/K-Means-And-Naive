# models/auth.py

import streamlit as st


def cek_login():

    return st.session_state.get(
        "login",
        False
    )


def cek_admin():

    return (
        st.session_state.get(
            "role"
        ) == "admin"
    )

def logout():

    for key in list(
        st.session_state.keys()
    ):
        del st.session_state[key]
