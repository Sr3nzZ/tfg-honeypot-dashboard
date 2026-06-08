import streamlit as st
import pandas as pd
import time
from datetime import timezone
from ui import layout
from analytics import data, metrics, geo, temporal, ports, credentials, suricata
 
layout.configure_page()
 
T_INICIO = pd.Timestamp("2026-05-27T17:00:00Z", tz="UTC")
T_FIN    = pd.Timestamp("2026-06-03T23:59:59Z", tz="UTC")
RANGO_SEG = (T_FIN - T_INICIO).total_seconds()
DURACION_REAL_SEG = 30 * 60  # 30 minutos
FACTOR = RANGO_SEG / DURACION_REAL_SEG  # seg de datos por seg real
INTERVALO_CONSULTA_SEG = 5   # consultar Supabase cada 5 segundos reales
 
with st.sidebar:
    st.title("Honeypot Dashboard")
    st.caption("Real-time threat analysis")
    st.divider()
    st.info("📅 Data from May 27 – Jun 3, 2026")
    st.caption(
        "Replaying attack data in real-time simulation. "
        "The system is designed for live updates via EC2 exporter."
    )
    st.divider()
 
    honeypot_sel = st.selectbox(
        "Honeypot",
        ["All"] + ["p0f", "suricata", "honeytrap", "fatt", "nginx",
                   "dionaea", "cowrie", "miniprint", "tanner", "h0neytr4p",
                   "adbhoney", "ciscoasa", "conpot", "mailoney",
                   "redishoneypot", "honeyaml", "elasticpot", "heralding"]
    )
 
    col_start, col_stop = st.columns(2)
    with col_start:
        if st.button("▶ Start", use_container_width=True):
            st.session_state["running"]          = True
            st.session_state["start_real_time"]  = time.time()
            st.session_state["t_cursor"]         = T_INICIO
            st.session_state["df_acumulado"]     = pd.DataFrame()
            st.session_state["ultima_consulta"]  = T_INICIO
    with col_stop:
        if st.button("⏹ Stop", use_container_width=True):
            st.session_state["running"] = False
 
for key, default in [
    ("running",         False),
    ("start_real_time", None),
    ("t_cursor",        T_INICIO),
    ("df_acumulado",    pd.DataFrame()),
    ("ultima_consulta", T_INICIO),
]:
    if key not in st.session_state:
        st.session_state[key] = default
 
if st.session_state["running"] and st.session_state["start_real_time"]:
    elapsed_real = time.time() - st.session_state["start_real_time"]
    elapsed_datos = pd.Timedelta(seconds=elapsed_real * FACTOR)
    t_cursor = T_INICIO + elapsed_datos
    t_cursor = min(t_cursor, T_FIN)
    st.session_state["t_cursor"] = t_cursor
else:
    t_cursor = st.session_state["t_cursor"]
 
ultima = st.session_state["ultima_consulta"]
if st.session_state["running"] and t_cursor > ultima:
    nuevos = data.load_window(
        desde=ultima.isoformat(),
        hasta=t_cursor.isoformat(),
    )
    st.write(f"DEBUG: desde={ultima} hasta={t_cursor} nuevos={len(nuevos)}")

    if not nuevos.empty:
        st.session_state["df_acumulado"] = pd.concat(
            [st.session_state["df_acumulado"], nuevos],
            ignore_index=True
        )
    st.session_state["ultima_consulta"] = t_cursor
 
df = st.session_state["df_acumulado"]
if honeypot_sel != "All" and not df.empty:
    df = df[df["honeypot"] == honeypot_sel]
 
st.title("Honeypot Dashboard")
col_info, col_prog = st.columns([3, 1])
with col_info:
    ts_str = t_cursor.strftime("%Y-%m-%d %H:%M UTC")
    st.caption(f"{len(df):,} events · simulating {ts_str}")
with col_prog:
    pct = int((t_cursor - T_INICIO).total_seconds() / RANGO_SEG * 100)
    st.progress(min(pct, 100), text=f"{min(pct,100)}%")
st.divider()
 
if df.empty:
    st.info("Press ▶ Start to begin the simulation.")
else:
    metrics.render(df)
    geo.render(df)
    temporal.render(df)
    ports.render(df)
    credentials.render(df)
    suricata.render(df)
 
    with st.expander("📋 Last 100 recorded events", expanded=False):
        cols_tabla = [c for c in ["timestamp", "honeypot", "src_ip", "dst_port",
                                   "country", "username", "password", "alert_signature"]
                      if c in df.columns]
        from ui.components import tabla
        tabla(df[cols_tabla].tail(100).reset_index(drop=True), key="raw_events")
 
layout.footer("🍯 Honeypot Dashboard · TFG · Data May 27 – Jun 3, 2026 · Designed for real-time updates via EC2 exporter")
 
if st.session_state["running"]:
    if t_cursor < T_FIN:
        time.sleep(INTERVALO_CONSULTA_SEG)
        st.rerun()
    else:
        st.session_state["running"] = False
        st.success("✅ Simulation complete — all attacks replayed.")