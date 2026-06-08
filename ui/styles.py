# ui/styles.py
import plotly.graph_objects as go

PALETTE_CATEGORICAL = [
    "#7c3aed", "#0ea5e9", "#f59e0b", "#10b981",
    "#ef4444", "#ec4899", "#8b5cf6", "#06b6d4",
]

PALETTE_SEQUENTIAL_RED    = "Reds"
PALETTE_SEQUENTIAL_BLUE   = "Blues"
PALETTE_SEQUENTIAL_PURPLE = "Purples"
PALETTE_SEQUENTIAL_ORANGE = "Oranges"

BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", size=12),
    margin=dict(l=0, r=0, t=40, b=0),
    coloraxis_showscale=False,
)

GEO_LAYOUT = dict(
    bgcolor="rgba(0,0,0,0)",
    showframe=False,
    showcoastlines=True,
    coastlinecolor="#444",
    showland=True,
    landcolor="#1e1e2e",
    showocean=True,
    oceancolor="#12121f",
    showlakes=False,
    projection_type="natural earth",
)

CSS = """
<style>
    [data-testid="stMetricValue"]  { font-size: 1.9rem !important; font-weight: 700; }
    [data-testid="stMetricLabel"]  { font-size: 0.8rem !important; color: #a6adc8; }
    [data-testid="stSidebar"] { background: #12121f; }
    hr { border-color: #2e2e3e !important; }
    [data-testid="stDataFrame"] thead th {
        background: #1e1e2e !important;
        color: #cba6f7 !important;
        font-size: 0.82rem;
    }
</style>
"""


def apply_base_layout(fig: go.Figure, **overrides) -> go.Figure:
    layout = {**BASE_LAYOUT, **overrides}
    fig.update_layout(**layout)
    return fig


def apply_yaxis_reversed(fig: go.Figure) -> go.Figure:
    fig.update_layout(yaxis=dict(autorange="reversed"))
    return fig
