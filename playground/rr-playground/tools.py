import yfinance as yf
import pandas as pd
import requests
from typing import List, Dict
import os
from datetime import datetime, timedelta
import json
import logging

logging.basicConfig(level=logging.INFO)

class StockAnalyzer:
    def __init__(self, symbol: str, days: int = 1):
        self.symbol = symbol
        self.days = days
        self.end_date = datetime.now()
        self.start_date = self.end_date - timedelta(days=self.days)

    def get_stock_data(self) -> pd.DataFrame:
        stock = yf.Ticker(self.symbol)
        df = stock.history(start=self.start_date.strftime('%Y-%m-%d'), end=self.end_date.strftime('%Y-%m-%d'))
        return df

    def get_news_headlines(self, input_dict=None) -> List[Dict]:
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={self.symbol}&apikey={api_key}'
        
        logging.info(f"Fetching news headlines for {self.symbol}")
        try:
            r = requests.get(url, timeout=10)  # Add a timeout
            r.raise_for_status()  # Raise an exception for bad status codes
            data = r.json()
            
            if 'feed' in data:
                logging.info(f"Successfully fetched {len(data['feed'])} headlines")
                return data['feed']
            elif 'Note' in data:
                logging.warning(f"API limit reached: {data['Note']}")
                return []
            else:
                logging.error(f"Unexpected response structure: {data.keys()}")
                return []
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching news headlines: {str(e)}")
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
