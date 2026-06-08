# app.py
import streamlit as st
from ui import layout
from analytics import data, metrics, geo, temporal, ports, credentials, suricata

layout.configure_page()
dias, honeypot_sel = layout.render_sidebar()

df_raw = data.load_data(dias)

if df_raw.empty:
    st.warning("No data available. Make sure exportar.py is running on the EC2 instance.")
    st.stop()

df = data.filter_honeypot(df_raw, honeypot_sel)

layout.render_header(len(df), dias)

metrics.render(df)
geo.render(df)
temporal.render(df)
ports.render(df)
credentials.render(df)
suricata.render(df)

cols_dataframe = [c for c in [
    "timestamp", "honeypot", "src_ip", "dst_port",
    "country", "username", "password", "alert_signature",
] if c in df.columns]

with st.expander("📋 Last 100 recorded events", expanded=False):
    from ui.components import dataframe
    dataframe(df[cols_dataframe].head(100).reset_index(drop=True), key="raw_events")

layout.footer("Honeypot Dashboard")
