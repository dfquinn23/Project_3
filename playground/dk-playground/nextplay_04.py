# Depenedencies
import os
import warnings
import openai
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, BaseTool, Tool
#from crewai.agent import Tool
from pydantic import BaseModel
from IPython.display import Markdown
from langchain_openai import OpenAI
import yfinance as yf


# Load from env file
load_dotenv()

# Filter warnings
warnings.filterwarnings('ignore')

# Load keys from .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_model_name = os.getenv("OPENAI_MODEL_NAME")
serper_api_key = os.getenv("SERPER_API_KEY")

# Initialize OpenAI LLM with the API key
llm = OpenAI(api_key=openai_api_key, model=openai_model_name, temperature=0.3)

# Instantiate tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()


# yfinance tool
class MyCustomTool(BaseTool):
    name: str = "stock_tool"
    description: str = "This tool gets stock details."

    def _run(self, argument: str) -> str:
        stock = yf.Ticker('TSLA')
        data = stock.history(period="max")
        return data



def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="max")
    return data

get_stock_data_tool = Tool(name="get_stock_data", func=get_stock_data)



# Agent: Investment Advisor
investment_advisor_agent = Agent(
    role = (
        "The Investment Advisor plays a critical role in guiding investment " 
        "decisions for the stock by coordinating with both the Equity Analyst and the " 
        "Sentiment Analysts to evaluate stocks comprehensively. " 
        "Upon receiving a stock for review, the Investment Advisor assigns " 
        "it to the appropriate analysts and they synthesize their findings. " 
        "With insights on financial health, market trends, and sentiment, " 
        "the Investment Advisor provides buy, sell, or hold recommendations, " 
        "along with the current stock price and sentiment score, ensuring " 
        "that decisions are data-driven and reflect assessments from both " 
        "of the analysts."
    ),
    goal = (
        "The primary goal of the Investment Advisor is to make informed " 
        "investment recommendations for the stock that align with the client interests. " 
        "By blending rigorous financial analysis with sentiment insights, " 
        "the Investment Advisor aims to maximize returns while effectively " 
        "managing risks. This role is essential in delivering actionable, " 
        "well-rounded investment guidance that considers both the numbers " 
        "and the nuances of market sentiment."
    ),
    backstory = (
        "The ideal Investment Advisor began their career with a background in " 
        "finance, economics, and business, initially focusing on client " 
        "advising and equity research. Over time, they honed skills in stock " 
        "evaluation, client communication, and portfolio strategy, often " 
        "working in roles that required collaboration across research and " 
        "analytical functions. With experience in both financial analysis " 
        "and a customer-focused approach, they developed a knack for " 
        "translating complex data into clear, actionable advice. " 
        "This unique combination of technical knowledge and strategic insight " 
        "enables the Investment Advisor to make recommendations that balance " 
        "profitability with risk management for clients and stakeholders."
    ),
    llm = llm,
    verbose = True,
    allow_delegation = True
)


# Agent: Sentiment Analyst
sentiment_analyst_agent = Agent(
    role = (
        "The Sentiment Analyst role focuses on interpreting and validating sentiment " 
        "analysis outputs for the stock, turning raw data into actionable insights and " 
        "identifies trends in sentiment that may impact investment strategy",
    ),
    goal = (
        "The goal of a Sentiment Analyst is to interpret and validate the " 
        "results of sentiment analysis for the stock to derive actionable insights that drive " 
        "investment decisions. Specifically, the objectives include: \n"
        "1. Identifying Trends and Patterns: Analyze sentiment data to detect " 
        "trends, emerging themes, or shifts in perception and opinion. \n"
        "2. Extracting Actionable Insights: Translate sentiment data into " 
        "insights that are meaningful for investors. \n"
        "3. Presenting Findings: Summarize sentiment analysis results as a score " 
        "bewteen -1 (very negitive) to 1 (very positive) for stakeholders making " 
        "complex data strategic investment decisions."
    ),
    backstory = (
        "The Sentiment Analyst has a background in psychology, linguistics, and " 
        "marketing, paired with strong analytical skills honed through experience " 
        "in customer insights or social media analytics. They have formalized " 
        "their data skills in tools like Python and NLP libraries, allowing them " 
        "to interpret complex sentiment data effectively. Experienced in " 
        "cross-functional collaboration, they bridge data with business and " 
        "investment strategy, drawing on their understanding of human behavior " 
        "to uncover meaningful insights. Their unique blend of empathy and " 
        "data-driven rigor enables them to identify trends and nuances in " 
        "customer sentiment that drive strategic investment decision-making."
    ),
    tools = [search_tool, scrape_tool, get_stock_data_tool], # revisit
    llm = llm,  # replace with Matt's slm
    verbose = True,
    allow_delegation = False
)


