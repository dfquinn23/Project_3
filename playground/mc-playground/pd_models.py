from pydantic import BaseModel

class CompanyInfo(BaseModel):
    company_name: str
    ticker: str

class FinancialAnalysis(BaseModel):
    company_name: str
    ticker: str
    financial_analysis: str

class SentimentAnalysis(BaseModel):
    name: str
    article: str
    sentiment_analysis: str