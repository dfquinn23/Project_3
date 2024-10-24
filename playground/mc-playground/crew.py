from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from langchain_openai import OpenAI

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")


from pydantic import BaseModel
class CompanyInfo(BaseModel):
    company_name: str
    ticker: str

def get_llm(num: int) -> LLM:
    if num == 0: 
        return LLM(
            model="grok-beta",
            base_url="https://api.x.ai/v1",
            api_key=XAI_API_KEY,
        )
    if num == 1:
        return LLM(model="ollama/llama3:latest", temperature=0.7)
    else:
        return OpenAI(api_key=OPENAI_API_KEY, model="gpt-4", temperature=0.3)

class AgentSea:
    def __init__(self, company_name: str):
        self.company_name = company_name
        self.serper_tool = SerperDevTool()
        self.scrape_website_tool = ScrapeWebsiteTool()
    
    def create_ticker_finder_agent(self) -> Agent:
        return Agent(
            role="Senior Online Researcher",
            goal=
                """
                Conduct an amazing online search to find the stock ticker for {self.company_name}.
                IMPORTANT:
                - If you cannot find the result, return "Ticker not found".
                - Do not include any unnecessary words or phrases in your response and only provide the ticker symbol if found.
                """,
            backstory=
                """
                You are a Senior Online Researcher that specializes in finding a company's stock martket ticker symbol with only the company name.
                """,
            agent_prompt = """
                You are an AI agent tasked with searching the web to find the stock market ticker symbol for the specified company name.
                
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
                """,
            max_iter=5,
            max_retry_limit=3,
            tools=[self.serper_tool, self.scrape_website_tool],
            llm=get_llm(1),
            verbose=True
        )

class Tasks:
    def __init__(self, company_name) -> None:
        self.company_name = company_name
    
    def get_stock_ticker_task(self, agent: Agent):
        return Task(
            description=(
                    f"Conduct a thorough research about the company and find the correct stock market ticker symbol for {self.company_name}."
            ),
            agent=agent,
            expected_output=(
                "A JSON object containing the company name and the company's stock market ticker symbol. For example: 'AAPL' would be for the Apple."
            ),
            # context=tasks,
            # output_json=CompanyInfo
        )
    
class CompanyResearchCrew:
    def __init__(self, company_name: str):
        self.company_name = company_name
        self.crew = None
    
    def setup_crew(self, company_name: str):
        print(f"Setting up crew for: {self.company_name}")
        agents = AgentSea(self.company_name)
        ticker_agent = agents.create_ticker_finder_agent()
        
        tasks = Tasks(self.company_name)
        task = tasks.get_stock_ticker_task(ticker_agent)


        self.crew = Crew(
            agents=[ticker_agent],
            tasks=[task],
            verbose=True
        )


    def kickoff(self):
        if not self.crew:
            print(f"No crew found for {self.company_name}")
            return
        try:
            print(f"Running crew for job {self.company_name}")
            result = self.crew.kickoff()
            return result
        except Exception as e:
            return str(e)
        
crew = CompanyResearchCrew("Tesla")
crew.setup_crew("Tesla")
res = crew.kickoff()

print(res)