import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt

class SmartVestVisualizer:
    def create_sentiment_clock(self, sentiment_score: float) -> go.Figure:
        """Create a gauge chart showing sentiment score"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=sentiment_score * 100,
            title={'text': "Sentiment Score"},
            gauge={
                'axis': {'range': [-100, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [-100, 0], 'color': "red"},
                    {'range': [0, 100], 'color': "green"}
                ]
            }
        ))
        return fig

    def load_final_report(self, file_path):
        try:
            with open(file_path, 'r') as file:
                report = file.read()
            st.subheader("Final Report")
            st.text(report)
        except FileNotFoundError:
            st.error("Final report not found.")

def display_sentiment_clock(sentiment_score: float):
    """Display the sentiment clock using Plotly"""
    visualizer = SmartVestVisualizer()
    fig = visualizer.create_sentiment_clock(sentiment_score)
    st.plotly_chart(fig)  # Display the Plotly figure in Streamlit

def beautify_financial_report(report):
    # Example implementation to beautify the financial report
    st.subheader("Financial Report")
    
    # Assuming 'report' is a dictionary with financial data
    # Here you would implement the logic to format and beautify the report
    # For demonstration, we will just display the report in a table format
    if isinstance(report, dict):
        st.table(report)  # Display the report as a table
    else:
        st.write("Invalid report format.")
