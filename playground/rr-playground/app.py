import streamlit as st
import json
from crewai import Crew
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os
import yfinance as yf
import plotly.graph_objects as go
from agents import StockAnalysisAgents
from tools import StockAnalyzer
import time
import random

# Load environment variables
load_dotenv()

# Check if the API key is set
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Initialize OpenAI LLM
llm = OpenAI(api_key=api_key, model="gpt-4o-mini", temperature=0.3)

def run_analysis(symbol, days, progress_callback):
    try:
        # Create StockAnalysisAgents instance
        stock_analysis_agents = StockAnalysisAgents(llm, symbol)

        # Create agents
        agents = stock_analysis_agents.create_agents()
        progress_callback(20, "Agents created")

        # Create tasks
        tasks = stock_analysis_agents.create_tasks(agents, days)
        progress_callback(40, "Tasks created")

        # Create the crew
        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True
        )
        progress_callback(60, "Crew assembled")

        # Run the crew
        result = crew.kickoff()
        progress_callback(80, "Analysis completed")

        # Generate JSON output
        stock_analyzer = StockAnalyzer(symbol, days)
        stock_analyzer.generate_json_output()
        progress_callback(100, "JSON output generated")

        return result
    except Exception as e:
        st.error(f"An error occurred during analysis: {str(e)}")
        return None

def load_analysis_results(symbol):
    with open(f'{symbol}_analysis.json', 'r') as f:
        return json.load(f)

def get_company_info(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    return {
        'name': info.get('longName', 'N/A'),
        'logo_url': info.get('logo_url', None),
        'sector': info.get('sector', 'N/A'),
        'industry': info.get('industry', 'N/A')
    }

def create_gauge_chart(sentiment_score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = sentiment_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Sentiment Score"},
        gauge = {
            'axis': {'range': [-1, 1]},
            'bar': {'color': "darkblue"},
            'steps' : [
                {'range': [-1, -0.5], 'color': "red"},
                {'range': [-0.5, 0.5], 'color': "yellow"},
                {'range': [0.5, 1], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': sentiment_score
            }
        }
    ))
    return fig

# Add this new function for fun facts
def get_stock_fun_fact():
    fun_facts = [
        "The New York Stock Exchange was founded in 1792 under a buttonwood tree.",
        "The term 'bull market' comes from the way a bull attacks, thrusting its horns up into the air.",
        "The first stock ticker was invented in 1867 by Edward Calahan.",
        "The longest bull market in history lasted from 2009 to 2020, lasting almost 11 years.",
        "The phrase 'Blue Chip stocks' comes from blue poker chips, which have the highest value in the game.",
        "The stock market crash of 1987 is known as 'Black Monday'.",
        "The dot-com bubble of the late 1990s saw the NASDAQ rise 400% in five years.",
        "Warren Buffett bought his first stock at age 11 and regretted selling it too soon.",
        "The term 'Wall Street' comes from an actual wall built in the 17th century to protect Dutch colonists.",
        "The first modern mutual fund was created in 1924."
    ]
    return random.choice(fun_facts)

st.set_page_config(page_title="Stock Sentiment Analysis", layout="wide")

st.title("Stock Sentiment Analysis")

col1, col2 = st.columns([1, 2])

with col1:
    symbol = st.text_input("Enter stock symbol (e.g., AAPL):", value="AAPL")
    days = st.number_input("Number of days for analysis:", min_value=1, max_value=30, value=1)
    
    if st.button("Run Analysis"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        fun_fact = st.empty()
        result_placeholder = st.empty()
        
        def update_progress(progress, status):
            progress_bar.progress(progress)
            status_text.text(status)
            if random.random() < 0.3:  # 30% chance to show a fun fact
                fun_fact.info(f"Fun Fact: {get_stock_fun_fact()}")
        
        result = run_analysis(symbol, days, update_progress)
        
        if result:
            result_placeholder.write("Crew result:", result)
        else:
            st.warning("Analysis failed. Please try again.")

with col2:
    try:
        results = load_analysis_results(symbol)
        company_info = get_company_info(symbol)

        st.subheader(f"{company_info['name']} ({symbol})")
        if company_info['logo_url']:
            st.image(company_info['logo_url'], width=100)
        st.write(f"Sector: {company_info['sector']}")
        st.write(f"Industry: {company_info['industry']}")

        sentiment_score = results['sentiment_analysis']['average_sentiment']
        fig = create_gauge_chart(sentiment_score)
        st.plotly_chart(fig)

        st.subheader("Financial Metrics")
        metrics = results['financial_metrics']
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Daily High", f"${metrics['daily_high']:.2f}")
        col2.metric("Daily Low", f"${metrics['daily_low']:.2f}")
        col3.metric("Volume", f"{metrics['volume']:,}")
        col4.metric("Market Cap", f"${metrics['market_cap']:,}")

        st.subheader("Recent Headlines")
        for headline in results['headlines']:
            st.write(f"- {headline['title']}")

        st.subheader("Stock Performance")
        performance = results['stock_performance']
        st.write(f"Start Price: ${performance['start_price']:.2f}")
        st.write(f"End Price: ${performance['end_price']:.2f}")
        st.write(f"Percent Change: {performance['percent_change']:.2f}%")

    except FileNotFoundError:
        st.warning("No analysis results found. Please run the analysis first.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
