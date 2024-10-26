from pydantic import BaseModel

from tools import SentementAnalysisToolOutput

class CompanyInfo(BaseModel):
    company_name: str
    ticker: str

class FinancialAnalysis(BaseModel):
    company_name: str
    ticker: str
    financial_summary: str

class SentimentAnalysis(BaseModel):
    company_name: str
    ticker: str
    financial_summary: str
    sentiment_analysis: str
    analysis: list[SentementAnalysisToolOutput]
    average_sentiment_score: float