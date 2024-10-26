# Agent1 is our Chatbot that takes the information from the user wrt
# company/ticker and date range for analysis
# Agent2 is our Researchbot that takes the info from Agent1 and heads
# out into cyberspace to look for headlines and news stories around that
# ticker and data range.
# Agent3 is our Analyzerbot that parses the returned information
# and makes recommendations.

# Data sources: Reddit, Twitter (researchbo32829, daniel_quinn@rocketmail.com, aibootcamp2024),
# YahooFinance

import warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew, Process, LLM
import os
from dotenv import load_dotenv

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
os.environ["OPENAI_MODEL_NAME"]='gpt-4-turbo'

from crewai_tools import ScrapeWebsiteTool, SerperDevTool

#Chatbot_Agent will take the ticker, company,. date range info from the user in later
# version - here, these will be encoded

chatbot_agent = Agent(
    role = "chatbot",
    goal = "Take the user's input, which will be either a company name or "
        "the company's stock ticker, as well as the date range they want to search for.",
    backstory= "You work in the front lines of customer service. Our customers "
        "come to you when they want to obtain our company's sentiment analysis "
        "for various stocks over s specific date range. You pride yourself on " 
        "being fast, courteous, and accurate.",
    verbose=True,
    allow_delegation=True,
    memory=True
)

chatbot_task = Task(
    description= "Take either a company name or its ticker from the user, as well a date range for the search. If they " 
        "provide a ticker, confirm the input by returning the name of the company. " 
        "If they provide the company, confirm the input by returning the ticker." 
        "Also, confirm the date range.",
    expected_output=("A simple conversation that states the user's choices of {ticker}, {company}, and {dates}"),
    agent = chatbot_agent
    )

manager_llm=LLM(model="ollama/mattarad/llama3.2-3b-instruct-mqc-sa", temperature=0.3)

chatbot_crew = Crew(
    agents = [chatbot_agent],
    tasks=[chatbot_task],
    #manager_llm = manager_llm,
    process=Process.sequential,
    verbose=True
)

company_or_ticker = input("Please enter the company name or ticker: ")
date_range = input("Please enter the date range")

user_input = {
     "company": company_or_ticker if not company_or_ticker.isupper() else "",
     "ticker": company_or_ticker if not company_or_ticker.isupper() else "",
     "dates": date_range
 }

result = chatbot_crew.kickoff(user_input)