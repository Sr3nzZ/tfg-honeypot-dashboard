# analytics/data.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from supabase import create_client
from config.settings import CACHE_TTL


@st.cache_resource
def _get_client():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"],
    )


@st.cache_data(ttl=CACHE_TTL)
def load_data(dias: int) -> pd.DataFrame:
    sb = _get_client()
    desde = "2026-05-27:00:00:00Z"

    res = (
        sb.table("ataques")
        .select("*")
        .gte("timestamp", desde)
        .order("timestamp", desc=True)
        .limit(50000)
        .execute()
    )

    if not res.data:
        return pd.DataFrame()

    df = pd.DataFrame(res.data)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, format='ISO8601')

    for col in ("src_port", "dst_port", "alert_severity", "latitude", "longitude"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def filter_honeypot(df: pd.DataFrame, honeypot: str) -> pd.DataFrame:
    if honeypot == "Todos" or df.empty:
        return df
    return df[df["honeypot"] == honeypot].copy()
