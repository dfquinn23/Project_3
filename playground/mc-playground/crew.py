from crewai import Crew, Process

from agents import AgentSea
from tasks import AgentTasks
    
class CompanyResearchCrew:
    def __init__(self, company_name: str):
        self.company_name = company_name
        self.crew = None
    
    def setup_crew(self, company_name: str):
        print(f"Setting up crew for: {self.company_name}")
        agents = AgentSea(self.company_name)
        ticker_agent = agents.create_ticker_finder_agent()

        financial_agent = agents.financial_analyst_agent()
        sentiment_agent = agents.sentiment_analyst_agent()
        
        tasks = AgentTasks(self.company_name)
        task_01 = tasks.get_stock_ticker_task(ticker_agent)


        task_02 = tasks.get_stock_information_task(financial_agent, [task_01])
        task_03 = tasks.get_stock_sentiment_task(sentiment_agent, [task_01, task_02])


        self.crew = Crew(
            agents=[ticker_agent, financial_agent, sentiment_agent],
            tasks=[task_01, task_02, task_03],
            process=Process.sequential,
            verbose=True,
            
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