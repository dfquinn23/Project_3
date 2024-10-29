from crewai import Agent, Task
from models import CompanyInfo, FinancialAnalysis, SentimentAnalysis, ArticleSummary, FinancialMetrics
from models import CompanyInfo, NewsArticles, FinancialAnalysis, SentimentAnalysis
from pydantic import BaseModel
from typing import List
from datetime import datetime

class AgentTasks:
    def __init__(self, company_name) -> None:
        self.company_name = company_name
        self.timestamp = None
    
    def get_stock_ticker_task(self, agent: Agent):
        return Task(
            name="Get Stock Ticker",
            description=f"""
                1. This task will enable the ticker_agent to take the company name '{self.company_name}'
                2. Then the ticker_agent will utilize the search_tool to go online and identify the stock ticker associated with {self.company_name}
                3. The ticker_agent will then return the stock ticker and pass it to the research_agent to research sentiment surrounding the stock
            """,
            agent=agent,
            expected_output=f"A json object containing {self.company_name} and the ticker symbol",
            output_pydantic=CompanyInfo
        )

    def get_news_task(self, agent: Agent, tasks: list[Task]):
        return Task(
            name="Get News",
            description=(
                f"This task will gather the latest news articles related to the company {self.company_name}."
            ),
            agent=agent,
            expected_output=(
                f"A json object containing the summaries for 5 news articles related to the company {self.company_name}."
            ),
            context=tasks,
            output_pydantic=NewsArticles
        )
    
    def get_analysis_task(self, agent: Agent, tasks: list[Task]):
        return Task(
            name="Analyze News",
            description=(
                "1. Use the stock ticker symbol to search for recent (within the last 24 hours) news articles across major financial news sources, focusing on headlines or summaries. "
                "2. Prioritize sources known for reliability, such as Bloomberg, CNBC, and Reuters, and avoid those with biased or low-quality reporting. "
                "3. Provide a summary list of up to 10 relevant news articles, formatted for easy processing by the Sentiment Analyst Agent. "
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
            output_pydantic=FinancialAnalysis  # Use the class directly
        )
    
    def get_financial_metrics_task(self, agent: Agent, tasks: list[Task]):
        return Task(
            name="Get Financial Metrics",
            description="Get the financial metrics for the company",
            agent=agent,
            expected_output="The financial metrics for the company",
            output_pydantic=FinancialMetrics
        )
    
    def get_sentiment_task(self, agent: Agent, tasks: list[Task]):
        # Generate a timestamp
        timestamp = datetime.now().timestamp()
        
        return Task(
            name="Get Sentiment",
            description=(
                "Conduct a financial sentiment analysis for all of the articles and blog posts that the News Article Researcher agent provided from the Get News task."
                "NewsSummaries.summaries will contain the list of articles from the Get News task."
                "Remember to also get a timestamp for when you save the file and save it to the tasks timestamp variable under this task."
                "Don't forget to use the obtained timestamp in the saved file name."
            ),
            agent=agent,
            expected_output=(
                f"A JSON object containing the {self.company_name}, ticker, and a summary of the research that you have done."
                "IMPORTANT:\n"
                "OUTPUT SHOULD LOOK LIKE:\n"
                "{\n"
                f"'company_name': {self.company_name}',\n"
                f"'ticker': [the found ticker for {self.company_name}]',\n"
                f"summaries: list[str],\n"
                "'financial_report': 'your overall financial sentiment analysis summary goes here.',\n"
                "'analysis': list[SentimentAnalysisToolOutput]\n"
                "'average_sentiment_score': [float of an average sentimentscore]',\n"
                "}\n"
            ),

            output_file=f"output/financial_analysis_{round(timestamp)}.md",
            context=tasks,
            output_pydantic=SentimentAnalysis  # Ensure this is a valid subclass of BaseModel
        )



# Remove or rename this custom Task class as it conflicts with crewai.Task
# class Task(BaseModel):
#     description: str
#     expected_output: str
#     output_pydantic: type
