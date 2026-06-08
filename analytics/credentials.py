import pandas as pd
import plotly.express as px
from config.settings import TOP_N
from ui.styles import apply_base_layout, apply_yaxis_reversed, PALETTE_SEQUENTIAL_PURPLE, PALETTE_SEQUENTIAL_RED, PALETTE_SEQUENTIAL_ORANGE
from ui import components as ui


def _filter_cowrie(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["honeypot"] == "cowrie"].dropna(subset=["username", "password"])


def _top_usernames(df: pd.DataFrame, n: int = TOP_N) -> pd.DataFrame:
    return (
        df["username"].value_counts().head(n)
        .reset_index()
        .rename(columns={"username": "Username", "count": "Attempts"})
    )


def _top_passwords(df: pd.DataFrame, n: int = TOP_N) -> pd.DataFrame:
    return (
        df["password"].value_counts().head(n)
        .reset_index()
        .rename(columns={"password": "Password", "count": "Attempts"})
    )


def _top_username_password_combinations(df: pd.DataFrame, n: int = TOP_N) -> pd.DataFrame:
    datos = (
        df.groupby(["username", "password"]).size()
        .reset_index(name="Attempts")
        .sort_values("Attempts", ascending=False).head(n)
    )
    datos["Combination"] = datos["username"] + " / " + datos["password"]
    return datos


def _create_horizontal_bar_chart(df_datos, x, y, titulo, paleta) -> px.Figure:
    fig = px.bar(
        df_datos, x=x, y=y, orientation="h",
        title=titulo, color=x, color_continuous_scale=paleta,
    )
    apply_base_layout(fig, margin=dict(l=0, r=0, t=40, b=0))
    apply_yaxis_reversed(fig)
    return fig

def _create_password_treemap(df: pd.DataFrame) -> px.Figure:
    fig = px.treemap(
        df,
        path=["Password"],
        values="Attempts",
        title="Password distribution (Treemap)",
        color="Attempts",
        color_continuous_scale=PALETTE_SEQUENTIAL_RED,
    )

    apply_base_layout(fig)
    return fig


def render(df: pd.DataFrame) -> None:
    ui.section("🔐 SSH credentials captured")
    df_cowrie = _filter_cowrie(df)
    if df_cowrie.empty:
        ui.no_data("Cowrie")
        ui.separator()
        return
    col_user, col_pass, col_combo = ui.columns(1, 1, 1)
    with col_user:
        ui.plot(_create_horizontal_bar_chart(_top_usernames(df_cowrie), "Attempts", "Username", "Top usernames", PALETTE_SEQUENTIAL_PURPLE), key="creds_users")
    with col_pass:
        ui.plot(
            _create_horizontal_bar_chart(
                _top_passwords(df_cowrie),
                "Attempts",
                "Password",
                "Top passwords",
                PALETTE_SEQUENTIAL_RED
            ),
            key="creds_pass"
        )
    with col_combo:
        ui.plot(_create_horizontal_bar_chart(_top_username_password_combinations(df_cowrie), "Attempts", "Combination", "Top combinations", PALETTE_SEQUENTIAL_ORANGE), key="creds_combo")
    ui.separator()
