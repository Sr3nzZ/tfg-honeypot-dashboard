# analytics/metrics.py
import streamlit as st
import pandas as pd


def _calculate(df: pd.DataFrame) -> dict:
    return {
        "total_ataques":     len(df),
        "ips_unicas":        df["src_ip"].nunique() if "src_ip" in df.columns else 0,
        "paises":            df["country"].nunique() if "country" in df.columns else 0,
        "honeypots_activos": df["honeypot"].nunique() if "honeypot" in df.columns else 0,
        "puertos_atacados":  df["dst_port"].nunique() if "dst_port" in df.columns else 0,
    }


def render(df: pd.DataFrame) -> None:
    kpis = _calculate(df)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total attacks",      f"{kpis['total_ataques']:,}")
    c2.metric("Unique IPs",         f"{kpis['ips_unicas']:,}")
    c3.metric("Countries",          f"{kpis['paises']:,}")
    c4.metric("Active honeypots",   f"{kpis['honeypots_activos']:,}")
    c5.metric("Attacked ports",     f"{kpis['puertos_atacados']:,}")
