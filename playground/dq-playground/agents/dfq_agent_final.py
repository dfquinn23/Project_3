from crewai import Agent, LLM
from crewai_tools import ScrapeWebsiteTool, SerperDevToo
search_tool = SerperDevToo()
scrape_tool = ScrapeWebsiteTool()

"""
Purpose:
    1. Our agents will be tasked with performing sentiment analysis of user-inputted stocks over a spoecific date range
    2. Agent 1 is the ChatBot responsible for interfacing with the user and obtaining the search data
    3. Agent 2 is our Researchbot. He will take the ticker and date range from Chatbot and conduct a search for for recent articles, blog posts, social meadia mentions headlines.
    4. Agent 3 is the Writerbot, who is tasked with creating the sentiment analysis report

"""

class Sentiment_Agents:
    def __init__(self):
        self.manager_llm = LLM(model="ollama/mattarad/llama3.2-3b-instruct-mqc-sa", temperature=0.3)
        
    def chatbot_agent(self):
        return Agent(
            role = "chatbot",
            goal =
                """
                1. Take the user's input, which will be either a company name or stock ticker, as well as the date range they want to search for.
                """,
                backstory=
                """
                1. You work in the front lines of customer service.
                2. Our customers come to you when they want to obtain our company's sentiment analysis for various stocks over a specific date range.
                3. You pride yourself on being fast, courteous, and accurate
                """,
            verbose=True,
            allow_delegation=True,
            memory=True
          )

    def Researchbot_agent(self):
        return Agent(
            role = "Researcher",
            goal =
            """
                1. Receive the input data from the Chatbot_agent.
                2. Conduct a "sentiment analysis" search for the ticker and date range information received from the chatbot_agent.
                3. Pass your findings off to the writer_agent
            """,
            backstory=
            """
                1. You have many years of experience conducting investment research.
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

    def Writerbot_agent(self):
        return Agent(
            role="Report Writer",
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