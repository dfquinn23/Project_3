from pydantic import BaseModel, Field
from typing import List
# from d_tools import SentementAnalysisToolOutput

# tool
# class TimestampOutput(BaseModel):
#     timemstamp: str


class SentimentAnalysisToolInput(BaseModel):
    title: str = Field(description="The title of the article or blog post.")
    summary: str = Field(..., description="The text to be analyzed for sentiment.")
    # Add other fields as necessary

class SentimentAnalysisToolOutput(BaseModel):
    reasoning: str
    sentiment_score: float
    confidence_score: float

# output
class CompanyInfo(BaseModel):
    company_name: str
    ticker: str

class NewsArticles(BaseModel):
    company_name: str
    ticker: str
    summaries: list[str]= Field(..., description="the list of news articles and blog post summaries.")

class FinancialAnalysis(BaseModel):
    company_name: str
    ticker: str
    summaries: list[str]= Field(..., description="the list of news articles and blog post summaries.")
    financial_report: str

class SentimentAnalysis(BaseModel):
    company_name: str
    ticker: str
    summaries: list[str]= Field(..., description="the list of news articles and blog post summaries.")
    financial_report: str
    analysis: list[SentimentAnalysisToolOutput]
    average_sentiment_score: float

class ArticleSummary(BaseModel):
    """
    The ellipsis makes the field required, alternative is to use sometinig like 'title: str', etc.
    The 'description=' is optional for self documenting and can be omitted.
    """
    title: str = Field(..., description="The title of the news article.") 
    content: str = Field(..., description="The full content of the news article.")
    publication_date: str = Field(..., description="The publication date of the article.")

class FinancialMetrics(BaseModel):
    company_name: str
    ticker: str
    financial_metrics: str


