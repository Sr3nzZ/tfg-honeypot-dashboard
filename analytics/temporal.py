import pandas as pd
import plotly.express as px
from ui.styles import apply_base_layout, PALETTE_CATEGORICAL, PALETTE_SEQUENTIAL_ORANGE
from ui import components as ui
 
TOOLS = ["p0f", "suricata", "fatt", "nginx"]
 
 
def _attacks_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

    df["day_hour"] = df["timestamp"].dt.floor("h")

    return (
        df.groupby("day_hour")
        .size()
        .reset_index(name="attacks")
    )
 
 
def _attacks_by_day_hour_honeypot(df: pd.DataFrame, tools: bool = False) -> pd.DataFrame:
    df = df.copy()
    if tools:
        df = df[df["honeypot"].isin(TOOLS)]
    else:
        df = df[~df["honeypot"].isin(TOOLS)]
    df["day_hour"] = df["timestamp"].dt.floor("h")
    return (
        df.groupby(["day_hour", "honeypot"]).size()
        .reset_index(name="attacks")
        .sort_values(["honeypot", "day_hour"])
    )
 
 
def _create_hourly_attacks_chart(df_hora: pd.DataFrame) -> px.Figure:
    fig = px.bar(
        df_hora, x="hour", y="attacks",
        title="Attacks by hour of day (UTC)",
        labels={"hour": "Hour", "attacks": "Attacks"},
        color="attacks", color_continuous_scale=PALETTE_SEQUENTIAL_ORANGE,
    )
    apply_base_layout(fig)
    fig.update_layout(xaxis=dict(tickmode="linear", tick0=0, dtick=2))
    return fig
 
 
def _create_day_hour_honeypot_chart(df_data: pd.DataFrame, title: str) -> px.Figure:
    fig = px.line(
        df_data,
        x="day_hour",
        y="attacks",
        color="honeypot",
        title=title,
        labels={
            "day_hour": "Day & Hour",
            "attacks": "Attacks",
            "honeypot": "Honeypot"
        },
        markers=False,
        color_discrete_sequence=PALETTE_CATEGORICAL,
    )

    apply_base_layout(fig, legend=dict(orientation="h", y=-0.25))

    fig.update_layout(
        xaxis=dict(tickangle=-45, nticks=24),
        yaxis=dict(type="linear")
    )

    return fig
 
 
def render(df: pd.DataFrame) -> None:
    ui.section("Temporal analysis")
 
    col_hora, col_tools, col_honeypots = ui.columns(1, 1, 1)
 
    with col_hora:
        ui.plot(_create_hourly_attacks_chart(_attacks_by_hour(df)), key="temp_hora")
 
    with col_tools:
        ui.plot(_create_day_hour_honeypot_chart(
            _attacks_by_day_hour_honeypot(df, tools=True),
            "Tools activity by day and hour"
        ), key="temp_tools")
 
    with col_honeypots:
        ui.plot(_create_day_hour_honeypot_chart(
            _attacks_by_day_hour_honeypot(df, tools=False),
            "Honeypots activity by day and hour"
        ), key="temp_honeypots")
 
    ui.separator()