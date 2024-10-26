from crewai import Agent, Task
# from models import CompanyInfo, FinancialAnalysis, SentimentAnalysis

class AgentTasks:
    def __init__(self, company_name) -> None:
        self.company_name = company_name
        self.timestamp = None
    
    def get_stock_ticker_task(self, agent: Agent):
        return Task(
            description=(
            ),
            agent=agent,
            expected_output=(
            ),
            output_json=CompanyInfo
        )
    

    def get_stock_information_task(self, agent: Agent, tasks: list[Task]):
        return Task(
            description=(
            ),
            agent=agent,
            expected_output=(
            ),
            context=tasks,
            output_pydantic="FinancialAnalysis"
        )

    def get_stock_sentiment_task(self, agent: Agent, tasks: list[Task]):
        return Task(
            description=(
            ),
            agent=agent,
            expected_output=(
            ),
            output_file=f"output/finacial_analysis{self.timestamp}.md",
            context=tasks,
            output_json=SentimentAnalysis
        )