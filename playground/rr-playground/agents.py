from crewai import Agent, Task
from langchain.tools import Tool
from langchain_openai import OpenAI
from tools import StockAnalyzer
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if the API key is set
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Initialize OpenAI LLM with the API key
llm = OpenAI(api_key=api_key, model="gpt-4", temperature=0.3)

class StockAnalysisAgents:
    def __init__(self, llm, symbol):
        self.llm = llm
        self.symbol = symbol
        self.stock_analyzer = StockAnalyzer(symbol)

    def create_agents(self):
        agent_prompt = """
        You are an AI agent tasked with analyzing stock data. Follow these steps:

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
        - Use each tool only once.
        - Provide your final answer in the specified format.
        """

        news_scraper = Agent(
            role='News Scraper',
            goal='Collect and summarize relevant financial news headlines',
            backstory='Expert at gathering and summarizing financial news from various sources',
            tools=[Tool(
                name='get_news_headlines',
                func=self.stock_analyzer.get_news_headlines,
                description="Fetches recent news headlines for the given stock symbol"
            )],
            llm=self.llm,
            verbose=True,
            agent_prompt=agent_prompt
        )

        sentiment_analyzer = Agent(
            role='Sentiment Analyzer',
            goal='Analyze the sentiment of financial news and its potential impact on stock prices',
            backstory='Expert at determining market sentiment from financial news and correlating it with stock movements',
            tools=[Tool(
                name='analyze_headlines_sentiment',
                func=self.stock_analyzer.analyze_headlines_sentiment,
                description="Analyzes the sentiment of given news headlines"
            )],
            llm=self.llm,
            verbose=True,
            agent_prompt=agent_prompt
        )

        data_analyzer = Agent(
            role='Data Analyzer',
            goal='Analyze stock performance data and identify trends',
            backstory='Expert at analyzing financial data, identifying patterns, and making data-driven insights',
            tools=[
                Tool(
                    name='analyze_stock_performance',
                    func=self.stock_analyzer.analyze_stock_performance,
                    description="Analyzes the performance of a stock over a given period"
                ),
                Tool(
                    name='get_financial_metrics',
                    func=self.stock_analyzer.get_financial_metrics,
                    description="Fetches current financial metrics including daily high, low, volume, and market capitalization"
                )
            ],
            llm=self.llm,
            verbose=True,
            agent_prompt=agent_prompt
        )

        return news_scraper, sentiment_analyzer, data_analyzer

    def create_tasks(self, agents, days):
        tasks = []
        for i, agent in enumerate(agents):
            if i == 0:  # News Scraper
                task_description = f"Collect the most recent and relevant news headlines for {self.symbol} over the past {days} days."
                expected_output = "A list of recent and relevant news headlines with their dates and sources."
            elif i == 1:  # Sentiment Analyzer
                task_description = f"Analyze the sentiment of the collected news headlines for {self.symbol}."
                expected_output = "A summary of the sentiment analysis, including overall sentiment score and key factors influencing the sentiment."
            else:  # Data Analyzer
                task_description = f"Analyze the stock performance data and current financial metrics for {self.symbol}, including daily high, low, volume, and market capitalization."
                expected_output = "A comprehensive report on the stock's performance, including key metrics, trends, and any significant patterns observed."

            tasks.append(
                Task(
                    description=task_description,
                    agent=agent,
                    expected_output=expected_output
                )
            )
        
        return tasks

# Example of how to instantiate StockAnalysisAgents correctly
symbol = "AAPL"  # Replace with the actual stock symbol you want to analyze

stock_analysis_agents = StockAnalysisAgents(llm, symbol)

# Make sure this line is at the end of the file
__all__ = ['StockAnalysisAgents']
