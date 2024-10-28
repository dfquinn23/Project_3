from crewai import Agent, LLM
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from langchain_openai import OpenAI

import os
from dotenv import load_dotenv

from d_tools import GetTimestampTool, SentimentAnalysisTool
from typing import List
from models import ArticleSummary

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

def get_llm(num) -> LLM:
    if num == 0:
        return OpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini", temperature=0.3)
    else:
        return LLM(model="ollama/llama3:latest", temperature=0.3)

"""
Purpose:
    1. Our agents will be tasked with performing sentiment analysis of user-inputted stocks over a specific date range.
    2. Agent 1 is the Ticker Agent responsible for taking a company name and returning the ticker.
    3. Agent 2 is our Researcher. He will take the ticker from the Ticker Agent and conduct a search for recent articles, blog posts, and social media mentions headlines.
    4. Agent 3 is the Analyst, who is tasked with creating the sentiment analysis report.
    5. Agent 4 is the Sentiment Analyst.
"""

class ResearchAgents:
    def __init__(self, company):
        self.company = company
        self.search_tool = SerperDevTool()
        self.scrape_tool = ScrapeWebsiteTool()
        self.get_timestamp_tool = GetTimestampTool()
        self.get_sentiment_analysis_tool = SentimentAnalysisTool()

        # if this is set to 0, then the LLM used will be OPENAI, else it will be a locally running Ollama
        self.llm_num = 0

    def ticker_agent(self) -> Agent:
        return Agent(
            role="Ticker Agent",
            goal="Return a company's stock ticker accurately.",
            backstory="""
                1. You work on the front lines of customer service.
                2. Our customers come to you when they want to obtain our company's sentiment analysis for stocks over a specific date range.
                3. You pride yourself on being fast, courteous, and accurate.
                """,
            verbose=True,
            tools=[self.search_tool],
            allow_delegation=True,
            memory=True,
            llm=get_llm(self.llm_num)
        )

    def research_agent(self) -> Agent:
        return Agent(
            role="News Article Researcher",
            goal="""
                1. Receive the stock ticker symbol from the Ticker Agent.
                2. Search for recent news articles about the ticker symbol using 
                    financial news websites and social media platforms, focusing 
                    on identifying headlines or summaries that have been published 
                    within the last 24 hours. Target sources include reputable 
                    news organizations, such as Bloomberg, CNBC, or Reuters.
                3. Refine search results by excluding articles from sources 
                    known for biased reporting or lack of objectivity.
                4. Expected delivery to Sentiment Analyst Agent: A list of up 
                    to 10 relevant news article summaries.
                """,
            backstory="""
                1. You are trained on a vast dataset of news articles from 
                    reputable sources, including financial news websites and 
                    social media platforms.
                2. Your expertise lies in searching and analyzing market data 
                    to identify relevant news articles using techniques to 
                    evaluate the credibility of news articles.
                3. You prioritize accuracy and reliability in your research.
                """,
            verbose=True,
            tools=[self.search_tool, self.scrape_tool],
            allow_delegation=True,
            memory=True,
            llm=get_llm(self.llm_num)
        )

    def analyst_agent(self) -> Agent:
        return Agent(
            role="Analyst",
            backstory="""
                1. You are a highly experienced writer with specialization in creating investment research reports.
                2. Your writing style is conversational and engaging, yet professional.
                3. For sentiment analysis reports like the ones you are creating here, you leverage your analytical and interpretative skills to offer insightful recommendations.
                """,
            goal="""
                1. Receive the research from the Research Agent and write your sentiment analysis report.
                2. These reports should be engaging, easily understood, and relatively jargon-free.
                3. These reports should provide an analysis of the research, provide a sentiment score of -1 (negative), 0 (neutral), or 1 (positive).
                    You must be able to explain why you scored the stock as you did, with citations if possible.
                """,
            verbose=True,
            llm=get_llm(self.llm_num)
        )

    def sentiment_agent(self) -> Agent:
        return Agent(
            role="Senior Financial Sentiment Analyst",
            backstory="""
                1. You are a Senior Financial Sentiment Analyst.
                2. You specialize in conducting an informative financial sentiment analysis from the news articles and blog posts received by the previous agent.
                """,
            goal="""
                1. Take the financial news articles and blog posts from the previous agent.
                2. Run a financial sentiment analysis on the articles and blog posts provided by the previous agent.
                3. Get the current timestamp.
                IMPORTANT:
                - Only use the tools provided below to complete your task.
                - Only conduct a sentiment analysis on the financial news articles and blog posts for {self.company} provided by the previous agent.
                - Don't forget to save the document using a current timestamp!
                """,
            max_iter=5,
            max_retry_limit=1,
            llm=get_llm(self.llm_num),
            tools=[self.get_timestamp_tool, self.get_sentiment_analysis_tool],
            memory=True,
            verbose=True
        )

    def get_analysis_task(self, analyst_agent, dependencies):
        article_summaries = fetch_article_summaries()  # Replace with actual data fetching logic

        # Ensure article_summaries is a list of ArticleSummary objects
        if isinstance(article_summaries, str):
            # Convert string to list of ArticleSummary objects
            article_summaries = parse_article_summaries(article_summaries)  # Implement this function

        # Use a dictionary to represent the task
        task = {
            "output_pydantic": article_summaries
        }

        return task

    def get_tool_input(self) -> dict:
        """
        Creates a tool input dictionary for the stock ticker search
        Returns:
            dict: Tool input configuration
        """
        return {
            "search_query": f"{self.company} stock ticker"
        }
