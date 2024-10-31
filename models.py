from pydantic import BaseModel, Field
from typing import List

class SentimentAnalysisToolInput(BaseModel):
    title: str = Field(description="The title of the article or blog post.")
    summary: str = Field(..., description="The text to be analyzed for sentiment.")

class SentimentAnalysisToolOutput(BaseModel):
    reasoning: str
    sentiment_score: float
    confidence_score: float

class CompanyInfo(BaseModel):
    company_name: str
    ticker: str

class NewsArticles(BaseModel):
    company_name: str
    ticker: str
    summaries: List[str] = Field(..., description="The list of news articles and blog post summaries.")

class FinancialAnalysis(BaseModel):
    company_name: str
    ticker: str
    summaries: List[str] = Field(..., description="The list of news articles and blog post summaries.")
    financial_report: str

class SentimentAnalysis(BaseModel):
    company_name: str
    ticker: str
    summaries: List[str] = Field(..., description="The list of news articles and blog post summaries.")
    financial_report: str
    analysis: List[SentimentAnalysisToolOutput]
    average_sentiment_score: float

class ArticleSummary(BaseModel):
    title: str = Field(..., description="The title of the news article.") 
    content: str = Field(..., description="The full content of the news article.")
    publication_date: str = Field(..., description="The publication date of the article.")


