import plotly.graph_objects as go
import streamlit as st

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