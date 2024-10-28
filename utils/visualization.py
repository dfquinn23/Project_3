import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
import pandas as pd
import numpy as np
import streamlit as st

class SmartVestVisualizer:
    def create_portfolio_allocation_chart(self, recommendations: Dict) -> go.Figure:
        """Create a pie chart showing portfolio allocation"""
        fig = go.Figure(data=[go.Pie(
            labels=recommendations["stocks"],
            values=recommendations["allocation"],
            hole=.3
        )])
        
        fig.update_layout(
            title="Recommended Portfolio Allocation",
            showlegend=True
        )
        return fig
    
    def create_risk_analysis_chart(self, risk_assessment: Dict) -> go.Figure:
        """Create a radar chart showing risk metrics"""
        categories = ['Market Risk', 'Volatility', 'Sector Risk', 'Liquidity Risk']
        values = [
            risk_assessment.get('market_risk', 0),
            risk_assessment.get('volatility', 0),
            risk_assessment.get('sector_risk', 0),
            risk_assessment.get('liquidity_risk', 0)
        ]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself'
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=False,
            title="Risk Analysis Breakdown"
        )
        return fig
    
    def create_market_trends_chart(self, market_analysis: Dict) -> go.Figure:
        """Create a line chart showing market trends"""
        # Assuming market_analysis contains historical data
        df = pd.DataFrame(market_analysis.get('historical_data', []))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['value'],
            mode='lines+markers',
            name='Market Trend'
        ))
        
        fig.update_layout(
            title="Market Performance Trend",
            xaxis_title="Date",
            yaxis_title="Value"
        )
        return fig
    
    def create_sector_performance_chart(self, market_analysis: Dict) -> go.Figure:
        """Create a bar chart showing sector performance"""
        sectors = market_analysis.get('sector_performance', {})
        
        fig = go.Figure([go.Bar(
            x=list(sectors.keys()),
            y=list(sectors.values()),
            marker_color=['green' if x > 0 else 'red' for x in sectors.values()]
        )])
        
        fig.update_layout(
            title="Sector Performance",
            xaxis_title="Sector",
            yaxis_title="Performance (%)"
        )
        return fig

    def create_risk_tolerance_match(self, user_profile: Dict, risk_assessment: Dict) -> go.Figure:
        """Create a gauge chart showing risk tolerance match"""
        risk_match = risk_assessment.get('risk_match', 0.75)  # Example value
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_match * 100,
            title={'text': "Risk Profile Match"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 75], 'color': "gray"},
                    {'range': [75, 100], 'color': "darkgray"}
                ]
            }
        ))
        return fig

    def display_analysis(self, results):
        st.subheader("Stock Performance")
        st.write(f"Start Price: {results['stock_performance']['start_price']}")
        st.write(f"End Price: {results['stock_performance']['end_price']}")
        st.write(f"Percent Change: {results['stock_performance']['percent_change']}%")

        st.subheader("Sentiment Analysis")
        st.write(f"Average Sentiment: {results['sentiment_analysis']['average_sentiment']}")
        st.write(f"Number of Headlines: {results['sentiment_analysis']['num_headlines']}")

        st.subheader("Financial Metrics")
        st.write(f"Daily High: {results['financial_metrics']['daily_high']}")
        st.write(f"Daily Low: {results['financial_metrics']['daily_low']}")
        st.write(f"Volume: {results['financial_metrics']['volume']}")
        st.write(f"Market Cap: {results['financial_metrics']['market_cap']}")

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
