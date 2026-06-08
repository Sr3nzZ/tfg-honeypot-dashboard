import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
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

def _create_wordcloud(series: pd.Series, title: str):
    text = " ".join(series.dropna().astype(str))

    if not text.strip():
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No data available", ha="center", va="center")
        ax.axis("off")
        ax.set_title(title)
        return fig

    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        colormap="Reds"
    ).generate(text)

    fig, ax = plt.subplots()
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title(title)

    return fig

def _top_user_series(df: pd.DataFrame, n: int = TOP_N) -> pd.Series:
    return df["username"].value_counts().head(n)

def _top_password_series(df: pd.DataFrame, n: int = TOP_N) -> pd.Series:
    return df["password"].value_counts().head(n)


def render(df: pd.DataFrame) -> None:
    ui.section("🔐 SSH credentials captured")
    df_cowrie = _filter_cowrie(df)
    if df_cowrie.empty:
        ui.no_data("Cowrie")
        ui.separator()
        return
    user_series = _top_user_series(df_cowrie)
    pass_series = _top_password_series(df_cowrie)

    col_user, col_pass, col_combo = ui.columns(1, 1, 1)
    with col_user:
        if user_series.empty:
            ui.no_data("Usernames")
        else:
            ui.plot(
                _create_wordcloud(user_series, "Usernames WordCloud"),
                key="creds_users_wc"
            )

    with col_pass:
        if pass_series.empty:
            ui.no_data("Passwords")
        else:
            ui.plot(
                _create_wordcloud(pass_series, "Passwords WordCloud"),
                key="creds_pass_wc"
            )
    with col_combo:
        ui.plot(_create_horizontal_bar_chart(_top_username_password_combinations(df_cowrie), "Attempts", "Combination", "Top combinations", PALETTE_SEQUENTIAL_ORANGE), key="creds_combo")
    ui.separator()
