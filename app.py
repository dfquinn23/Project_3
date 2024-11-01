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

    def display_final_report(self):
        """Display the final report from the output directory"""
        try:
            report_pattern = f"output/financial_analysis_*.md"
            latest_file = max(glob.glob(report_pattern), key=os.path.getctime)
            with open(latest_file, 'r') as file:
                report_content = json.loads(file.read())  # Load JSON content

            # Beautify the report content
            st.subheader("Final Report")
            st.markdown(f"**Company Name:** {report_content['company_name']}")
            st.markdown(f"**Ticker Symbol:** {report_content['ticker']}")
            st.markdown("**News Summaries:**")
            for summary in report_content['summaries']:
                st.markdown(f"• {summary}")

            st.markdown("**Financial Report:**")
            st.markdown(report_content['financial_report'])

            # Sentiment Analysis Visualization
            self.visualize_sentiment(report_content['analysis'])

        except FileNotFoundError:
            st.error("Final report not found.")
        except ValueError:
            st.error("No report files found.")

    def visualize_sentiment(self, analysis):
        """Visualize sentiment scores using a gauge chart"""
        average_sentiment = sum(item['sentiment_score'] for item in analysis) / len(analysis)
        
        # Create a gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=average_sentiment,
            title={'text': "Average Sentiment Score"},
            gauge={
                'axis': {'range': [-1, 1]},
                'bar': {'color': "blue"},
                'steps': [
                    {'range': [-1, 0], 'color': "red"},
                    {'range': [0, 1], 'color': "green"}
                ]
            }
        ))

        st.plotly_chart(fig)

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
        Welcome to Agent Sea, your AI-powered investment advisor. 
        Get personalized investment recommendations based on market analysis 
        and your investment preferences.
    """)

    app.display_sidebar()
    app.display_final_report()

if __name__ == "__main__":
    main()
