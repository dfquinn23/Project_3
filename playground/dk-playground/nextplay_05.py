# Dependencies
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from langchain_openai import ChatOpenAI
import openai
from IPython.display import Markdown


# Load keys from .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_model_name = os.getenv("OPENAI_MODEL_NAME")
serper_api_key = os.getenv("SERPER_API_KEY")


# Initialize OpenAI LLM with the API key
#llm = OpenAI(api_key=openai_api_key, model=openai_model_name, temperature=0.3)


# Instantiate tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()


# Agents
collect_news_agent = Agent(
    role='News Collector',
    goal='Collect and summarize financial news',
    backstory='Expert at gathering and summarizing financial news',
    tools=[search_tool, scrape_tool],
    verbose=True,
)


sentiment_analysis_agent = Agent(
    role='Sentiment Analysis',
    goal='Analyze the sentiment of news and its impact on stock prices',
    backstory='Expert at determining sentiment from news articles about stocks',
    tools=[search_tool, scrape_tool],
    verbose=True,
)


# Tools
stock_analysis_task = Task(
    description='Analyze market data for {stock} to identify trends and predict market movements.',
    expected_output='Sentiment score for {stock}',
    agent=sentiment_analysis_agent,
)


# Crew
sentiment_crew = Crew(
    agents=[collect_news_agent,
            sentiment_analysis_agent],
    tasks=[stock_analysis_task],
    manager_llm=ChatOpenAI(model=openai_model_name, temperature=0.7),
    process=Process.hierarchical,
    verbose=True
)


# Stock
stock_selection = {'stock' : 'TSLA'}


# Kickoff
result = sentiment_crew.kickoff(inputs=stock_selection)


# Display
Markdown(result)