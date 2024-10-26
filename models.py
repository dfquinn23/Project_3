from pydantic import BaseModel, Field

from tools import SentementAnalysisToolOutput

class CompanyInfo(BaseModel):
    company_name: str
    ticker: str

class FinancialAnalysis(BaseModel):
    company_name: str
    ticker: str
    financial_analysis: list[str]

class SentimentAnalysis(BaseModel):
    company_name: str
    ticker: str
    sentiment_analysis: str
    analysis: list[SentementAnalysisToolOutput]
    average_sentiment_score: float


class TimestampOutput(BaseModel):
    timemstamp: str

class SentementAnalysisToolInput(BaseModel):
    text: str = Field(..., description="The text you want to run a sentiment analysis on.")

class SentementAnalysisToolOutput(BaseModel):
    reasoning: str
    sentiment_score: float
    confidence_score: float
