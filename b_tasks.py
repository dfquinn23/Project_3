from crewai import Agent, Task
from models import CompanyInfo, FinancialAnalysis, SentimentAnalysis, ArticleSummary
from pydantic import BaseModel
from typing import List
from datetime import datetime

class AgentTasks:
    def __init__(self, company_name) -> None:
        self.company_name = company_name
    
    def get_stock_ticker_task(self, agent: Agent):
        return Task(
            name="Get Stock Ticker",
            description="""
                1. This task will enable the ticker_agent to take a company name provided by a user input
                2. Then the ticker_agent will utilize the search_tool to go online and identify the stock ticker associated with that company
                3. The ticker_agent will then return the stock ticker and pass it to the research_agent to research sentiment surrounding the stock
            """,
            agent=agent,
            expected_output=(
                "The ticker_agent will return the stock {ticker} symbol for the requested company"
                "to pass to the research_agent"
            ),
            output_pydantic=CompanyInfo
        )

    def get_news_task(self, agent: Agent, tasks: list[Task]):
        return Task(
            name="Get News",
            description=(
                "This task will gather the latest news articles related to the company {self.company_name}."
            ),
            agent=agent,
            expected_output=(
                "A list of news articles related to the company {self.company_name}."
            ),
            context=tasks,
            output_pydantic=FinancialAnalysis
        )
    
    def get_analysis_task(self, agent: Agent, tasks: list[Task]):
        return Task(
            name="Analyze News",
            description=(
                "1) Use the stock ticker symbol to search for recent (within the last 24 hours) news articles across major financial news sources, focusing on headlines or summaries. "
                "2) Prioritize sources known for reliability, such as Bloomberg, CNBC, and Reuters, and avoid those with biased or low-quality reporting. "
                "3) Provide a summary list of up to 10 relevant news articles, formatted for easy processing by the Sentiment Analyst Agent. "
                "The information gathered should maintain a high standard of objectivity and credibility."
            ),
            agent=agent,
            expected_output=(
                "A list of up to 10 recent news articles (title and brief summary) relevant to the specified stock ticker symbol. "
                "Each entry should include: "
                "- Title of the article "
                "- Complete text of each article, capturing all details for analysis "
                "- Publication date "
                "Ensure the list excludes duplicate or irrelevant sources."
            ),
            context=tasks,
            output_pydantic=ArticleSummary  # Use the class directly
        )
    
    def get_sentiment_task(self, agent: Agent, tasks: list[Task]):
        # Generate a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        return Task(
            name="Get Sentiment",
            description=(
                "Conduct a financial sentiment analysis for all of the articles and blog posts that the previous agent provided."
                "Remember to also get a timestamp for when you save the file."
                "Don't forget to use the obtained timestamp in the saved file name."
            ),
            agent=agent,
            expected_output=(
                "A JSON object containing the {self.company_name}, ticker, and a summary of the research that you have done."
                "IMPORTANT:\n"
                "OUTPUT SHOULD LOOK LIKE:\n"
                "{\n"
                "'company_name': {self.company_name}',\n"
                "'ticker': [the found ticker for {self.company_name}]',\n"
                "'sentiment_analysis': 'your overall financial sentiment analysis summary goes here.'',\n"
                "'analysis': list[SentimentAnalysisToolOutput]\n"
                "'average_sentiment_score': [float of an average sentimentscore]',\n"
                "}\n"
            ),
            output_file=f"output/financial_analysis_{timestamp}.md",
            context=tasks,
            output_pydantic=SentimentAnalysis  # Ensure this is a valid subclass of BaseModel
        )

# Remove or rename this custom Task class as it conflicts with crewai.Task
# class Task(BaseModel):
#     description: str
#     expected_output: str
#     output_pydantic: type
