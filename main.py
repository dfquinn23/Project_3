import streamlit as st
import pandas as pd
from agents.agents import AgentSea
# from tools.evaluation import RecommendationEvaluator
from tools.visualization import SmartVestVisualizer
import plotly.graph_objects as go
from datetime import datetime
import json

class SmartVestWeb:
    def __init__(self):
        self.agent_sea = AgentSea()
        # self.evaluator = RecommendationEvaluator()
        self.visualizer = SmartVestVisualizer()
        
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = None
        if 'analysis_results' not in st.session_state:
            st.session_state.analysis_results = None

    def display_sidebar(self):
        """Create sidebar for user inputs"""
        with st.sidebar:
            st.title("Investment Profile")
            
            risk_tolerance = st.select_slider(
                "Risk Tolerance",
                options=["Low", "Medium", "High"],
                value="Medium"
            )
            
            investment_horizon = st.select_slider(
                "Investment Horizon",
                options=["Short-term", "Medium-term", "Long-term"],
                value="Medium-term"
            )
            
            investment_amount = st.number_input(
                "Investment Amount ($)",
                min_value=1000,
                max_value=10000000,
                value=10000,
                step=1000
            )
            
            has_portfolio = st.checkbox("I have existing investments")
            
            existing_portfolio = {}
            if has_portfolio:
                st.subheader("Current Portfolio")
                col1, col2 = st.columns(2)
                with col1:
                    symbol = st.text_input("Stock Symbol").upper()
                with col2:
                    amount = st.number_input("Amount ($)", min_value=0.0)
                
                if st.button("Add to Portfolio"):
                    if symbol and amount > 0:
                        existing_portfolio[symbol] = amount
            
            if st.button("Generate Analysis"):
                st.session_state.user_profile = {
                    "risk_tolerance": risk_tolerance,
                    "investment_horizon": investment_horizon,
                    "investment_amount": investment_amount,
                    "existing_portfolio": existing_portfolio,
                    "timestamp": datetime.now().isoformat()
                }
                self.run_analysis()

    def run_analysis(self):
        """Run the investment analysis"""
        with st.spinner("Analyzing market conditions..."):
            # Simulate market analysis
            market_analysis = {
                "market_trend": "bullish",
                "sector_performance": {
                    "Technology": 0.8,
                    "Healthcare": 0.5,
                    "Finance": -0.2,
                    "Energy": 0.3
                },
                "historical_data": [
                    {"date": "2024-01", "value": 100},
                    {"date": "2024-02", "value": 105},
                    {"date": "2024-03", "value": 103},
                ]
            }
        
        with st.spinner("Generating recommendations..."):
            # Simulate recommendations
            recommendations = {
                "stocks": ["AAPL", "MSFT", "GOOGL"],
                "allocation": [0.4, 0.3, 0.3]
            }
        
        with st.spinner("Assessing risks..."):
            # Simulate risk assessment
            risk_assessment = {
                "risk_score": 0.7,
                "market_risk": 0.6,
                "volatility": 0.5,
                "sector_risk": 0.4,
                "liquidity_risk": 0.3,
                "risk_factors": ["market volatility", "sector concentration"],
                "risk_match": 0.85
            }
        
        st.session_state.analysis_results = {
            "market_analysis": market_analysis,
            "recommendations": recommendations,
            "risk_assessment": risk_assessment
        }

    def display_results(self):
        """Display analysis results with visualizations"""
        if st.session_state.analysis_results is None:
            return
        
        results = st.session_state.analysis_results
        
        # Market Analysis Section
        st.header("Market Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(
                self.visualizer.create_market_trends_chart(
                    results["market_analysis"]
                ),
                use_container_width=True
            )
        with col2:
            st.plotly_chart(
                self.visualizer.create_sector_performance_chart(
                    results["market_analysis"]
                ),
                use_container_width=True
            )
        
        # Portfolio Recommendations Section
        st.header("Investment Recommendations")
        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(
                self.visualizer.create_portfolio_allocation_chart(
                    results["recommendations"]
                ),
                use_container_width=True
            )
        with col4:
            st.plotly_chart(
                self.visualizer.create_risk_analysis_chart(
                    results["risk_assessment"]
                ),
                use_container_width=True
            )
        
        # Risk Assessment Section
        st.header("Risk Assessment")
        st.plotly_chart(
            self.visualizer.create_risk_tolerance_match(
                st.session_state.user_profile,
                results["risk_assessment"]
            ),
            use_container_width=True
        )
        
        # Download Results
        if st.button("Download Analysis Report"):
            report = {
                "user_profile": st.session_state.user_profile,
                "analysis_results": st.session_state.analysis_results,
                "timestamp": datetime.now().isoformat()
            }
            st.download_button(
                "Download JSON",
                data=json.dumps(report, indent=2),
                file_name=f"smartvest_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

def main():
    st.set_page_config(
        page_title="SmartVest - AI Investment Advisor",
        page_icon="📈",
        layout="wide"
    )
    
    app = SmartVestWeb()
    app.initialize_session_state()
    
    # Title and Description
    st.title("SmartVest - AI Investment Advisor")
    st.markdown("""
        Get personalized investment recommendations based on market analysis 
        and your investment preferences.
    """)
    
    # Display sidebar and main content
    app.display_sidebar()
    app.display_results()

if __name__ == "__main__":
    main()