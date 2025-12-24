"""
AutoDevCrew - HuggingFace Spaces Deployment
Streamlit-based multi-agent SDLC automation system
"""

import os
import sys
import streamlit as st

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment variables for HuggingFace Spaces
os.environ["AUTODEVCREW_MODE"] = "huggingface"
os.environ["HF_SPACE"] = "true"
os.environ["PRIVACY_LEVEL"] = "moderate"  # Moderate privacy on HF
os.environ["LIGHTWEIGHT_MODE"] = "true"
os.environ["QUANTIZATION"] = "int4"

# Import the main Streamlit app
# Since the original streamlit_app.py is in ui/, we'll import it
try:
    # Copy the streamlit app logic here or import it
    from ui.streamlit_app import *
except ImportError:
    # Fallback: create a simple app
    st.set_page_config(page_title="AutoDevCrew 🤖", page_icon="🤖", layout="wide")
    
    st.title("🤖 AutoDevCrew - Multi-Agent SDLC Automation")
    
    st.markdown("""
    ## Welcome to AutoDevCrew!
    
    **Automate your entire software development lifecycle with AI agents.**
    
    ### 🚀 Features
    - 4 Specialized AI Agents (Engineer, Tester, DevOps, Summarizer)
    - Privacy-first architecture with offline operation
    - Real-time monitoring and reporting
    - GitHub Actions integration
    
    ### 📝 Quick Start
    1. Enter your task description below
    2. Click "Execute Task"
    3. Watch agents work in real-time
    4. Get generated code and reports
    """)
    
    with st.form("task_form"):
        task_desc = st.text_area(
            "Enter your task (e.g., Create a login system)",
            height=100,
            placeholder="Describe what you want to build..."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            project_name = st.text_input("Project Name (optional)")
        with col2:
            priority = st.selectbox("Priority", ["low", "medium", "high", "critical"])
        
        submit_btn = st.form_submit_button("🚀 Execute Task", use_container_width=True)
    
    if submit_btn and task_desc:
        with st.spinner("🤖 Agents are working..."):
            try:
                # Import and run
                import asyncio
                from main import AutoDevCrew
                
                # Initialize
                autodevcrew = AutoDevCrew(config_path="config/development.yaml")
                
                # Process task
                async def run_task():
                    return await autodevcrew.process_task(
                        task_desc,
                        project_name=project_name if project_name else None,
                        priority=priority
                    )
                
                result = asyncio.run(run_task())
                
                if result.get("success"):
                    st.success("✅ Task completed successfully!")
                    
                    # Show results in tabs
                    tab1, tab2, tab3, tab4 = st.tabs(["📝 Code", "🧪 Tests", "🚀 Deployment", "📊 Summary"])
                    
                    with tab1:
                        st.code(result.get("generated_code", "No code generated"), language="python")
                    
                    with tab2:
                        st.json(result.get("test_report", {}))
                    
                    with tab3:
                        st.info(result.get("deployment_status", "Not deployed"))
                    
                    with tab4:
                        st.json(result.get("summary", {}))
                else:
                    st.error(f"❌ Task failed: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                import traceback
                with st.expander("Error Details"):
                    st.code(traceback.format_exc())
    
    # Sidebar with info
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        **AutoDevCrew** is a multi-agent system that automates the software development lifecycle.
        
        ### 🤖 Agents
        - **Engineer**: Generates code
        - **Tester**: Validates and tests
        - **DevOps**: Builds and deploys
        - **Summarizer**: Creates reports
        
        ### 🔒 Privacy
        All processing happens in this Space. No external API calls are made in strict mode.
        
        ### 📚 Resources
        - [GitHub](https://github.com/yourusername/autodevcrew)
        - [Docs](https://autodevcrew.readthedocs.io)
        """)
        
        # System status
        st.header("📊 System Status")
        try:
            from core.lightweight_mode import LightweightMode
            lm = LightweightMode()
            report = lm.get_performance_report()
            
            st.metric("RAM", f"{report['hardware_profile']['ram_gb']:.1f} GB")
            st.metric("CPU Cores", report['hardware_profile']['cpu_cores'])
            st.metric("Quantization", report['quantization_level'])
        except:
            st.info("System info unavailable")

if __name__ == "__main__":
    pass  # Streamlit handles execution
