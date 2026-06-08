# analytics/ports.py
import pandas as pd
import plotly.express as px
from config.settings import PORT_NAMES, TOP_N
from ui.styles import apply_base_layout, PALETTE_CATEGORICAL, PALETTE_SEQUENTIAL_BLUE
from ui import components as ui


def _top_ports(df: pd.DataFrame, n: int = TOP_N) -> pd.DataFrame:
    data = (
        df["dst_port"].dropna().astype(int)
        .value_counts()
        .head(n)
        .reset_index()
        .rename(columns={"dst_port": "Port", "count": "Attacks"})
    )

    def map_service(p):
        return PORT_NAMES.get(int(p), "Other")

    data["Service"] = data["Port"].map(map_service)

    return data


def _attacks_by_honeypot(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df["honeypot"].dropna()
        .value_counts()
        .reset_index()
        .rename(columns={"honeypot": "Honeypot", "count": "Attacks"})
    )


def _create_ports_chart(df_ports: pd.DataFrame) -> px.Figure:
    fig = px.pie(
        df_ports,
        names="Port",
        values="Attacks",
        title=f"Top {TOP_N} most attacked ports",
        color_discrete_sequence=PALETTE_CATEGORICAL,
        hole=0.4,
    )

    apply_base_layout(fig, legend=dict(orientation="h", y=-0.1))
    return fig


def _create_services_chart(df_ports: pd.DataFrame) -> px.Figure:
    fig = px.pie(
        df_ports,
        names="Service",
        values="Attacks",
        title=f"Top {TOP_N} most attacked services",
        color_discrete_sequence=PALETTE_CATEGORICAL,
        hole=0.4,
    )

    apply_base_layout(fig, legend=dict(orientation="h", y=-0.1))
    return fig


def _create_honeypot_chart(df_honey: pd.DataFrame) -> px.Figure:
    fig = px.pie(
        df_honey,
        names="Honeypot",
        values="Attacks",
        title="Distribution by honeypot",
        color_discrete_sequence=PALETTE_CATEGORICAL,
        hole=0.45,
    )

    apply_base_layout(fig, legend=dict(orientation="h", y=-0.1))
    return fig




def render(df: pd.DataFrame) -> None:
    ui.section("Ports and protocols")

    col_ports, col_services, col_honeypot = ui.columns(1, 1, 1)

    top_ports = _top_ports(df)
    honey_data = _attacks_by_honeypot(df)

    with col_ports:
        ui.plot(
            _create_ports_chart(top_ports),
            key="ports_chart"
        )

    with col_services:
        ui.plot(
            _create_services_chart(top_ports),
            key="services_chart"
        )

    with col_honeypot:
        ui.plot(
            _create_honeypot_chart(honey_data),
            key="honeypot_chart"
        )

    ui.separator()
