import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
import time

# --- 1. SETTINGS & AUTHENTICATION ---
st.set_page_config(page_title="Corporate Strategy Protocol", layout="wide")

if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'page' not in st.session_state: st.session_state.page = 'login'
if 'database' not in st.session_state:
    # Pre-populating with diverse mock data across ALL departments and ALL Bands
    projects = ["Sabbatical Leave", "EV Car Lease", "AI Lab Automation", "Inventory Digital Twin", "CRM Overhaul", "Green Packaging"]
    depts = ["HR", "HR", "Operations", "Operations", "Sales", "Service"]
    mock_data = []
    for i in range(120):
        p_idx = i % len(projects)
        band = np.random.choice([5, 6, 7, 8, 9, 10])
        align, feas = np.random.randint(4, 11), np.random.randint(3, 11)
        mock_data.append({
            "Project": projects[p_idx], "Dept": depts[p_idx], "Band": band,
            "Alignment": align, "Feasibility": feas, "Impact": np.random.randint(5, 10),
            "ROI": np.random.randint(5, 10), "Score": (align + feas + 7) / 3,
            "Keywords": "Efficiency, Strategy"
        })
    st.session_state.database = pd.DataFrame(mock_data)

def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=3)
        return r.json() if r.status_code == 200 else None
    except: return None

lottie_loading = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_S6939L.json") 
lottie_success = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_qw88sc7m.json") 

