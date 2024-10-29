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

from models import SentimentAnalysisToolInput, NewsArticles, SentimentAnalysisToolOutput


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
        
        if stock_data.empty:
            return {
                'start_price': None,
                'end_price': None,
                'percent_change': None,
                'error': 'No stock data available for the given period.'
            }
        
        return {
            'start_price': stock_data['Close'].iloc[0],
            'end_price': stock_data['Close'].iloc[-1],
            'percent_change': ((stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]) / stock_data['Close'].iloc[0]) * 100
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
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f'output/financial_analysis_{self.symbol}_{timestamp}.json'
        
        with open(file_path, 'w') as f:
            json.dump(analysis_result, f, indent=2)
        
        print(f"Analysis for {self.symbol} has been saved to {file_path}")


# 3B model
try:
    sa_llm = OllamaLLM(
        model="mattarad/llama3.2-3b-instruct-mqc-sa",  # Updated to 3b model
        temperature=0.25,
        base_url="http://localhost:11434"  # Add explicit base URL
    )
except Exception as e:
    print(f"Error initializing Ollama: {e}")
    # Fallback to a different model or raise error
    raise


class GetTimestampTool(BaseTool):
    name: str = "Get Timestamp Tool"
    description: str = "This tool is used to obtain a timestamp"

    def _run(self) -> int:
        return round(datetime.now().timestamp())

class SentimentAnalysisTool(BaseTool):
    name: str = "Sentiment Analysis Tool"
    description: str = "This tool iterantes through a list of text, analyzes the sentiment of the text and returns a list of SentimentAnalysisToolOutput."
    args_schema: Type[BaseModel] = NewsArticles

    def _run(self, articles: NewsArticles) -> List[SentimentAnalysisToolOutput]:
        analysis = []
        for article in articles:
            sentiment = sa_llm.invoke(article.articles)

            sentiment_output = SentimentAnalysisToolOutput(
                reasoning=sentiment.get("reasoning"),
                sentiment_score=sentiment.get("sentiment_score"),
                confidence_score=sentiment.get("confidence_score")
            )
            analysis.append(sentiment_output)
        return analysis

class FormatJSONReportTool(BaseTool):
    name: str = "Format JSON Report Tool"
    description: str = "This tool formats financial analysis data into a structured JSON report"

    def _run(self, input_data: dict) -> str:
        """Format the input data into a structured JSON report"""
        try:
            report = {
                "Company Analysis Report": {
                    "Company Information": {
                        "Name": input_data.get("company_name"),
                        "Ticker Symbol": input_data.get("ticker"),
                        "Report Generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    },
                    "News Summaries": [
                        f"• {summary}" for summary in input_data.get("summaries", [])
                    ],
                    "Financial Analysis": {
                        "Report": input_data.get("financial_report"),
                        "Sentiment Analysis": {
                            "Individual Article Analysis": [
                                {
                                    "Analysis": analysis.get("reasoning"),
                                    "Sentiment Score": f"{analysis.get('sentiment_score', 0):.2f}",
                                    "Confidence": f"{analysis.get('confidence_score', 0):.2f}"
                                }
                                for analysis in input_data.get("analysis", [])
                            ],
                            "Overall Sentiment Score": f"{input_data.get('average_sentiment_score', 0):.2f}"
                        }
                    }
                }
            }
            
            return json.dumps(report, indent=4)
        except Exception as e:
            print(f"Error formatting JSON report: {str(e)}")
            return "{}"

class FinancialMetricsTool(BaseTool):
    name: str = "Financial Metrics Tool"
    description: str = "This tool retrieves financial metrics for a given company."

    def _run(self, company_name: str) -> dict:
        # Logic to retrieve financial metrics
        metrics = {
            "revenue": 1000000,
            "net_income": 200000,
            "assets": 5000000,
            "liabilities": 3000000
        }
        return metrics

