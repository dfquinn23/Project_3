import streamlit as st
import subprocess
from PIL import Image
import os
import json
from datetime import datetime

class SmartVestWeb:
    def __init__(self):
        self.initialize_session_state()

    def initialize_session_state(self):
        if 'analysis_results' not in st.session_state:
            st.session_state.analysis_results = None

    def run_analysis(self, company_name):
        with st.spinner("Analyzing..."):
            try:
                # Create output directory if it doesn't exist
                os.makedirs("output", exist_ok=True)
                
                # Run main.py with company name
                result = subprocess.run(
                    ['python', 'main.py'],
                    input=company_name,
                    text=True,
                    capture_output=True
                )
                
                st.session_state.analysis_results = True
                
                # Debug information
                st.write("Analysis complete!")
                if result.stderr:
                    st.write("Errors:", result.stderr)
                
            except Exception as e:
                st.error(f"Error during analysis: {e}")

    def display_report(self):
        try:
            # Get the latest report file
            output_dir = "output"
            files = [f for f in os.listdir(output_dir) if f.endswith('.json')]
            
            if not files:
                st.warning("No analysis reports found.")
                return
                
            latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(output_dir, x)))
            file_path = os.path.join(output_dir, latest_file)
            
            # Read and display the report
            with open(file_path, 'r') as f:
                report = json.load(f)
                
            st.subheader("Analysis Report")
            st.write(report)
            
        except Exception as e:
            st.error(f"Error displaying report: {e}")

def load_css():
    with open("utils/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Agent Sea - Your AI Investment Advisor",
        page_icon="🌊",
        layout="wide"
    )
    
    load_css()  # Load custom CSS
    
    # Display logo
    logo = Image.open("utils/logo.png")
    st.image(logo, width=200)
    
    # Initialize app
    app = SmartVestWeb()
    
    # Header
    st.title("Agent Sea - AI Investment Advisor")
    st.markdown("""
        Welcome to Agent Sea, your AI-powered investment advisor. 
        Enter a company name to get started.
    """)
    
    # Sidebar inputs
    with st.sidebar:
        company_name = st.text_input("Enter company name:", "Apple")
        if st.button("Analyze"):
            app.run_analysis(company_name)
    
    # Display report if analysis has been run
    if st.session_state.analysis_results:
        app.display_report()

if __name__ == "__main__":
    main()
