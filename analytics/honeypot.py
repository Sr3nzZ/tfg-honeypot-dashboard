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


def _group_small_categories(df: pd.DataFrame, threshold: float = 0.05) -> pd.DataFrame:
    df = df.copy()

    total = df["Attacks"].sum()
    df["ratio"] = df["Attacks"] / total

    main = df[df["ratio"] >= threshold].copy()
    small = df[df["ratio"] < threshold]

    if not small.empty:
        other_row = pd.DataFrame({
            "Honeypot": ["Other"],
            "Attacks": [small["Attacks"].sum()]
        })
        main = pd.concat([main[["Honeypot", "Attacks"]], other_row], ignore_index=True)
    else:
        main = main[["Honeypot", "Attacks"]]

    return main


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

def _heatmap_data(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["country", "honeypot"])
        .size()
        .reset_index(name="Attacks")
    )


def _create_heatmap(df: pd.DataFrame):
    fig = px.density_heatmap(
        df,
        x="country",
        y="honeypot",
        z="Attacks",
        color_continuous_scale="Reds",
        title="Honeypot activity by country"
    )

    apply_base_layout(fig, margin=dict(l=10, r=10, t=40, b=10))

    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Honeypot"
    )

    return fig


def render(df: pd.DataFrame) -> None:
    ui.section("Honeypot distribution")

    df_filtered = _filter_honeypots(df)

    if df_filtered.empty:
        ui.no_data("Honeypots")
        ui.separator()
        return

    df_chart = _honeypot_distribution(df_filtered)

    df_chart = _group_small_categories(df_chart, threshold=0.05)

    ui.plot(
        _create_pie_chart(df_chart),
        key="honeypot_pie"
    )

    ui.separator()

    df_heat = _heatmap_data(df_filtered)

    if not df_heat.empty:
        ui.plot(
            _create_heatmap(df_heat),
            key="honeypot_heatmap"
        )

    ui.separator()