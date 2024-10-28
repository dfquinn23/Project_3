import streamlit as st
import subprocess
from PIL import Image
from a_agents import ResearchAgents
from tools.visualization import SmartVestVisualizer
from d_tools import StockAnalyzer
import os
import glob

class SmartVestWeb:
    def __init__(self, company):
        self.agent_sea = ResearchAgents(company)
        self.visualizer = SmartVestVisualizer()
        self.company = company

    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = None
        if 'analysis_results' not in st.session_state:
            st.session_state.analysis_results = None

    def display_sidebar(self):
        """Create sidebar for user inputs"""
        st.sidebar.header("User Input")
        company_name = st.sidebar.text_input("Enter the company name:", self.company)
        date_range = st.sidebar.date_input("Select date range:", [])
        if st.sidebar.button("Analyze"):
            st.session_state.user_profile = {
                "company_name": company_name,
                "date_range": date_range
            }
            self.run_main_script(company_name)

    def run_main_script(self, company_name):
        """Run the main.py script with the company name as input"""
        try:
            result = subprocess.run(
                ['python', 'main.py'],
                input=company_name,
                text=True,
                capture_output=True
            )
            st.session_state.analysis_results = result.stdout
        except Exception as e:
            st.error(f"Error running main.py: {e}")

    def display_results(self):
        """Display analysis results with visualizations"""
        if st.session_state.analysis_results:
            st.header("Analysis Results")
            st.text(st.session_state.analysis_results)
            self.display_final_report()
        else:
            st.write("No analysis results to display. Please enter a company name and date range, then click 'Analyze'.")

    def display_final_report(self):
        """Display the final report from the output directory"""
        try:
            report_pattern = f"output/financial_analysis_{self.company}_*.md"
            latest_file = max(glob.glob(report_pattern), key=os.path.getctime)
            with open(latest_file, 'r') as file:
                report_content = file.read()
            st.subheader("Final Report")
            st.markdown(report_content)
        except FileNotFoundError:
            st.error("Final report not found.")
        except ValueError:
            st.error("No report files found.")

def main():
    st.set_page_config(
        page_title="Agent Sea - Your AI Investment Advisor",
        page_icon="🌊",
        layout="wide"
    )
    
    # Display logo
    logo = Image.open("tools/logo.png")
    st.image(logo, width=200)
    
    company = "Apple"  # Default company
    app = SmartVestWeb(company)
    app.initialize_session_state()
    
    st.title("Agent Sea - Your AI Investment Advisor")
    st.markdown("""
        Welcome to Agent Sea, your AI-powered investment advisor. 
        Get personalized investment recommendations based on market analysis 
        and your investment preferences.
    """)
    
    app.display_sidebar()
    app.display_results()

if __name__ == "__main__":
    main()
