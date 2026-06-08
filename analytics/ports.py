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
        title=f"Most attacked services",
        color_discrete_sequence=PALETTE_CATEGORICAL,
        hole=0.4,
    )

    apply_base_layout(fig, legend=dict(orientation="h", y=-0.1))
    return fig



def render(df: pd.DataFrame) -> None:
    ui.section("Ports and protocols")

    col_ports, col_services = ui.columns(1, 1)

    top_ports = _top_ports(df)

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

    ui.separator()