# Agent: Equity Analyst
equity_analyst_agent = Agent(
    role = (
        "The Equity Analyst role conducts research and analysis on the {stock}, " 
        "and trends to provide recommendations on specific stocks. " 
        "They analyze financial statements, company performance, and industry " 
        "conditions to inform investment decisions."
    ),
    goal = (
        "The goal of an Equity Analyst is to provide in-depth, accurate research " 
        "and actionable insights on the {stock} to guide investment decisions. " 
        "They aim to identify undervalued or overvalued stocks by analyzing " 
        "financial statements, market trends, industry conditions, and company " 
        "fundamentals. Their insights help portfolio managers, traders, and " 
        "clients make informed buy, hold, or sell decisions."
    ),
    backstory = (
        "An Equity Analyst has a background in finance, economics, and business. " 
        "They began their career in analytical roles, where they learned " 
        "financial modeling, valuation, and industry analysis. " 
        "They honed their ability to assess company fundamentals, market " 
        "conditions, and economic factors that drive stock performance. " 
        "Motivated by a blend of analytical precision and a passion for " 
        "uncovering investment opportunities, they advanced to provide " 
        "research-driven stock recommendations that inform and support " 
        "strategic investment decisions."
    ),
    tools = [search_tool, scrape_tool, get_stock_data_tool],
    llm = llm,
    verbose = True,
    allow_delegation = False
)



# Tasks
data_collection_and_preprocessing_task = Task(
    description = (
        "Gather data from sources using APIs and web scraping tools for {stock}. "
        "Clean, preprocess, and structure text data, including tasks like " 
        "removing noise, tokenizing, and standardizing language for sentiment "
        "analysis."
    ),
    agent = sentiment_analyst_agent,
    expected_output = (
        "Data that is ready for sentiment analysis"
    )
)

sentiment_analysis_and_evaluation_task = Task(
    description = (
        "Apply sentiment analysis models to categorize text data into positive, "
        "negative, or neutral sentiment and measure the strength of sentiment "
        "between -1 (very negitive) and 1 (very positive) for {stock}. Test and validate " 
        "model performance to improve model accuracy and ensure the analysis " 
        "captures nuanced sentiment changes over time."
    ),
    agent = sentiment_analyst_agent,
    expected_output = (
        "Evaluate for positive, negative, or neutral sentiment and measure the " 
        "strength of sentiment between -1 (very negitive) and 1 (very positive)."
    )
)


communication_and_recommendations_task = Task(
    description = (
        "Provide clear, actionable insights and strategic guidance based on " 
        "sentiment analysis findings of {stock}."
    ),
    agent = sentiment_analyst_agent,
    expected_output = (
        "1. Insight Report: A well-organized report summarizing key sentiment " 
        "trends, patterns, and any significant shifts over time. It should "
        "highlight noteworthy themes (e.g., customer satisfaction, " 
        "brand perception) and explain how sentiment aligns with recent events. \n"
        "2. Executive Summary and Strategic Recommendations: A set of actionable " 
        "investment recommendations.\n"
        "3. Sentiment Score: A sentiment score between -1 and 1."
    )
)


