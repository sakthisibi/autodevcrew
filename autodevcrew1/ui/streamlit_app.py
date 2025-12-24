import streamlit as st
import sys
import os
import time
import json
from datetime import datetime

# Ensure we can import modules from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.engineer_agent import generate_code
from agents.tester_agent import validate_code, generate_tests
from agents.devops_agent import build_and_deploy
from agents.summarizer_agent import summarize_task
from db.storage import save_task, save_code, save_test_log, save_deployment_log, save_final_report, get_task_summary, get_connection

# Page Configuration
st.set_page_config(
    page_title="AutoDevCrew Pro | SDLC Automation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Premium Aesthetics)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    :root {
        --primary: #00f2fe;
        --secondary: #4facfe;
        --bg-dark: #0f172a;
        --card-bg: rgba(30, 41, 59, 0.7);
    }
    
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .sub-header {
        text-align: center;
        color: #94a3b8;
        font-weight: 300;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: var(--card-bg);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    .agent-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 8px;
        background: rgba(79, 172, 254, 0.2);
        color: #4facfe;
        border: 1px solid rgba(79, 172, 254, 0.3);
    }
    
    .status-done {
        color: #10b981;
    }
    
    .status-running {
        color: #3b82f6;
    }
    
    /* Custom tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        color: #94a3b8;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        color: #00f2fe !important;
        border-bottom-color: #00f2fe !important;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function to get history
def get_task_history():
    try:
        conn = get_connection()
        cursor = conn.execute("SELECT id, description, created_at FROM tasks ORDER BY created_at DESC LIMIT 10")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except:
        return []

# Sidebar - Memory & Knowledge Layer
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103855.png", width=100)
    st.title("📂 Memory Layer")
    st.markdown("---")
    
    st.subheader("🕑 Recent Tasks")
    history = get_task_history()
    if history:
        for row in history:
            if st.button(f"Task #{row['id']}: {row['description'][:20]}...", key=f"hist_{row['id']}"):
                st.session_state.selected_task = row['id']
    else:
        st.info("No tasks in memory yet.")
    
    st.markdown("---")
    st.subheader("⚙️ System Status")
    st.success("Engineer: Online")
    st.success("Tester: Online")
    st.success("DevOps: Online")
    st.success("Summarizer: Online")

# Main Interface
st.markdown('<div class="main-header">AutoDevCrew Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Unified SDLC Multi-Agent Ecosystem</div>', unsafe_allow_html=True)

# Layout: Form and Dashboard
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("🎯 New Mission")
    with st.form("task_form", clear_on_submit=False):
        task_desc = st.text_area("What should the crew build today?", placeholder="e.g., Build a login system with password recovery...", height=150)
        project_name = st.text_input("Project Name (optional)", placeholder="Project X")
        priority = st.select_slider("Priority Level", options=["Low", "Medium", "High", "Critical"], value="Medium")
        use_demo = st.checkbox("Demo Mode (Offline Fallback)", value=True)
        submit_btn = st.form_submit_button("🚀 Launch Production Flow")
    st.markdown('</div>', unsafe_allow_html=True)

# Execution Flow
if submit_btn and task_desc:
    # 0. User Input Step
    st.session_state.current_results = {}
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # 1. Engineer Agent
    status_text.markdown("### 👨‍load_config Engineer Agent Activated")
    with st.status("🏗️ Generating Source Code...", expanded=True) as status:
        st.write("Synthesizing code architecture...")
        code = generate_code(task_desc)
        progress_bar.progress(25)
        st.write("Code synthesis complete.")
        status.update(label="✅ Engineer Agent: Code Ready", state="complete", expanded=False)
    
    # 2. Tester Agent
    status_text.markdown("### 🧪 Tester Agent Engaged")
    with st.status("🔍 Analyzing & Validating Code...", expanded=True) as status:
        st.write("Running static analysis...")
        valid, test_results = validate_code(code)
        progress_bar.progress(50)
        if valid:
            st.write("All syntax checks passed.")
            status.update(label="✅ Tester Agent: Validation Passed", state="complete", expanded=False)
        else:
            st.error(f"Logic flaws detected: {test_results}")
            status.update(label="❌ Tester Agent: Validation Failed", state="error", expanded=True)
    
    # 3. DevOps Agent
    status_text.markdown("### 🚀 DevOps Agent Triggered")
    with st.status("📦 Simulating CI/CD Pipeline...", expanded=True) as status:
        st.write("Setting up container environment...")
        deploy_success, deploy_status = False, "Skipped"
        if valid:
            deploy_success, deploy_status = build_and_deploy(code)
            progress_bar.progress(75)
            if deploy_success:
                st.write("Deployment simulation successful.")
                status.update(label="✅ DevOps Agent: Deployed", state="complete", expanded=False)
            else:
                st.write("Deployment encountered errors.")
                status.update(label="❌ DevOps Agent: Build Failed", state="error", expanded=True)
        else:
            status.update(label="⚠️ DevOps Agent: Task Skipped", state="complete", expanded=False)

    # 4. Summarizer Agent
    status_text.markdown("### 📊 Summarizer Agent Compiling Report")
    with st.status("📝 Finalizing Executive Summary...", expanded=True) as status:
        st.write("Aggregating agent outputs...")
        summary = summarize_task(task_desc, code, test_results, deploy_status)
        progress_bar.progress(100)
        status.update(label="✅ Summarizer Agent: Report Finalized", state="complete", expanded=False)
    
    # Save to Memory Layer
    try:
        task_id = save_task(task_desc)
        save_code(task_id, code)
        save_test_log(task_id, test_results)
        save_deployment_log(task_id, deploy_status)
        save_final_report(task_id, summary)
        st.session_state.selected_task = task_id
    except Exception as e:
        st.warning(f"Memory update failed: {e}")

    status_text.empty()
    st.balloons()

# Display Results from History or Current
selected_id = st.session_state.get("selected_task")
if selected_id:
    # Fetch details if not in session current
    conn = get_connection()
    task_row = conn.execute("SELECT * FROM tasks WHERE id = ?", (selected_id,)).fetchone()
    code_row = conn.execute("SELECT * FROM generated_code WHERE task_id = ?", (selected_id,)).fetchone()
    test_row = conn.execute("SELECT * FROM test_logs WHERE task_id = ?", (selected_id,)).fetchone()
    deploy_row = conn.execute("SELECT * FROM deployment_logs WHERE task_id = ?", (selected_id,)).fetchone()
    report_row = conn.execute("SELECT * FROM final_reports WHERE task_id = ?", (selected_id,)).fetchone()
    conn.close()
    
    if task_row:
        with col2:
            st.markdown(f"### 📋 Task #{selected_id}: {task_row['description'][:50]}...")
            
            # Outcome Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📄 Summary Report", "💻 Generated Code", "🧪 Test Logs", "🚀 Deployment"])
            
            with tab1:
                if report_row:
                    report_data = json.loads(report_row['summary'])
                    st.markdown(report_data.get('summary_report', 'No summary available'))
                    
                    st.markdown("---")
                    st.markdown("#### 📊 Mission Core Metrics")
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Code Engine", report_data.get('code_gen', 'N/A'), delta="OPTIMIZED")
                    m2.metric("QA Security", "Pass" if "Checks: PASSED" in str(test_row['test_results']) else "Fail", delta="VERIFIED")
                    m3.metric("Deploy Ops", "Success" if "✅" in str(deploy_row['deployment_status']) else "Failed", delta="STAGED")
                    m4.metric("Privacy", "Strict", delta="LOCAL")
                else:
                    st.warning("Report missing in memory.")
            
            with tab2:
                if code_row:
                    st.markdown("#### Source Artifact")
                    st.code(code_row['code'], language='python')
                    st.download_button("💾 Download Source", code_row['code'], file_name=f"task_{selected_id}.py")
                else:
                    st.info("No code generated for this task.")
            
            with tab3:
                if test_row:
                    st.markdown("#### QA Analyst - Static Analysis")
                    st.info(test_row['test_results'])
                    if "PASSED" in test_row['test_results']:
                        st.success("The code meets the minimum safety and syntax standards.")
                else:
                    st.info("No test logs found.")
                    
            with tab4:
                if deploy_row:
                    st.markdown("#### 🚀 Execution & Deployment Logs")
                    st.code(deploy_row['deployment_status'], language='bash')
                    
                    if "STDOUT" in deploy_row['deployment_status']:
                        st.toast("Code execution verified!", icon="✅")
                else:
                    st.info("No deployment records.")
    else:
        st.error("Could not retrieve task from memory.")
else:
    with col2:
        st.markdown('<div class="metric-card" style="height: 400px; display: flex; align-items: center; justify-content: center; flex-direction: column;">', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/6122/6122588.png", width=150)
        st.markdown("<h3 style='color: #94a3b8;'>Awaiting Mission Parameters...</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b;'>Enter a task on the left to activate the core agents.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>AutoDevCrew v1.0 | Built with LangChain & Autogen Architecture</p>", unsafe_allow_html=True)
