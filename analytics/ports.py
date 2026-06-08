# analytics/ports.py
import pandas as pd
import plotly.express as px
from config.settings import PORT_NAMES, TOP_N
from ui.styles import apply_base_layout, PALETTE_CATEGORICAL, PALETTE_SEQUENTIAL_BLUE
from ui import components as ui


def _top_ports(df: pd.DataFrame, n: int = TOP_N) -> pd.DataFrame:
    datos = (
        df["dst_port"].dropna().astype(int)
        .value_counts().head(n)
        .reset_index()
        .rename(columns={"dst_port": "Port", "count": "Attacks"})
    )
    datos["Service"] = datos["Port"].map(
        lambda p: PORT_NAMES.get(int(p), str(int(p)))
    )
    return datos


def _attacks_by_honeypot(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df["honeypot"].dropna()
        .value_counts().reset_index()
        .rename(columns={"honeypot": "Honeypot", "count": "Attacks"})
    )


def _create_ports_chart(df_puertos: pd.DataFrame) -> px.Figure:
    fig = px.pie(
        df_puertos,
        names="Service",
        values="Attacks",
        title=f"Top {TOP_N} most attacked ports",
        color_discrete_sequence=PALETTE_CATEGORICAL,
        hole=0.4,
    )

    apply_base_layout(fig, legend=dict(orientation="h", y=-0.1))
    return fig


def _create_honeypot_chart(df_honey: pd.DataFrame) -> px.Figure:
    fig = px.pie(
        df_honey, names="Honeypot", values="Attacks",
        title="Distribution by honeypot", hole=0.45,
        color_discrete_sequence=PALETTE_CATEGORICAL,
    )
    apply_base_layout(fig, legend=dict(orientation="h", y=-0.1))
    return fig


def render(df: pd.DataFrame) -> None:
    ui.section("🔌 Ports and protocols")
    col_puertos, col_honey = ui.columns(1, 1)
    with col_puertos:
        ui.plot(_create_ports_chart(_top_ports(df)), key="ports_top")
    with col_honey:
        ui.plot(_create_honeypot_chart(_attacks_by_honeypot(df)), key="ports_honey")
    ui.separator()
