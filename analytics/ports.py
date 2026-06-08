import pandas as pd
import plotly.express as px
from config.settings import PORT_NAMES, TOP_N
from ui.styles import apply_base_layout, PALETTE_CATEGORICAL, PALETTE_SEQUENTIAL_BLUE
from ui import components as ui
 
TOOLS = ["p0f", "suricata", "fatt", "nginx"]
 
 
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
 
 
def _attacks_by_honeypot(df: pd.DataFrame, tools: bool = False) -> pd.DataFrame:
    if tools:
        filtered = df[df["honeypot"].isin(TOOLS)]
    else:
        filtered = df[~df["honeypot"].isin(TOOLS)]
    return (
        filtered["honeypot"].dropna()
        .value_counts().reset_index()
        .rename(columns={"honeypot": "Honeypot", "count": "Attacks"})
    )
 
 
def _create_ports_pie(df_puertos: pd.DataFrame) -> px.Figure:
    fig = px.pie(
        df_puertos, names="Service", values="Attacks",
        title=f"Top {TOP_N} most attacked ports",
        hole=0.45,
        color_discrete_sequence=PALETTE_CATEGORICAL,
    )
    apply_base_layout(fig, legend=dict(orientation="h", y=-0.1))
    return fig
 
 
def _create_honeypot_chart(df_honey: pd.DataFrame, title: str) -> px.Figure:
    fig = px.pie(
        df_honey, names="Honeypot", values="Attacks",
        title=title, hole=0.45,
        color_discrete_sequence=PALETTE_CATEGORICAL,
    )
    apply_base_layout(fig, legend=dict(orientation="h", y=-0.1))
    return fig
 
 
def render(df: pd.DataFrame) -> None:
    ui.section("🔌 Ports and protocols")
 
    col_ports, col_tools, col_honeypots = ui.columns(1, 1, 1)
 
    with col_ports:
        ui.plot(_create_ports_pie(_top_ports(df)), key="ports_pie")
 
    with col_tools:
        ui.plot(_create_honeypot_chart(
            _attacks_by_honeypot(df, tools=True),
            "Distribution by tool"
        ), key="ports_tools")
 
    with col_honeypots:
        ui.plot(_create_honeypot_chart(
            _attacks_by_honeypot(df, tools=False),
            "Distribution by honeypot"
        ), key="ports_honeypots")
 
    ui.separator()