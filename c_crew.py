from crewai import Crew, Process
from a_agents import ResearchAgents
from b_tasks import AgentTasks

class CompanyResearchCrew:
    def __init__(self, company: str):
        self.company = company
        self.crew = None

    def setup_crew(self):
        print(f"Setting up crew for {self.company}")
        agents = ResearchAgents(self.company)
        ticker_agent = agents.ticker_agent()
        research_agent = agents.research_agent()
        analyst_agent = agents.analyst_agent()
        sentiment_agent = agents.sentiment_agent()

        tasks = AgentTasks(self.company)

        task_01 = tasks.get_stock_ticker_task(ticker_agent)
        task_02 = tasks.get_news_task(research_agent, [task_01])
        task_03 = tasks.get_analysis_task(analyst_agent, [task_01, task_02])
        task_04 = tasks.get_sentiment_task(sentiment_agent, [task_01, task_02, task_03])

        self.crew = Crew(
            tasks=[task_01, task_02, task_03, task_04],
            process=Process.sequential,
            verbose=True
        )


    def kickoff(self):
        if not self.crew:
            print(f"No crew found for {self.company}")
            return
        try:
            print(f"Running crew for company: {self.company}")
            result = self.crew.kickoff()
            return result
        except Exception as e:
            print(f"Error running crew: {e}")
            return str(e)
