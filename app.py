import streamlit as st
import pandas as pd
import time
from ui import layout
from analytics import data, metrics, geo, temporal, ports, credentials, suricata, honeypot
 
layout.configure_page()
 
T_INICIO          = pd.Timestamp("2026-05-27T18:55:02Z", tz="UTC")
T_FIN             = pd.Timestamp("2026-06-04T23:59:59Z", tz="UTC")
RANGO_SEG         = (T_FIN - T_INICIO).total_seconds()
DURACION_REAL_SEG = 30 * 60
VENTANA_DATOS     = pd.Timedelta(hours=1)
TICK_REAL_SEG     = max(1, int(VENTANA_DATOS.total_seconds() / (RANGO_SEG / DURACION_REAL_SEG)))
 
for key, default in [
    ("running", False),
    ("t_cursor", T_INICIO),
    ("df_acumulado", pd.DataFrame()),
    ("ultimo_tick", None),
    ("country_sel", "All"),
    ("country_options", ["All"]),
]:
    if key not in st.session_state:
        st.session_state[key] = default

df_preview = st.session_state["df_acumulado"].copy()

honeypot_sel_preview = st.session_state.get("honeypot_sel", "All")

if honeypot_sel_preview != "All" and not df_preview.empty:
    df_preview = data.filter_honeypot(df_preview, honeypot_sel_preview)

if not df_preview.empty and "country" in df_preview.columns:
    st.session_state["country_options"] = (
        ["All"] + sorted(df_preview["country"].dropna().unique().tolist())
    )
else:
    st.session_state["country_options"] = ["All"]

    
with st.sidebar:
    st.title("Honeypot Dashboard")
    st.caption("Real-time threat analysis")
    st.divider()
    st.info("Data from May 27 – Jun 3, 2026")
    st.caption(
        "Replaying attack data in real-time simulation. "
        "The system is designed for live updates via EC2 exporter. "
    )
    st.caption(        
        "Not supported because of database size limitations, but the code structure allows for it with minimal adjustments. "
    )
    st.divider()
 
    honeypot_sel = st.selectbox(
        "Honeypot selector",
        ["All", "p0f", "suricata", "honeytrap", "fatt", "nginx",
         "dionaea", "cowrie", "miniprint", "tanner", "h0neytr4p",
         "adbhoney", "ciscoasa", "conpot", "mailoney",
         "redishoneypot", "honeyaml", "elasticpot", "heralding"]
    )

    country_sel = st.selectbox(
        "Country selector",
        options=st.session_state.get("country_options", ["All"]),
        key="country_sel"
    )
 
    col_start, col_stop = st.columns(2)
    with col_start:
        if st.button("▶ Start", use_container_width=True):
            st.session_state["running"]      = True
            st.session_state["t_cursor"]     = T_INICIO
            st.session_state["df_acumulado"] = pd.DataFrame()
            st.session_state["ultimo_tick"]  = time.time()
    with col_stop:
        if st.button("⏹ Stop", use_container_width=True):
            st.session_state["running"] = False
 
@st.fragment(run_every=TICK_REAL_SEG if st.session_state["running"] else None)
def dashboard():
    if st.session_state["running"] and st.session_state["ultimo_tick"]:
        ahora = time.time()
        if ahora - st.session_state["ultimo_tick"] >= TICK_REAL_SEG:
            t_cursor = st.session_state["t_cursor"]
            hasta    = min(t_cursor + VENTANA_DATOS, T_FIN)
 
            with st.spinner(f"Loading {t_cursor.strftime('%b %d %H:%M')} – {hasta.strftime('%b %d %H:%M')}..."):
                nuevos = data.load_window(
                    desde=t_cursor.isoformat(),
                    hasta=hasta.isoformat(),
                )
 
            if not nuevos.empty:
                st.session_state["df_acumulado"] = pd.concat(
                    [st.session_state["df_acumulado"], nuevos],
                    ignore_index=True
                )
 
            st.session_state["t_cursor"]    = hasta
            st.session_state["ultimo_tick"] = ahora
 
            if hasta >= T_FIN:
                st.session_state["running"] = False
                st.success("Simulation complete — all attacks replayed.")
 
    df = st.session_state["df_acumulado"].copy()
    t_cursor = st.session_state["t_cursor"]

    if honeypot_sel != "All" and not df.empty:
        df = data.filter_honeypot(df, honeypot_sel)
        
    if st.session_state["country_sel"] != "All" and not df.empty:
        df = df[df["country"] == st.session_state["country_sel"]]

    st.title("Honeypot Dashboard")
    col_info, col_prog = st.columns([3, 1])
    with col_info:
        st.caption(f"{len(df):,} events · simulating up to {t_cursor.strftime('%Y-%m-%d %H:%M UTC')}")
    with col_prog:
        pct = int((t_cursor - T_INICIO).total_seconds() / RANGO_SEG * 100)
        st.progress(min(pct, 100), text=f"{min(pct, 100)}%")
    st.divider()
 
    if df.empty:
        st.info("Press ▶ Start to begin the simulation.")
    else:
        metrics.render(df)
        geo.render(df)
        temporal.render(df)
        honeypot.render(df)
        ports.render(df)
        credentials.render(df)
        suricata.render(df)
 
        with st.expander("Last 100 recorded events", expanded=False):
            cols_dataframe = [c for c in [
                "timestamp", "honeypot", "src_ip", "dst_port",
                "country", "username", "password", "alert_signature"
            ] if c in df.columns]
            from ui.components import dataframe
            dataframe(df[cols_dataframe].tail(100).reset_index(drop=True), key="raw_events")
  
dashboard()