import streamlit as st
import pandas as pd
import time
from ui import layout
from analytics import data, metrics, geo, temporal, ports, credentials, suricata
 
layout.configurar_pagina()
 
@st.cache_data(ttl=3600)
def get_all_data():
    return data.load_all()
 
with st.spinner("Loading data..."):
    df_all = get_all_data()
 
if df_all.empty:
    st.warning("No data available.")
    st.stop()
 
df_all = df_all.sort_values("timestamp").reset_index(drop=True)
 
DURACION_REAL_SEG = 30 * 60          
total_eventos = len(df_all)
t_inicio_datos = df_all["timestamp"].min()
t_fin_datos    = df_all["timestamp"].max()
rango_datos_seg = (t_fin_datos - t_inicio_datos).total_seconds()
factor_tiempo   = rango_datos_seg / DURACION_REAL_SEG  
 
with st.sidebar:
    st.title("Honeypot Dashboard")
    st.caption("Real-time threat analysis")
    st.divider()
    st.info("📅 Data from May 27 – Jun 3, 2026")
    st.caption("Replaying attack data in real-time simulation.")
    st.divider()
 
    honeypot_sel = st.selectbox("Honeypot", ["All"] + sorted(df_all["honeypot"].dropna().unique().tolist()))
 
    if st.button("▶ Start / Restart", use_container_width=True):
        st.session_state["running"] = True
        st.session_state["start_real_time"] = time.time()
        st.session_state["t_cursor"] = t_inicio_datos
 
    if st.button("⏹ Stop", use_container_width=True):
        st.session_state["running"] = False
 
if "running" not in st.session_state:
    st.session_state["running"] = False
if "start_real_time" not in st.session_state:
    st.session_state["start_real_time"] = None
if "t_cursor" not in st.session_state:
    st.session_state["t_cursor"] = t_inicio_datos
 
if st.session_state["running"] and st.session_state["start_real_time"]:
    elapsed_real = time.time() - st.session_state["start_real_time"]
    elapsed_datos = pd.Timedelta(seconds=elapsed_real * factor_tiempo)
    t_cursor = t_inicio_datos + elapsed_datos
    t_cursor = min(t_cursor, t_fin_datos)
    st.session_state["t_cursor"] = t_cursor
else:
    t_cursor = st.session_state["t_cursor"]
 
df = df_all[df_all["timestamp"] <= t_cursor]
if honeypot_sel != "All":
    df = df[df["honeypot"] == honeypot_sel]
 
st.title("Honeypot Dashboard")
 
col_info, col_clock = st.columns([3, 1])
with col_info:
    st.caption(f"{len(df):,} events · up to {t_cursor.strftime('%Y-%m-%d %H:%M:%S UTC')}")
with col_clock:
    pct = min(100, int((t_cursor - t_inicio_datos).total_seconds() / rango_datos_seg * 100))
    st.progress(pct, text=f"{pct}%")
 
st.divider()
 
if df.empty:
    st.info("Press ▶ Start to begin the simulation.")
else:
    metrics.renderizar(df)
    geo.renderizar(df)
    temporal.renderizar(df)
    ports.renderizar(df)
    credentials.renderizar(df)
    suricata.renderizar(df)
 
    with st.expander("📋 Last 100 recorded events", expanded=False):
        cols_tabla = [c for c in ["timestamp", "honeypot", "src_ip", "dst_port",
                                   "country", "username", "password", "alert_signature"]
                      if c in df.columns]
        from ui.components import tabla
        tabla(df[cols_tabla].tail(100).reset_index(drop=True), key="raw_events")
 
layout.footer("Honeypot Dashboard")
 
if st.session_state["running"] and t_cursor < t_fin_datos:
    time.sleep(1)
    st.rerun()
elif st.session_state["running"] and t_cursor >= t_fin_datos:
    st.session_state["running"] = False
    st.success("✅ Simulation complete.")