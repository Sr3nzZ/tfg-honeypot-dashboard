import streamlit as st
import pandas as pd
from supabase import create_client
from config.settings import CACHE_TTL
 
 
@st.cache_resource
def _get_client():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"],
    )
 
 
def load_window(desde: str, hasta: str) -> pd.DataFrame:
    """
    Carga solo los eventos entre dos timestamps.
    Se llama incrementalmente desde el live mode.
    """
    sb = _get_client()
 
    res = (
        sb.table("ataques")
        .select("*")
        .gte("timestamp", desde)
        .lt("timestamp", hasta)
        .order("timestamp", desc=False)
        .limit(5000)
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
    if honeypot == "All" or df.empty:
        return df
    return df[df["honeypot"] == honeypot].copy()