import yfinance as yf
import pandas as pd
import requests
from typing import List, Dict, Type
import os
from datetime import datetime, timedelta
import json

from langchain_ollama.llms import OllamaLLM
from crewai_tools import BaseTool
from pydantic import BaseModel, Field

from models import SentimentAnalysisToolInput, SentimentAnalysisToolOutput
# Ensure these classes are defined in models.py


class StockAnalyzer:
    def __init__(self, symbol: str, days: int = 30):
        self.symbol = symbol
        self.days = days
        self.end_date = datetime.now()
        self.start_date = self.end_date - timedelta(days=self.days)

    def get_stock_data(self) -> pd.DataFrame:
        stock = yf.Ticker(self.symbol)
        df = stock.history(start=self.start_date.strftime('%Y-%m-%d'), end=self.end_date.strftime('%Y-%m-%d'))
        return df

    def get_news_headlines(self, input_dict=None) -> List[Dict]:
        stock = yf.Ticker(self.symbol)
        news = stock.news
        
        if news:
            return news
        return []

    def analyze_headlines_sentiment(self, headlines: List[Dict]) -> Dict:
        sentiment_scores = [headline.get('overall_sentiment_score', 0) for headline in headlines]
        return {
            'average_sentiment': sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0,
            'num_headlines': len(headlines)
        }

    def analyze_stock_performance(self, input_dict=None) -> Dict:
        stock_data = self.get_stock_data()
        return {
            'start_price': stock_data['Close'].iloc[0],
            'end_price': stock_data['Close'].iloc[-1],
            'percent_change': ((stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]) / stock_data['Close'].iloc[0]) * 100
        }

    def get_financial_metrics(self, input_dict=None) -> Dict:
        stock = yf.Ticker(self.symbol)
        info = stock.info
        return {
            'daily_high': info.get('dayHigh'),
            'daily_low': info.get('dayLow'),
            'volume': info.get('volume'),
            'market_cap': info.get('marketCap')
        }

    def analyze_sentiment(self) -> Dict:
        stock_data = self.get_stock_data()
        headlines = self.get_news_headlines()
        
        sentiment_analysis = self.analyze_headlines_sentiment(headlines)
        stock_performance = self.analyze_stock_performance()
        financial_metrics = self.get_financial_metrics()
        
        return {
            'symbol': self.symbol,
            'analysis_period': f"{self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')}",
            'stock_performance': stock_performance,
            'sentiment_analysis': sentiment_analysis,
            'financial_metrics': financial_metrics,
            'headlines': headlines[:5]  # Include only the first 5 headlines for brevity
        }

    def generate_json_output(self) -> None:
        analysis_result = self.analyze_sentiment()
        
        with open(f'{self.symbol}_analysis.json', 'w') as f:
            json.dump(analysis_result, f, indent=2)
        
        print(f"Analysis for {self.symbol} has been saved to {self.symbol}_analysis.json")


# 3B model
sa_llm = OllamaLLM(model="mattarad/llama3.2-3b-instruct-mqc-sa", temperature=0.25)


class GetTimestampTool(BaseTool):
    name: str = "Get Timestamp Tool"
    description: str = "This tool is used to obtain a timestamp"

    def _run(self) -> str:
        return str(datetime.now().timestamp())

class SentimentAnalysisTool(BaseTool):
    name: str = "Sentiment Analysis Tool"
    description: str = "This tool analyzes the sentiment of a given text and returns a SentimentAnalysisToolOutput."
    args_schema: Type[BaseModel] = SentimentAnalysisToolInput

    def _run(self, input_data: SentimentAnalysisToolInput) -> SentimentAnalysisToolOutput:
        return sa_llm.invoke(input_data.text)

