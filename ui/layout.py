# ui/layout.py
import streamlit as st
from datetime import datetime
from config.settings import APP_TITLE, TIME_RANGE, HONEYPOTS
from ui.styles import CSS


def configure_page() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(CSS, unsafe_allow_html=True)


def render_sidebar() -> tuple[int, str]:
    with st.sidebar:
        st.title(f"{APP_TITLE.split('·')[0].strip()}")
        st.divider()

        dias = st.selectbox(
            "Time range",
            options=list(TIME_RANGE.keys()),
            format_func=lambda x: TIME_RANGE[x],
            index=2,
        )

        honeypot = st.selectbox("Honeypot", HONEYPOTS)

        st.divider()
        st.info("Data from May 27 – Jun 3, 2026")
        st.caption(
            "The system is designed for real-time updates. "
            "Data has been scoped to this period due to storage constraints."
        )

    return dias, honeypot


def render_header(total_eventos: int, dias: int) -> None:
    rango_texto = TIME_RANGE.get(dias, f"{dias} days").lower()
    st.title("Honeypot Dashboard")
    st.caption(f"{rango_texto} · {total_eventos:,} events")
    st.divider()


def footer(texto: str) -> None:
    st.caption(texto)
