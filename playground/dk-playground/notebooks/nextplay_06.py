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
investment_advisor_agent = Agent(
    role = """
        The Investment Advisor Agent plays a critical role in guiding investment 
        decisions for the stock by coordinating with both the Equity Analyst Agent and the 
        Sentiment Analyst Agent to evaluate a stock.  
        Upon receiving a stock for review, the Investment Advisor Agent assigns 
        it to the appropriate analyst and synthesizes their findings.  
        With insights on stock price and sentiment,  
        the Investment Advisor Agent provides buy, sell, or hold recommendations,  
        along with the current stock price and sentiment score, ensuring  
        that decisions are data-driven and reflect assessments from both  
        of the analysts.""",
    goal = """The primary goal of the Investment Advisor Agent is to make informed  
        investment recommendations for the stock by blending rigorous financial 
        analysis of the price with sentiment insights. This role is essential in 
        delivering actionable, well-rounded investment guidance that considers 
        both the numbers and the nuances of market sentiment.""",
    backstory = """The ideal Investment Advisor Agent began their career with a background in  
        finance, economics, and business, initially focusing on client  
        advising and equity research. Over time, they honed skills in stock  
        evaluation, client communication, and portfolio strategy, often  
        working in roles that required collaboration across research and  
        analytical functions. With experience in both financial analysis  
        and a customer-focused approach, they developed a knack for  
        translating complex data into clear, actionable advice.  
        This unique combination of technical knowledge and strategic insight 
        enables the Investment Advisor Agent to make recommendations.""",
    #tools=[search_tool, scrape_tool],
    verbose = True,
    allow_delegation = True
)


sentiment_analyst_agent = Agent(
    role = """The Sentiment Analyst Agent role focuses on interpreting and validating sentiment 
        analysis outputs for the stock, turning raw data into actionable insights and 
        identifies trends in sentiment that may impact investment recommendations""",
    goal = """
        The goal of a Sentiment Analyst is to interpret and validate the  
        results of sentiment analysis for the stock. Specifically, the objectives include: 
        1. Identifying Trends and Patterns: Analyze sentiment data to detect 
        trends, emerging themes, or shifts in perception and opinion. 
        2. Extracting Actionable Insights: Translate sentiment data into  
        insights that are meaningful for investors. 
        3. Presenting Findings: Summarize sentiment analysis results as a score 
        bewteen -1 (very negitive) to 1 (very positive).""",
    backstory = """The Sentiment Analyst Agent has a background in psychology, linguistics, and 
        marketing, paired with strong analytical skills. They have formalized  
        their data skills in tools like Python and NLP libraries, allowing them  
        to interpret complex sentiment data effectively. Experienced in  
        cross-functional collaboration, they bridge data with business and  
        investment strategy, drawing on their understanding of human behavior  
        to uncover meaningful insights. Their unique blend of empathy and  
        data-driven rigor enables them to identify trends and nuances in  
        customer sentiment that drive strategic investment decision-making.""",
    #tools=[search_tool, scrape_tool],
    verbose=True,
    allow_delegation = False,
)



equity_analyst_agent = Agent(
    role ="""The Equity Analyst Agent role conducts research and analysis on the stock,  
        and trends to provide recommendations.""",
    goal = """The goal of an Equity Analyst Agent is to provide in-depth, accurate research  
        and actionable insights on the stock to guide investment decisions.  
        Their insights help the Investment Advisor Agent 
        make informed buy, hold, or sell decisions.""",
    backstory = """An Equity Analyst Agent has a background in finance, economics, and business.  
        They began their career in analytical roles, where they learned  
        financial modeling, valuation, and industry analysis.""",
    #tools = [search_tool, scrape_tool], # add stock tool
    #llm = llm,
    verbose = True,
    allow_delegation = False
)

"""
## OLD
collect_news_agent = Agent(
    role='News Collector',
    goal='Collect and summarize financial news',
    backstory='Expert at gathering and summarizing financial news',
    tools=[search_tool, scrape_tool],
    verbose=True,
    allow_delegation = False

)


sentiment_analyst_agent = Agent(
    role='Sentiment Analysis',
    goal='Analyze the sentiment of news and its impact on stock prices',
    backstory='Expert at determining sentiment from news articles about stocks',
    tools=[search_tool, scrape_tool],
    verbose=True,
    allow_delegation = False
)
"""


# Task
stock_analysis_task = Task(
    description='Analyze market data for {stock} to identify trends and predict market movements.',
    expected_output='Sentiment score for {stock}',
    agent=investment_advisor_agent
)


# Crew
sentiment_crew = Crew(
    agents=[investment_advisor_agent,
            equity_analyst_agent,
            sentiment_analyst_agent],
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