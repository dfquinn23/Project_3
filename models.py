from pydantic import BaseModel, Field
from typing import List
# from d_tools import SentementAnalysisToolOutput

# tool
# class TimestampOutput(BaseModel):
#     timemstamp: str

class SentementAnalysisToolInput(BaseModel):
    text: str = Field(..., description="The text you want to run a sentiment analysis on.")

class SentementAnalysisToolOutput(BaseModel):
    reasoning: str
    sentiment_score: float
    confidence_score: float

# output
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

class ArticleSummary(BaseModel):
    """
    The ellipsis makes the field required, alternative is to use sometinig like 'title: str', etc.
    The 'description=' is optional for self documenting and can be omitted.
    """
    title: str = Field(..., description="The title of the news article.") 
    content: str = Field(..., description="The full content of the news article.")
    publication_date: str = Field(..., description="The publication date of the article.")


