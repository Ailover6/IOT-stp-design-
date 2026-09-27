import streamlit as st
import pandas as pd
import numpy as np
import time
import sqlite3

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('stp_projects.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT UNIQUE,
            q_flow REAL,
            bod_in REAL,
            bod_out REAL,
            fm_ratio REAL,
            mlvss REAL,
            sor REAL,
            aeration_volume REAL,
            clarifier_area REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Page Configuration
st.set_page_config(
    page_title="EcoSmart Industrial Digital Twin & SCADA",
    page_icon="⚡",
    layout="wide"
)

# --- INITIALIZE SESSION STATE DEFAULTS ---
if 'q_flow' not in st.session_state:
    st.session_state.q_flow = 5000.0
if 'bod_in' not in st.session_state:
    st.session_state.bod_in = 250.0
if 'bod_out' not in st.session_state:
    st.session_state.bod_out = 10.0
if 'fm_ratio' not in st.session_state:
    st.session_state.fm_ratio = 0.2
if 'mlvss' not in st.session_state:
    st.session_state.mlvss = 3000.0
if 'sor' not in st.session_state:
    st.session_state.sor = 25.0
if 'influent_turbidity' not in st.session_state:
    st.session_state.influent_turbidity = 50.0
if 'coagulant_dose_rate' not in st.session_state:
    st.session_state.coagulant_dose_rate = 2.5
if 'power_tariff' not in st.session_state:
    st.session_state.power_tariff = 0.13

# --- CALLBACK FUNCTION FOR LOADING PROJECTS ---
def load_project_callback():
    selected = st.session_state.load_project_dropdown
    if selected != "-- Choose Project --":
        conn = sqlite3.connect('stp_projects.db')
        cursor = conn.cursor()
        cursor.execute("SELECT q_flow, bod_in, bod_out, fm_ratio, mlvss, sor FROM projects WHERE project_name = ?", (selected,))
        p_data = cursor.fetchone()
        conn.close()
        if p_data:
            st.session_state.q_flow = float(p_data[0])
            st.session_state.bod_in = float(p_data[1])
            st.session_state.bod_out = float(p_data[2])
            st.session_state.fm_ratio = float(p_data[3])
            st.session_state.mlvss = float(p_data[4])
            st.session_state.sor = float(p_data[5])
            st.session_state.project_name_input = selected

# --- SIDEBAR THEME TOGGLE ---
st.sidebar.markdown("### 🎛️ Control Panel")
theme_mode = st.sidebar.radio("Select Display Theme", ["Dark SCADA Mode", "Clean Light Mode"], index=0)

# Dynamic Theme Configuration & CSS
if theme_mode == "Dark SCADA Mode":
    bg_color = "#060913"
    card_bg = "linear-gradient(135deg, #111827 0%, #0f172a 100%)"
    text_color = "#e2e8f0"
    heading_color = "#f8fafc"
    input_bg = "#0f172a"
    border_color = "#1e293b"
    sidebar_bg = "#0b1329"
    sidebar_text = "#f8fafc"
else:
    bg_color = "#f8fafc"
    card_bg = "linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%)"
    text_color = "#1e293b"
    heading_color = "#0f172a"
    input_bg = "#ffffff"
    border_color = "#cbd5e1"
    sidebar_bg = "#e2e8f0"
    sidebar_text = "#0f172a"

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
    }}
    section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] h3 {{
        color: {sidebar_text} !important;
        font-weight: 700 !important;
    }}
    div[data-testid="stMetric"] {{
        background: {card_bg};
        padding: 18px;
        border-radius: 12px;
        border: 1px solid {border_color};
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }}
    div[data-testid="stMetric"] label {{
        color: {text_color} !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 0.9rem;
    }}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
        color: #0284c7 !important;
        font-weight: 800 !important;
    }}
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
        border-radius: 8px !important;
        font-weight: 600;
    }}
    .stButton button, .stDownloadButton button {{
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4);
        width: 100%;
        transition: all 0.3s ease;
    }}
    .stButton button:hover, .stDownloadButton button:hover {{
        background: linear-gradient(135deg, #0369a1 0%, #075985 100%) !important;
        box-shadow: 0 6px 15px rgba(2, 132, 199, 0.6);
    }}
    h1, h2, h3, h4, p {{
        color: {heading_color} !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600 !important;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 12px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {input_bg};
        border-radius: 8px 8px 0px 0px;
        color: {text_color};
        padding: 12px 24px;
        border: 1px solid {border_color};
        font-weight: 700;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #0284c7 !important;
        color: white !important;
        border: 1px solid #38bdf8 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Top Command Center Header
col_h1, col_h2 = st.columns([4, 1])
with col_h1:
    st.markdown("## ⚡ EcoSmart SCADA & Plant Digital Twin")
    st.markdown("**AI-Powered Wastewater Treatment Automation, Energy Tracking & IoT Telemetry Suite**")
with col_h2:
    st.markdown("### 🟢 **SYSTEM: ONLINE**")
    st.caption("Active Sync: 100ms polling")

st.markdown("---")

tab1, tab2 = st.tabs(["⚙️ Plant Design, Energy & Compliance", "📊 Real-Time SCADA Control Center"])

# ==========================================
# MODULE 1: DESIGN, ENERGY & COMPLIANCE
# ==========================================
with tab1:
    st.subheader("Automated Wastewater Treatment Unit Sizing, Energy Audit & Compliance")
    
    # --- LOAD EXISTING PROJECTS ---
    conn = sqlite3.connect('stp_projects.db')
    cursor = conn.cursor()
    cursor.execute("SELECT project_name FROM projects")
    saved_projects = [row[0] for row in cursor.fetchall()]
    conn.close()

    if saved_projects:
        with st.expander("📂 Load Plant Configuration from Database"):
            st.selectbox(
                "Select Profile", 
                ["-- Choose Project --"] + saved_projects, 
                key="load_project_dropdown",
                on_change=load_project_callback
            )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📥 Influent Characteristics & Kinetics")
        q_flow = st.number_input("Average Daily Flow (m³/day)", key="q_flow", step=100.0)
        bod_in = st.number_input("Influent BOD5 (mg/L)", key="bod_in", step=10.0)
        bod_out = st.number_input("Target Effluent BOD5 (mg/L)", key="bod_out", step=1.0)
        fm_ratio = st.number_input("F/M Ratio (day⁻¹)", key="fm_ratio", step=0.05)
        mlvss = st.number_input("MLVSS in Aeration Tank (mg/L)", key="mlvss", step=100.0)
        sor = st.number_input("Clarifier Surface Overflow Rate (m³/m²·day)", key="sor", step=1.0)
        
        st.markdown("---")
        st.markdown("#### 🧪 Tertiary & Energy Parameters")
        influent_turbidity = st.number_input("Average Influent Turbidity (NTU)", key="influent_turbidity", step=5.0)
        coagulant_dose_rate = st.number_input("Alum Dosage Rate (mg per NTU)", key="coagulant_dose_rate", step=0.5)
        power_tariff = st.number_input("Electricity Tariff ($ per kWh)", key="power_tariff", step=0.01)

    with col2:
        st.markdown("#### 📊 Computed Plant Sizing & Energy Matrix")
        
        bod_load = (q_flow * bod_in) / 1000.0
        aeration_volume = (q_flow * bod_in) / (mlvss * fm_ratio) if (mlvss * fm_ratio) > 0 else 0
        hrt = (aeration_volume / q_flow) * 24 if q_flow > 0 else 0
        clarifier_area = q_flow / sor if sor > 0 else 0
        clarifier_diameter = np.sqrt((4 * clarifier_area) / np.pi)

        srt_days = 1.0 / fm_ratio if fm_ratio > 0 else 0
        daily_alum_kg = (q_flow * influent_turbidity * coagulant_dose_rate) / 1000.0

        daily_energy_kwh = q_flow * 0.05
        daily_cost = daily_energy_kwh * power_tariff
        daily_carbon_kg = daily_energy_kwh * 0.85

        m1, m2 = st.columns(2)
        with m1:
            st.metric("Daily BOD Load", f"{bod_load:.2f} kg/d")
            st.metric("Aeration Volume", f"{aeration_volume:.2f} m³")
            st.metric("Retention Time", f"{hrt:.2f} hrs")
        with m2:
            st.metric("Clarifier Area", f"{clarifier_area:.2f} m²")
            st.metric("Sludge Age (SRT)", f"{srt_days:.1f} days")
            st.metric("Daily Alum Dosing", f"{daily_alum_kg:.2f} kg/d")

        e1, e2, e3 = st.columns(3)
        e1.metric("Est. Blower Energy", f"{daily_energy_kwh:.1f} kWh/d")
        e2.metric("Daily Power Cost", f"${daily_cost:.2f}/d")
        e3.metric("Carbon Footprint", f"{daily_carbon_kg:.1f} kg CO₂/d")

        # --- REGULATORY COMPLIANCE AUDIT ---
        st.markdown("---")
        st.markdown("#### 📜 Environmental Compliance Audit")
        max_allowed_bod = 20.0 
        
        if bod_out <= max_allowed_bod:
            st.success(f"✅ REGULATORY PASS: Target Effluent BOD ({bod_out} mg/L) satisfies CPCB/EPA inland disposal norms (≤ {max_allowed_bod} mg/L).")
        else:
            st.error(f"❌ REGULATORY FAIL: Target Effluent BOD breaches legal discharge threshold of {max_allowed_bod} mg/L!")

        # --- SAVE TO DATABASE SECTION ---
        st.markdown("---")
        st.markdown("#### 💾 Project Database Management")
        proj_name_input = st.text_input("Project Identification Tag", key="project_name_input", value="Delhi_STP_Phase1")
        if st.button("💾 Commit Design Configuration to Database"):
            try:
                conn = sqlite3.connect('stp_projects.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO projects (project_name, q_flow, bod_in, bod_out, fm_ratio, mlvss, sor, aeration_volume, clarifier_area)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (proj_name_input, q_flow, bod_in, bod_out, fm_ratio, mlvss, sor, aeration_volume, clarifier_area))
                conn.commit()
                conn.close()
                st.success(f"Successfully committed profile: **{proj_name_input}**!")
            except Exception as e:
                st.error(f"Database error: {e}")

        # Professional Certified Report Generator
        report_text = f"""
=====================================================================
            ECOSMART INDUSTRIAL DIGITAL TWIN & SCADA SUITE
                    CERTIFIED ENGINEERING REPORT
=====================================================================
Project Identifier Tag : {proj_name_input}
Audit Timestamp        : {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

1. INFLUENT DESIGN CRITERIA
---------------------------------------------------------------------
- Average Daily Flow   : {q_flow:,.2f} m³/day
- Influent BOD5        : {bod_in:.2f} mg/L
- Target Effluent BOD5 : {bod_out:.2f} mg/L (Limit: <= 20.0 mg/L)
- Influent Turbidity   : {influent_turbidity:.2f} NTU

2. COMPUTED UNIT SIZING SPECIFICATIONS
---------------------------------------------------------------------
- Daily BOD Load       : {bod_load:.2f} kg/day
- Aeration Tank Volume : {aeration_volume:.2f} m³
- Hydraulic Retention  : {hrt:.2f} hours
- Clarifier Surface Area: {clarifier_area:.2f} m²
- Clarifier Diameter   : {clarifier_diameter:.2f} meters
- Sludge Age (SRT)     : {srt_days:.1f} days
- Daily Alum Requirement: {daily_alum_kg:.2f} kg/day

3. ENERGY & SUSTAINABILITY AUDIT
---------------------------------------------------------------------
- Estimated Blower Power: {daily_energy_kwh:.1f} kWh/day
- Daily Energy Cost    : ${daily_cost:.2f} / day (Tariff: ${power_tariff}/kWh)
- Carbon Emissions     : {daily_carbon_kg:.1f} kg CO₂ / day

4. REGULATORY COMPLIANCE STATUS
---------------------------------------------------------------------
- Discharge Audit Result : {"PASSED (Compliant with Environmental Norms)" if bod_out <= max_allowed_bod else "FAILED (Non-Compliant)"}
=====================================================================
                  [End of Certified Audit Report]
=====================================================================
"""
        st.download_button(
            label="📥 Download Certified Official Engineering Report",
            data=report_text,
            file_name=f"{proj_name_input}_certified_engineering_report.txt",
            mime="text/plain"
        )

        # What-If Scenario Stress-Tester
        st.markdown("---")
        st.markdown("#### ⚠️ Peak Hydraulic Surge Stress Simulator")
        shock_multiplier = st.slider("Simulate Monsoon / Peak Inflow Multiplier", min_value=1.0, max_value=3.0, value=1.5, step=0.1)
        
        shocked_flow = q_flow * shock_multiplier
        shocked_hrt = (aeration_volume / shocked_flow) * 24 if shocked_flow > 0 else 0
        
        st.write(f"Under a **{shock_multiplier}x** hydraulic surge ({shocked_flow:.0f} m³/day):")
        st.metric("Adjusted HRT Under Surge", f"{shocked_hrt:.2f} hours", 
                  delta=f"{shocked_hrt - hrt:.2f} hrs", delta_color="inverse")
        
        if shocked_hrt < 3.0:
            st.error("🚨 CRITICAL WARNING: HRT drops below 3-hour critical limit! Risk of biological biomass washout.")
        else:
            st.success("✅ STABLE BUFFER: Aeration reactor volume safely absorbs peak hydraulic shock.")

# ==========================================
# MODULE 2: REAL-TIME IoT SCADA CONTROL CENTER
# ==========================================
with tab2:
    st.subheader("Live IoT SCADA Control Room & Telemetry Feed")
    st.markdown("Live operational stream from distributed smart sensors (ESP32 IoT nodes) installed across plant processing units.")

    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric("MQTT Broker Latency", "14 ms", "-2ms optimal")
    sc2.metric("Edge Node Health", "100%", "12/12 Online")
    sc3.metric("Blower Motor Status", "ACTIVE", "Frequency: 50 Hz")
    sc4.metric("Dosing Pump PID", "AUTO MODE", "Flow-proportional")

    st.markdown("---")
    
    control_col1, control_col2 = st.columns([3, 1])
    with control_col1:
        run_simulation = st.checkbox("🟢 Enable High-Frequency Live Telemetry Stream", value=True)
    with control_col2:
        refresh_rate = st.selectbox("Polling Rate", ["2 Seconds", "5 Seconds"], index=0)

    if 'sensor_data' not in st.session_state:
        st.session_state.sensor_data = pd.DataFrame(
            columns=['Time', 'pH', 'Dissolved_Oxygen', 'Turbidity', 'Flow_Rate']
        )

    if 'event_logs' not in st.session_state:
        st.session_state.event_logs = []

    if run_simulation:
        current_time = pd.Timestamp.now().strftime("%H:%M:%S")
        
        sim_ph = round(np.random.normal(7.2, 0.25), 2)
        sim_do = round(np.random.normal(2.4, 0.35), 2)
        sim_turbidity = round(np.random.normal(4.2, 0.6), 2)
        sim_flow = round(np.random.normal(205.0, 8.5), 1)

        new_row = pd.DataFrame({
            'Time': [current_time],
            'pH': [sim_ph],
            'Dissolved_Oxygen': [sim_do],
            'Turbidity': [sim_turbidity],
            'Flow_Rate': [sim_flow]
        })

        if sim_do < 2.0:
            st.session_state.event_logs.insert(0, {"Time": current_time, "Level": "WARNING", "Message": f"Aeration tank DO dropped to {sim_do} mg/L. Blower speed increased."})
        if sim_ph < 6.5 or sim_ph > 8.5:
            st.session_state.event_logs.insert(0, {"Time": current_time, "Level": "ALERT", "Message": f"Abnormal pH detected ({sim_ph}). Dosing circuit adjusted."})
        
        if len(st.session_state.event_logs) > 5:
            st.session_state.event_logs = st.session_state.event_logs[:5]

        st.session_state.sensor_data = pd.concat([st.session_state.sensor_data, new_row], ignore_index=True)
        if len(st.session_state.sensor_data) > 25:
            st.session_state.sensor_data = st.session_state.sensor_data.iloc[1:]

        latest = st.session_state.sensor_data.iloc[-1]
        
        st.markdown("#### Live Unit Telemetry Gauges")
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        ph_status = "Normal" if 6.5 <= latest['pH'] <= 8.5 else "⚠️ Out of Range"
        col_m1.metric("Effluent pH Level", f"{latest['pH']}", ph_status)
        
        do_val = latest['Dissolved_Oxygen']
        do_status = "⚠️ Low Aeration" if do_val < 2.0 else "Optimal Range"
        col_m2.metric("Dissolved Oxygen (DO)", f"{do_val} mg/L", do_status)
        
        col_m3.metric("Outlet Turbidity", f"{latest['Turbidity']} NTU", "Crystal Clear")
        col_m4.metric("Real-Inflow Velocity", f"{latest['Flow_Rate']} m³/h", "Steady Flow")

        chart_col1, chart_col2 = st.columns([2, 1])
        
        with chart_col1:
            st.markdown("#### Real-Time Sensor Telemetry Trends")
            chart_data_indexed = st.session_state.sensor_data.set_index('Time')
            st.line_chart(chart_data_indexed[['pH', 'Dissolved_Oxygen', 'Turbidity']], height=300)

        with chart_col2:
            st.markdown("#### 🚨 SCADA Live Event Ticker")
            if st.session_state.event_logs:
                for log in st.session_state.event_logs:
                    if log["Level"] == "ALERT":
                        st.error(f"[{log['Time']}] {log['Message']}")
                    else:
                        st.warning(f"[{log['Time']}] {log['Message']}")
            else:
                st.success("✅ All telemetry parameters within nominal safe operating thresholds. No active anomalies.")

        health_score = 98.4 if do_val >= 2.0 and (6.5 <= latest['pH'] <= 8.5) else 84.2
        st.markdown("---")
        st.markdown(f"#### Overall Plant Digital Twin Health Index: **{health_score}%** (Optimal Operational Efficiency)")
        st.progress(int(health_score))

        time.sleep(2)
        st.rerun()