# --- 2. CSS CUSTOMIZATION (Professional Light Theme) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; color: #1e293b; }
    .header-img { width: 100%; height: 200px; object-fit: cover; border-radius: 10px; margin-bottom: 25px; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #0369a1; color: white; }
    .metric-box {
        background-color: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        border: 1px solid #e2e8f0; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PAGE: LOGIN ---
if st.session_state.page == 'login':
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.image("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070&auto=format&fit=crop")
        st.title("Corporate Strategy Protocol")
        with st.form("auth_gate"):
            emp_id = st.text_input("Employee ID (Compulsory)", placeholder="Ex: TF-9923")
            band = st.select_slider("Professional Band", options=[5, 6, 7, 8, 9, 10], value=6)
            dept = st.selectbox("Department", ["HR", "Finance", "Sales/Marketing", "Operations", "Leadership", "Service"])
            if st.form_submit_button("Authenticate & Initialize"):
                if emp_id:
                    st.session_state.user = {"id": emp_id, "band": band, "dept": dept}
                    st.session_state.authenticated = True
                    st.session_state.page = 'portal'
                    if lottie_loading: st_lottie(lottie_loading, height=150)
                    time.sleep(1); st.rerun()
                else: st.error("Authentication Failed: ID is compulsory.")

# --- 4. PAGE: VOTING PORTAL ---
elif st.session_state.page == 'portal':
    if not st.session_state.authenticated: st.rerun()
    st.markdown('<img src="https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=2069&auto=format&fit=crop" class="header-img">', unsafe_allow_html=True)
    st.title("Strategic Input Portal")
    
    with st.sidebar:
        st.title("Login Info")
        st.write(f"**User:** {st.session_state.user['id']} (Band {st.session_state.user['band']})")
        if st.button("Logout"):
            st.session_state.authenticated = False; st.session_state.page = 'login'; st.rerun()
        st.write("---")
        admin_pw = st.text_input("Executive Key", type="password")
        if admin_pw == "EXECUTIVE2026":
            if st.button(" Enter Command Center"):
                st.session_state.page = 'leadership'; st.rerun()

    dept_projects = {"HR": ["Sabbatical Leave", "Car Lease"], "Operations": ["Warehouse Robotics"], "Finance": ["Tax AI"]}
    options = dept_projects.get(st.session_state.user['dept'], ["General Strategy"]) + ["➕ Add Custom Project"]
    selected = st.selectbox("Current Initiatives", options)
    
    project_name, keywords = selected, "Standard"
    if "Add Custom" in selected:
        project_name = st.text_input("Project Name/Question")
        keywords = st.text_input("Keywords (e.g. ESG, Automation)")

    st.write("---")
    c1, c2 = st.columns(2)
    with c1:
        a, f = st.slider("Strategic Alignment", 1, 10, 5), st.slider("Feasibility", 1, 10, 5)
    with c2:
        i, r = st.slider("Impact", 1, 10, 5), st.slider("ROI Confidence", 1, 10, 5)

    if st.button(" TRANSMIT DATA"):
        if project_name:
            new_data = {"Project": project_name, "Dept": st.session_state.user['dept'], 
                       "Band": st.session_state.user['band'], "Score": (a+f+i+r)/4,
                       "Alignment": a, "Feasibility": f, "Impact": i, "ROI": r, "Keywords": keywords}
            st.session_state.database = pd.concat([st.session_state.database, pd.DataFrame([new_data])], ignore_index=True)
            st.success("Submission Secured.")
            if lottie_success: st_lottie(lottie_success, height=100, loop=False)
        else: st.error("Please name the project.")

# --- 5. PAGE: LEADERSHIP ---
elif st.session_state.page == 'leadership':
    st.title(" Executive Command Center")
    if st.sidebar.button("⬅️ Exit Boardroom"):
        st.session_state.page = 'portal'; st.rerun()

    k1, k2, k3 = st.columns(3)
    with k1: st.markdown(f'<div class="metric-box"><h3>{len(st.session_state.database)}</h3><p>Total Data Points</p></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="metric-box"><h3>{st.session_state.database["Score"].mean():.1f}</h3><p>Avg Score</p></div>', unsafe_allow_html=True)
    with k3: st.markdown('<div class="metric-box"><h3>All Bands</h3><p>Perspective Audit</p></div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs([" Strategic Frontier", " Band Audit"])

    with tab1:
        st.subheader("Interactive Strategy Matrix")
        view_mode = st.selectbox("Switch Strategic Lens", ["Global", "Band 5", "Band 6", "Band 7", "Band 8", "Band 9", "Band 10"])
        
        if view_mode == "Global": df_plot = st.session_state.database
        else: df_plot = st.session_state.database[st.session_state.database['Band'] == int(view_mode.split(" ")[1])]

        
        
        fig = px.scatter(df_plot.sort_values("Score", ascending=False).head(25), 
                         x="Alignment", y="Feasibility", size="Score", color="Dept", 
                         hover_name="Project", text="Project", size_max=45,
                         template="plotly_white", 
                         color_discrete_sequence=px.colors.qualitative.Prism)
        
        fig.update_layout(transition_duration=1200, height=600, xaxis=dict(range=[0,11]), yaxis=dict(range=[0,11]))
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Multi-Band Consensus Audit")
        
        fig_radar = go.Figure()
        band_colors = {5: "#ef4444", 6: "#f59e0b", 7: "#10b981", 8: "#3b82f6", 9: "#8b5cf6", 10: "#06b6d4"}
        
        for b in [5, 6, 7, 8, 9, 10]:
            b_data = st.session_state.database[st.session_state.database['Band'] == b]
            if not b_data.empty:
                r_vals = [b_data[c].mean() for c in ['Alignment', 'Feasibility', 'Impact', 'ROI']]
                fig_radar.add_trace(go.Scatterpolar(r=r_vals, theta=['Alignment', 'Feasibility', 'Impact', 'ROI'], 
                                                   fill='toself', name=f'Band {b}', line_color=band_colors[b]))
        
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), template="plotly_white", height=600)
        st.plotly_chart(fig_radar, use_container_width=True)

    with st.expander(" Export Data"):
        if st.text_input("Export Key", type="password") == "PIA2026":
            st.download_button("Download Audit Ledger", data=st.session_state.database.to_csv(index=False), file_name="Strategy_Audit.csv")