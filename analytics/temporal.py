# analytics/temporal.py
import pandas as pd
import plotly.express as px
from ui.styles import apply_base_layout, PALETTE_CATEGORICAL, PALETTE_SEQUENTIAL_ORANGE
from ui import components as ui


def _attacks_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.assign(hour=df["timestamp"].dt.hour)
        .groupby("hour").size()
        .reset_index(name="attacks")
    )


def _attacks_by_day(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.assign(date=df["timestamp"].dt.date)
        .groupby(["date", "honeypot"]).size()
        .reset_index(name="attacks")
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


def _create_daily_attacks_chart(df_dia: pd.DataFrame) -> px.Figure:
    fig = px.line(
        df_dia, x="date", y="attacks", color="honeypot",
        title="Daily evolution by honeypot",
        labels={"date": "Date", "attacks": "Attacks", "honeypot": "Honeypot"},
        markers=True, color_discrete_sequence=PALETTE_CATEGORICAL,
    )
    apply_base_layout(fig, legend=dict(orientation="h", y=-0.25))
    return fig


def render(df: pd.DataFrame) -> None:
    ui.section("Temporal analysis")
    col_hora, col_dia = ui.columns(1, 1)
    with col_hora:
        ui.grafico(_create_hourly_attacks_chart(_attacks_by_hour(df)), key="temp_hora")
    with col_dia:
        ui.grafico(_create_daily_attacks_chart(_attacks_by_day(df)), key="temp_dia")
    ui.separador()
