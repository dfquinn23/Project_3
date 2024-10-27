from crewai import Agent, Task
from models import CompanyInfo, FinancialAnalysis, SentimentAnalysis

class AgentTasks:
    def __init__(self, company_name) -> None:
        self.company_name = company_name
    
    def get_stock_ticker_task(self, agent: Agent):
        return Task(
            description=(
            ),
            agent=agent,
            expected_output=(

            ),
            output_pydantic=CompanyInfo
        )

    def get_news_task(self, agent: Agent, tasks: list[Task]):
        return Task(
            description=(
            ),
            agent=agent,
            expected_output=(
            ),
            context=tasks,
            output_pydantic="FinancialAnalysis"
        )
    
    def get_analysis_task(self, agent: Agent, tasks: list[Task]):
        return Task(
            description=(
            ),
            agent=agent,
            expected_output=(
            ),
            context=tasks,
            output_pydantic=""
        )
    
    def get_sentiment_task(self, agent: Agent, tasks: list[Task]):
        return Task(
            description=(
                    "Conduct a financial sentiment analysis for all of the articles and blog posts that the previous agent provided."
                    "Remember to also get a timestamp for when you save the file."
                    "Dont forget to use the obtained timestamp in the saved file name."
            ),
            agent=agent,
            expected_output=(
                "A JSON object containing the {self.company_name}, ticker, and a summary of the research that you have done."
                "IMPORTANT:\n"
                "OUTPUT SHOULD LOOK LIKE:\n"
                "{\n"
                "'company_name': {self.company_name}',\n"
                "'ticker': [the found ticker for {self.company_name}]',\n"
                "'sentiment_analysis': 'your overall financial sentiment analysis summary goes here.'',\n"
                "'analysis': list[SentementAnalysisToolOutput]\n"
                "'average_sentiment_score': [float of an average sentimentscore]',\n"
                "}\n"
            ),
            output_file="output/finacial_analysis{timestamp}.md",
            context=tasks,
            output_json=SentimentAnalysis
        )