industory_and_market_research_task = Task(
    description = (
        "Research industry trends, market dynamics, and economic factors for {stock} that " 
        "could impact company performance, using both qualitative and " 
        "quantitative data to provide context for investment decisions."
    ),
    agent = sentiment_analyst_agent,
    expected_output = (
        "Comprehensive insights and context that help guide investment decisions: \n"
        "1. Industry Overview: A detailed summary of the industry landscape, " 
        "highlighting current trends, growth drivers, regulatory factors, and " 
        "challenges that impact the sector's performance. \n"
        "2. Market Trends: Projected growth rates and market forecasts for the " 
        "industry, providing context for performance expectations."
    )
)

stock_assignment_and_coordination_task = Task(
    description = (
        "Receives stock requests for {stock} and assigns each to the Equity Analyst for " 
        "financial analysis and the Sentiment Analyst for sentiment evaluation."
        "Ensures timely communication with analysts, and tracking progress to " 
        "maintain a smooth workflow."
    ),
    agent = investment_advisor_agent,
    expected_output = (
        "Organized tracking that assigns the stock to the Equity Analyst and " 
        "Sentiment Analyst. It should include basic stock details " 
        "(e.g., ticker symbol) and allow for progress tracking, ensuring the " 
        "process stays on schedule."
    )
)

synthesis_analyst_reports_task = Task(
    description = (
        "Collects and reviews the reports from the Equity and Sentiment " 
        "Analysts, ensuring all critical data and insights are compiled accurately. "
        "Synthesizes quantitative data (financial performance, valuation metrics) " 
        "and qualitative sentiment insights, transforming them into a clear " 
        "summary for decision-making for {stock}."
    ),
    agent = investment_advisor_agent,
    expected_output = (
        "A concise summary report that combines key insights from the Equity " 
        "and Sentiment Analysts. This should include essential financial metrics, " 
        "trends, sentiment highlights, and relevant qualitative and quantitative " 
        "insights. It serves as a reference for the Investment Advisor " 
        "final recommendation and provides a cohesive view of both " 
        "financial and sentiment data."
    )
)

recommendations_task = Task(
    description = (
        "Based on the combined findings, makes informed buy, sell, or hold " 
        "recommendations for the {stock}, considering both financial health and " 
        "market sentiment. Justifies recommendations with concise explanations " 
        "that balance market trends, sentiment shifts, and other factors."
    ),
    agent = investment_advisor_agent,
    expected_output = (
        "A clear, action-oriented recommendation (buy, sell, or hold) for each " 
        "stock, accompanied by a brief rationale. This should include a summary " 
        "of findings that support the recommendation, touching on the financial " 
        "outlook, sentiment trends, and any risk considerations. " 
        "The recommendation should be formatted in a way that is easily " 
        "understood by clients and internal stakeholders."
    )
)

provide_stock_price_and_sentiment_score_task = Task(
    description = (
        "Updates each recommendation with the current stock price and includes " 
        "the sentiment score from the Sentiment Analyst report for the {stock}."
    ),
    agent = investment_advisor_agent,
    expected_output = (
        "A final report or communication that includes the Investment Advisor " 
        "recommendation along with the current stock price and sentiment score. " 
        "The stock price should be up-to-date, reflecting recent market activity, " 
        "while the sentiment score should summarize the sentiment analyst findings " 
        "(e.g., a numerical score or qualitative summary of positive, neutral, " 
        "or negative sentiment). This output gives clients a comprehensive " 
        "snapshot of the stock standing and the Advisor final guidance."
    )
)


# Define the crew with agents and tasks
financial_sentiment_trading_crew = Crew(
    agents=[investment_advisor_agent,
            sentiment_analyst_agent,
            equity_analyst_agent
    ],
    
    tasks=[data_collection_and_preprocessing_task,
           sentiment_analysis_and_evaluation_task,
           communication_and_recommendations_task,
           industory_and_market_research_task,
           stock_assignment_and_coordination_task,
           synthesis_analyst_reports_task,
           recommendations_task,
           provide_stock_price_and_sentiment_score_task,
    ],
    
    manager_llm=llm,
    process=Process.hierarchical,
    verbose=True
)


# Run the Crew
#inputs = {
#    "stock": "TSLA",
#}

#result = crew.kickoff(inputs=inputs)
result = crew.kickoff('TSLA')

# Display the results
Markdown(result)