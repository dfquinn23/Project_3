from crewai import Agent, LLM
from crewai_tools import ScrapeWebsiteTool, SerperDevToo
search_tool = SerperDevToo()
scrape_tool = ScrapeWebsiteTool()

"""
Purpose:
    1. Our agents will be tasked with performing sentiment analysis of user-inputted stocks over a spoecific date range
    2. Agent 1 is the Ticker Agent responsible for taking comanmy name and returning the ticker
    3. Agent 2 is our Researcher. He will take the ticker from Chatbot and conduct a search for for recent articles, blog posts, social meadia mentions headlines.
    4. Agent 3 is the Analyst, who is tasked with creating the sentiment analysis report
    4. Agent 4 is the Sentiment Analyst

"""

class Sentiment_Agents:
    def __init__(self):
        self.manager_llm = LLM(model="ollama/mattarad/llama3.2-3b-instruct-mqc-sa", temperature=0.3)
        
    def ticker_agent(self):
        return Agent(
            role = "Ticker Agent",
            goal =
                """
                1. Take the user's input, which will be either a company name or stock ticker, as well as the date range for which they want to search.
                """,
                backstory=
                """
                1. You work in the front lines of customer service.
                2. Our customers come to you when they want to obtain our company's sentiment analysis for various stocks over a specific date range.
                3. You pride yourself on being fast, courteous, and accurate.
                """,
            verbose=True,
            allow_delegation=True,
            memory=True
          )

    def research_agent(self):
        return Agent(
            role = "Researcher",
            goal =
            """
                1. Receive the stock symbol from the Ticker Agent.
                2. Conduct a search for recent news about that ticker symbol.
                3. Pass your findings off to the Analyst Agent
            """,
            backstory=
            """
                1. You are an expert at finding the best news articles with many years of experience conducting investment research.
                2. Your area of expertise is in conducting sentiment analysis.
                3. Your research sources include social media, news outlets, forums and blogs, and company communications.
                4. You pride yourself on being thorough, detailed, accurate, and comprehensive
                5. Do not make any assumptions or provide any information that cannot be independently verified.
            """,
            verbose=True,
            allow_delegation=True,
            memory=True,
            tools = [search_tool, scrape_tool]
)

    def analyst_agent(self):
        return Agent(
            role="Analyst",
            backstory=
                """"
                1. You are a highly experienced writer with specialization in creating investment research reports
                2. Your writing style is conversational and engaging, yet professional.
                3. For sentiment analysis reports like the ones you are creating here, you leverage your analytical and interpretative skills to offer insightful recommendations.
                """,
            goal="""
                1. Receive the research from the Researchbot_agent and write your sentiment analysis report.
                2. These reports should be engaging, easily-understood, and relatively jargon-free.
                3. These reports should provide an analysis of the research, provide a sentiment score of -1 (negaticve), 0 (neutral), or 1 (positive).
                    You must be able to explain why you scored the stock as you did, with citations if possible.
            """,
            verbose=True,
            manager_llm = manager_llm
        )

def sentiment_agent(self):
        return Agent(
            role="Senior Financial Sentiment Analyst",
            backstory=
                """"
                1. You are a Senior Financial Sentiment Analyst\n
                2. You specialize in conducting an informative financial sentiment analysis on a specific company
                3. .
                """,
            goal="""
                1. Take the financial news articles and blog posts related to {self.company_name} from the previous agent.
                2. Run a financial sentiment analysis on the articles and blog posts provided by the previous agent.
                3. Get the current timestamp.
                IMPORTANT:
                - Only use the tools provided below to complete your task.
                - Only conduct a sentiment analysis on the financial news articles and blog posts for {self.company_name} frovided by the previous agent.
                - Don't forget to save the document using a current timestamp!
            """,
            verbose=True,
            llm = LLM(model="ollama/llama3:latest", temperature=0.3)
        )
