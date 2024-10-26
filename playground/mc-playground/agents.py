from crewai import Agent, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from tools import SentimentAnalysisTool, GetTimestampTool
from langchain_openai import OpenAI

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")


def get_llm(num: int) -> LLM:
    if num == 0:
        return LLM(model="ollama/llama3:latest", temperature=0.3)
    if num == 1:
        return LLM(
            provider="anthropic",
            model="claude-3.5",
            api_key=CLAUDE_API_KEY,
        )
    if num ==2:
        return LLM(
            model="grok-beta",
            base_url="https://api.x.ai/v1",
            api_key=XAI_API_KEY,
        )
    else:
        return OpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo", temperature=0.3)

class AgentSea:
    def __init__(self, company_name: str):
        self.company_name = company_name
        self.serper_tool = SerperDevTool()
        self.scrape_website_tool = ScrapeWebsiteTool()
        self.yahoo_finance_tool = YahooFinanceNewsTool()
        self.sentiment_analysis_tool = SentimentAnalysisTool()
        self.get_timestamp_tool = GetTimestampTool()
    
    def create_ticker_finder_agent(self) -> Agent:
        return Agent(
            role="Senior Online Researcher",
            goal=
                """
                Conduct an amazing online search to find the stock ticker for {self.company_name}.
                IMPORTANT:
                - If you cannot find the result, return "Ticker not found".
                - Do not include any unnecessary words or phrases in your response and only provide the ticker symbol if found.
                - MAKE SURE TO PASS THE TICKER SYMBOL TO THE NEXT AGENT. THIS IS A MUST.
                """,
            backstory=
                """
                You are a Senior Online Researcher that specializes in finding a company's stock market ticker symbol with only the company name.
                """,
            agent_prompt = 
                """
                You are an AI Senior Online Researcher agent tasked with searching the web to find the
                 stock market ticker symbol for the {self.company_name}.
                
                Follow these steps:

                1. Think about what you need to do to complete the task.
                2. Choose an action from the available tools.
                3. Provide the action input as a dictionary.
                4. Observe the result of the action.
                5. Repeat steps 1-4 until you have enough information to provide a final answer.
                6. When ready to give a final answer, use the format:

                Thought: I now can give a great answer
                Final Answer: [ticker]

                Remember:
                - Always start with a Thought.
                - Provide your final answer in the specified format.
                - ONLY RETURN THE TICKER SYMBOL IF FOUND. DO NOT INCLUDE ANY UNNECESSARY WORDS OR PHRASES.
                """,
            max_iter=5,
            max_retry_limit=1,
            tools=[self.serper_tool],
            llm=get_llm(0),
            memory=True,
            verbose=True
        )

    def financial_analyst_agent(self) -> Agent:
        return Agent(
            role="Senior Financial Analyst",
            goal=
                """
                Conduct a thorough search to find the ten most recent financial news articles and blog posts related to the {self.company_name}.\n
                Analyze the articles and blog posts found and provide a comprehensive report on the stock market performance of the {self.company_name}.\n
                If you need more information, use the tools that you have to find more financial information on the {self.company_name}.
                IMPORTANT:
                - Do not include any unnecessary words or phrases in your response and only provide a detailed financial analysis on the ticker for {self.company_name}.
                """,
            backstory=
                """
                You are a Senior Financial Analyst that specializes in finding the most informative financial information on a specific company's stock market ticker symbol.
                """,
            agent_prompt = """
                You are an AI Financial Analyst agent tasked with searching the web to find the most relavant information on the stock market ticker symbol for the specified company name.
                
                Follow these steps:

                1. Think about what you need to do to complete the task.
                2. Choose an action from the available tools.
                3. Provide the action input as a dictionary.
                4. Observe the result of the action.
                5. Repeat steps 1-4 until you have enough information to provide a final answer.
                6. When ready to give a final answer, use the format:

                Thought: I now can give a great answer
                Final Answer: [Your comprehensive answer here]

                Remember:
                - Always start with a Thought.
                - Provide your final answer in the specified format.
                - If you cannot find an answer, do not make one up. Instead, return "Information not found".
                - You are to pass the headlines you recieved from the previous agent to the next agent for a financial sentiment analysis
                - you are also to pass you analysis to the next agent to add to the report.
                """,
            max_iter=5,
            max_retry_limit=1,
            tools=[self.serper_tool, self.scrape_website_tool, self.yahoo_finance_tool],
            llm=get_llm(0),
            memory=True,
            verbose=True

        )
    
    def sentiment_analyst_agent(self) -> Agent:
        return Agent(
            role="Senior Financial Sentiment Analyst",
            goal=
                """
                Take the financial news articles and blog posts related {self.company_name} from the Senior Financial Analyst agent, and using the correct tool, run a sentiment analysis on them.
                IMPORTANT:
                - Only use the tools provided below to complete your task.
                - Only use a tool to run the sentitment analysis.
                - Only conduct a sentiment analysis on the financial news articles and blog posts for {self.company_name} frovided by the previous agent.
                - Don't forget to save the document using a current timestamp!
                """,
            backstory=
                """
                You are a Senior Financial Sentiment Analyst that specializes in conducting the most informative financial sentiment analysis on a specific company and applying
                the most cutting-edge, up-to-date, and accurate sentiment analysis on the company's financial news and blog posts provided by the previous agent.
                """,
            agent_prompt = """
                You are an AI Senior Sentiment Analyst agent tasked with searching the web to find the most relavant financial news and blog posts on the stock market ticker symbol for the specified company name.
                
                Follow these steps:

                1. Think about what you need to do to complete the task.
                2. Make sure to take the headlines from the previous agent and run sentiment analysis on each headline
                3. YOU MUST RETURN SentementAnalysisToolOutput FOR ALL SENTIMENT ANALYSIS.
                4. When ready to give a final answer, use the format:

                Thought: I now can give a great answer
                Final Answer:\n
                [Your comprehensive financial sentiment analysis for {self.company_name} answer here]

                Remember:
                - Always start with a Thought.
                - Provide your final answer in the specified format.
                - If you cannot find an answer, do not make one up. Instead, return "Information not found".
                - When you have recieved the list of related news articles and blog posts from the previous agent, run them through the sentiment analysis tool to get the overall sentiment of each article.
                """,
            max_iter=5,
            max_retry_limit=1,
            tools=[self.sentiment_analysis_tool, self.get_timestamp_tool],
            llm=get_llm(0),
            memory=True,
            verbose=True

        )