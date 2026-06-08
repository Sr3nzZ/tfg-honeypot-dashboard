# ui/layout.py
import streamlit as st
from datetime import datetime
from config.settings import APP_TITLE, APP_DESCRIPTION, RANGOS_TIEMPO, HONEYPOTS
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
        st.caption(APP_DESCRIPTION)
        st.divider()

        dias = st.selectbox(
            "Time range",
            options=list(RANGOS_TIEMPO.keys()),
            format_func=lambda x: RANGOS_TIEMPO[x],
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
    rango_texto = RANGOS_TIEMPO.get(dias, f"{dias} days").lower()
    st.title("Honeypot Dashboard")
    st.caption(f"{rango_texto} · {total_eventos:,} events")
    st.divider()


def footer(texto: str) -> None:
    st.caption(texto)
