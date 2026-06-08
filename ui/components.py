# ui/components.py
import streamlit as st
import plotly.graph_objects as go
from typing import Any


def section(titulo: str) -> None:
    st.subheader(titulo)


def columns(*ratios: int):
    return st.columns(list(ratios))


def plot(fig: go.Figure, key: str | None = None) -> None:
    st.plotly_chart(fig, use_container_width=True, key=key)


def dataframe(df: Any, key: str | None = None) -> None:
    st.dataframe(df, use_container_width=True, hide_index=True, key=key)


def no_data(seccion: str) -> None:
    st.info(f"No data available for {seccion} in the selected range.")


def separator() -> None:
    st.divider()


def expander(titulo: str, expandido: bool = False):
    return st.expander(titulo, expanded=expandido)


def footer(texto: str) -> None:
    st.caption(texto)
