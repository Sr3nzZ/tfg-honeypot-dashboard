import pandas as pd
import plotly.express as px

from ui.styles import apply_base_layout
from ui import components as ui

TOOLS = ["p0f", "suricata", "fatt", "nginx"]


def _filter_honeypots(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df["honeypot"].isin(TOOLS)].dropna(subset=["honeypot"])

def _filter_tools(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df[df["honeypot"].isin(TOOLS)]
        .dropna(subset=["honeypot"])
    )


def _distribution(df: pd.DataFrame, col: str) -> pd.DataFrame:
    data = (
        df[col]
        .astype(str)
        .value_counts()
        .reset_index()
    )
    data.columns = [col.capitalize(), "Attacks"]
    return data


def _group_small_categories(df: pd.DataFrame, threshold: float = 0.05) -> pd.DataFrame:
    df = df.copy()

    total = df["Attacks"].sum()
    df["ratio"] = df["Attacks"] / total

    main = df[df["ratio"] >= threshold].copy()
    small = df[df["ratio"] < threshold]

    if not small.empty:
        other = pd.DataFrame({
            df.columns[0]: ["Other"],
            "Attacks": [small["Attacks"].sum()]
        })
        main = pd.concat(
            [main[[df.columns[0], "Attacks"]], other],
            ignore_index=True
        )
    else:
        main = main[[df.columns[0], "Attacks"]]

    return main


def _create_pie_chart(df: pd.DataFrame, title: str):
    fig = px.pie(
        df,
        names=df.columns[0],
        values="Attacks",
        title=title,
        hole=0.35
    )

    apply_base_layout(fig, margin=dict(l=10, r=10, t=40, b=10))
    return fig

def render(df: pd.DataFrame) -> None:
    ui.section("Tools & Honeypot distribution")

    df_filtered = _filter_honeypots(df)

    if df_filtered.empty:
        ui.no_data("Honeypots")
        ui.separator()
        return

    df_honeypots = _filter_honeypots(df)

    if not df_honeypots.empty:
        df_chart_hp = _distribution(df_honeypots, "honeypot")
        df_chart_hp = _group_small_categories(df_chart_hp)

        ui.plot(
            _create_pie_chart(df_chart_hp, "Attacks by Honeypot"),
            key="honeypot_pie"
        )

    ui.separator()

    df_tools = _filter_tools(df)

    if not df_tools.empty:
        df_chart_tools = _distribution(df_tools, "honeypot")

        ui.plot(
            _create_pie_chart(df_chart_tools, "Tools activity distribution"),
            key="tools_pie"
        )

    ui.separator()