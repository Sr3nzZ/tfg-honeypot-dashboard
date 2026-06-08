# app.py
import streamlit as st
from ui import layout
from analytics import data, metrics, geo, temporal, ports, credentials, suricata

layout.configurar_pagina()
dias, honeypot_sel = layout.renderizar_sidebar()

df_raw = data.cargar_datos(dias)

if df_raw.empty:
    st.warning("No data available. Make sure exportar.py is running on the EC2 instance.")
    st.stop()

df = data.filtrar_honeypot(df_raw, honeypot_sel)

layout.renderizar_cabecera(len(df), dias)

metrics.renderizar(df)
geo.renderizar(df)
temporal.renderizar(df)
ports.renderizar(df)
credentials.renderizar(df)
suricata.renderizar(df)

cols_tabla = [c for c in [
    "timestamp", "honeypot", "src_ip", "dst_port",
    "country", "username", "password", "alert_signature",
] if c in df.columns]

with st.expander("📋 Last 100 recorded events", expanded=False):
    from ui.components import tabla
    tabla(df[cols_tabla].head(100).reset_index(drop=True), key="raw_events")

layout.footer("Honeypot Dashboard")
