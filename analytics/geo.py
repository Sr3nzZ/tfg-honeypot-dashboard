# analytics/geo.py
import pandas as pd
import plotly.express as px
from config.settings import TOP_N
from ui.styles import apply_base_layout, apply_yaxis_reversed, PALETTE_CATEGORICAL, PALETTE_SEQUENTIAL_RED, GEO_LAYOUT
from ui import components as ui


def _prepare_geo_data(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["country", "latitude", "longitude", "honeypot"]
    return (
        df.dropna(subset=["latitude", "longitude"])
        .groupby(cols).size()
        .reset_index(name="count")
    )


def _top_countries(df: pd.DataFrame, n: int = TOP_N) -> pd.DataFrame:
    return (
        df["country"].dropna()
        .value_counts().head(n)
        .reset_index()
        .rename(columns={"country": "Country", "count": "Attacks"})
    )


def _create_geo_map(df_geo: pd.DataFrame) -> px.Figure:
    fig = px.scatter_geo(
        df_geo, lat="latitude", lon="longitude",
        size="count", color="honeypot",
        hover_name="country",
        hover_data={"count": True, "latitude": False, "longitude": False},
        title="Worldwide attacker distribution",
        size_max=40,
        color_discrete_sequence=PALETTE_CATEGORICAL,
    )
    apply_base_layout(fig, geo=GEO_LAYOUT, legend=dict(orientation="h", y=-0.05))
    return fig


def _create_country_bar_chart(df_paises: pd.DataFrame) -> px.Figure:
    fig = px.bar(
        df_paises, x="Attacks", y="Country", orientation="h",
        title=f"Top {TOP_N} attacking countries",
        color="Attacks", color_continuous_scale=PALETTE_SEQUENTIAL_RED,
    )
    apply_base_layout(fig)
    apply_yaxis_reversed(fig)
    return fig


def render(df: pd.DataFrame) -> None:
    ui.section("🌍 Geographic origin of attacks")
    col_mapa, col_paises = ui.fila_columnas(2, 1)
    with col_mapa:
        datos = _prepare_geo_data(df)
        if not datos.empty:
            ui.grafico(_create_geo_map(datos), key="geo_mapa")
        else:
            ui.sin_datos("geolocation")
    with col_paises:
        ui.grafico(_create_country_bar_chart(_top_countries(df)), key="geo_paises")
    ui.separador()
