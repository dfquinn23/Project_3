import streamlit as st
import subprocess
from PIL import Image
import os
import json
from datetime import datetime
from utils.visualization import display_sentiment_clock, beautify_financial_report


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
            
            # Display company name
            company_name = report.get("company_name", "Unknown Company")
            st.write(f"**Company Name:** {company_name}")
            
            # Display final summary
            final_summary = report.get("summaries", [])
            if isinstance(final_summary, list):
                final_summary_cleaned = " ".join(final_summary)  # Join list elements into a single string
            else:
                final_summary_cleaned = final_summary
            
            st.write(f"**Final Summary:** {final_summary_cleaned}")
            
            # Assuming 'average_sentiment_score' is part of the report
            average_sentiment_score = report.get("average_sentiment_score", 0)  # Default to 0 if not found
            
            # Display the sentiment clock
            display_sentiment_clock(average_sentiment_score)  # Pass the sentiment score
            
            # Remove or comment out the beautification of the financial report
            # financial_report = beautify_financial_report(report)
            
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
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(logo, width=200)
    
    # Initialize app
    app = SmartVestWeb()
    
    # Header
    st.title("Agent Sea - AI Investment Advisor")
    st.markdown("""
        <div style='font-family: Roboto, sans-serif;'>
        Welcome to Agent Sea, your AI-powered Investment Advisor. 
        Enter a company name to get started.
        </div>
    """, unsafe_allow_html=True)
    
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
