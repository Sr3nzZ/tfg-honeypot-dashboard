# analytics/suricata.py
import pandas as pd
import plotly.express as px
from config.settings import TOP_N, SEVERITY_MAP, SEVERITY_COLORS
from ui.styles import apply_base_layout, apply_yaxis_reversed, PALETTE_SEQUENTIAL_RED
from ui import components as ui


def _filter_suricata(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["honeypot"] == "suricata"].dropna(subset=["alert_signature"])


def _top_alert_signatures(df: pd.DataFrame, n: int = TOP_N) -> pd.DataFrame:
    return (
        df["alert_signature"].value_counts().head(n)
        .reset_index()
        .rename(columns={"alert_signature": "Signature", "count": "Occurrences"})
    )


def _alerts_by_severity(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Severity"] = df["alert_severity"].map(SEVERITY_MAP).fillna("Unknown")
    return (
        df["Severity"].value_counts()
        .reset_index()
        .rename(columns={"Severity": "Severity", "count": "Alerts"})
    )


def _create_signatures_chart(df_firmas: pd.DataFrame) -> px.Figure:
    fig = px.bar(
        df_firmas, x="Occurrences", y="Signature", orientation="h",
        title=f"Top {TOP_N} detected attack signatures",
        color="Occurrences", color_continuous_scale=PALETTE_SEQUENTIAL_RED,
    )
    apply_base_layout(fig)
    apply_yaxis_reversed(fig)
    return fig


def _create_severity_chart(df_sev: pd.DataFrame) -> px.Figure:
    fig = px.pie(
        df_sev, names="Severity", values="Alerts",
        title="Distribution by severity", hole=0.45,
        color="Severity", color_discrete_map=SEVERITY_COLORS,
    )
    apply_base_layout(fig, legend=dict(orientation="h", y=-0.1))
    return fig


def render(df: pd.DataFrame) -> None:
    ui.section("🚨 IDS Alerts — Suricata")
    df_suri = _filter_suricata(df)
    if df_suri.empty:
        ui.no_data("Suricata")
        ui.separator()
        return
    col_firmas, col_sev = ui.columns(2, 1)
    with col_firmas:
        ui.plot(_create_signatures_chart(_top_alert_signatures(df_suri)), key="suri_firmas")
    with col_sev:
        if "alert_severity" in df_suri.columns:
            ui.plot(_create_severity_chart(_alerts_by_severity(df_suri)), key="suri_sev")
    ui.separator()
