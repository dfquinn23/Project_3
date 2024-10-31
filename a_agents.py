from crewai import Agent, LLM
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from openai import OpenAI

import os
from dotenv import load_dotenv

from d_tools import GetTimestampTool, SentimentAnalysisTool, FormatJSONReportTool
# from typing import List
# from models import ArticleSummary

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

def get_llm(num) -> LLM:
    try:
        if num == 0:
            # returns GPT 4o Mini
            return OpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini", temperature=0.2)
        if num == 1:
            # returns X AI Grok-2 Mini
            return OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1", model="grok-beta", temperature=0.2)
        if num == 2:
            # returns Groq (LPU not GPPU) Llama3-70b-8192
            return OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1", model="llama3-70b-8192", temperature=0.2)
        else:
            # returns Ollama/llama3.1:8b
            return LLM(model="ollama/llama3.1:8b", base_url="http://localhost:11434", temperature=0.2)
            # return LLM(model="ollama/llama3:latest", base_url="http://localhost:11434")
    except Exception as e:
        print("preparing model")
        # print("Error in get_llm:", e)

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
        print(f"Research agent initialized for company: {self.company}")  # Debugging statement
        self.search_tool = SerperDevTool()
        self.scrape_tool = ScrapeWebsiteTool()
        self.get_timestamp_tool = GetTimestampTool()
        self.get_sentiment_analysis_tool = SentimentAnalysisTool()
        self.format_json_report_tool = FormatJSONReportTool()
        self.llm_num = 1

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
            memory=True,
            llm=get_llm(1)
        )

    def research_agent(self) -> Agent:
        return Agent(
            role="News Article Researcher",
            goal="""
                 1. Receive the stock ticker symbol from the Ticker Agent.
                 2. Search for recent news articles about the ticker symbol using 
                     financial news websites and social media platforms, focusing 
                     on identifying headlines or summaries that have been published 
                     within the last 72 hours. Target sources include reputable 
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
            memory=True,
            llm=get_llm(2)
        )

    def analyst_agent(self) -> Agent:
        return Agent(
            role="Analyst",
            backstory="""
                1. You are a financial analyst specializing in creating structured financial reports.
                2. Your expertise lies in analyzing financial news and creating clear, JSON-formatted reports.
                3. You always use the Format JSON Report Tool to ensure consistent output structure.
                4. You excel at synthesizing multiple inputs into a single comprehensive analysis.
                """,
            goal=f"""
                1. Analyze all inputs from previous agents about {self.company} and synthesize into ONE final report.
                2. Create a single comprehensive financial report that includes:
                   - Company name and ticker
                   - Consolidated summary of all news articles
                   - Overall financial analysis incorporating all data points
                3. Use the Format JSON Report Tool to structure your final output.
                4. Ensure the report is cohesive and avoids redundant information.
                """,
            verbose=True,
            max_retry_limit=1,
            memory=False,
            llm=get_llm(1)
        )

    def sentiment_agent(self) -> Agent:
        return Agent(
            role="Senior Financial Sentiment Analyst",
            backstory="""
                 1. You are a Senior Financial Sentiment Analyst.
                 2. You specialize in conducting an informative financial sentiment analysis from the news articles and blog posts received by the News Article Researcher agent.
                 Important:\n
                 - Once you have done the sentiment analysis, you are done.\n
                 - The returned sentiment analysis should be a list containing:
                    1. the reason for the score
                    2. the sentiment score
                    3. the confidence score
                 """,
            goal="""
                 1. Take the financial news articles and blog posts summaries from the News Article Researcher agent.
                 2. Run a financial sentiment analysis on the articles and blog posts provided by the News Article Researcher agent using only the tools you have.
                 IMPORTANT:
                 - Only use the tool provided below to complete your task.
                 - Only conduct a sentiment analysis on the financial news articles and blog posts summaries for {self.company} provided by the News Article Researcher agent using the tools you have.
                 - Make sure your output includes the correct information from the pervious agents.
                 - The company and ticker should not be made up but should be obtained from previous agents.
                 """,
            max_iter=2,
            max_retry_limit=1,
            llm=get_llm(1),
            tools=[self.get_sentiment_analysis_tool],
            memory=True,
            verbose=True
        )

