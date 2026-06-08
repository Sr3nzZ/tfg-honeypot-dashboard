import pandas as pd
import plotly.express as px

from ui.styles import apply_base_layout
from ui import components as ui

TOOLS = ["p0f", "suricata", "fatt", "nginx"]


def _filter_honeypots(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df["honeypot"].isin(TOOLS)].dropna(subset=["honeypot"])


def _honeypot_distribution(df: pd.DataFrame) -> pd.DataFrame:
    data = (
        df["honeypot"]
        .astype(str)
        .value_counts()
        .reset_index()
    )

    data.columns = ["Honeypot", "Attacks"]
    return data


def _create_pie_chart(df: pd.DataFrame) -> px.Figure:
    fig = px.pie(
        df,
        names="Honeypot",
        values="Attacks",
        title="Attacks by Honeypot",
        hole=0.35  
    )

    apply_base_layout(fig, margin=dict(l=10, r=10, t=40, b=10))

    return fig


def render(df: pd.DataFrame) -> None:
    ui.section("Honeypot distribution")

    df_filtered = _filter_honeypots(df)

    if df_filtered.empty:
        ui.no_data("Honeypots")
        ui.separator()
        return

    df_chart = _honeypot_distribution(df_filtered)

    ui.plot(
        _create_pie_chart(df_chart),
        key="honeypot_pie"
    )

    ui.separator()