from __future__ import annotations

import streamlit as st


def initialize_state() -> None:
    defaults = {
        "subject_id": "001",
        "messages": [],
        "show_debug": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
