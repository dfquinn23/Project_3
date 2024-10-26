from crewai import Agent, Task
from models import CompanyInfo, FinancialAnalysis, SentimentAnalysis

class AgentTasks:
    def __init__(self, company_name) -> None:
        self.company_name = company_name
    
    def get_stock_ticker_task(self, agent: Agent):
        return Task(
            description=(
                    "Conduct a thorough research about the company and find the correct stock market ticker symbol for {self.company_name}."
            ),
            agent=agent,
            expected_output=(
                "A JSON object containing the company name and the company's stock market ticker symbol. For example: 'AAPL' would be for the Apple."
                "IMPORTANT:\n"
                "OUTPUT SHOULD LOOK LIKE:\n"
                "{\n"
                "'company_name': {self.company_name}',\n"
                "'ticker': 'the ticker symbol you found'',\n"
                "}\n"
            ),
            # context=tasks,
            output_json=CompanyInfo
        )

    def get_stock_information_task(self, agent: Agent, tasks: list[Task]):
        return Task(
            description=(
                    "Conduct a thorough financial analysis about the company using the correct stock market ticker symbol for {self.company_name}."
                    "The stock market ticker symbol should be obtained from the previous task."
            ),
            agent=agent,
            expected_output=(
                "A JSON object containing the company_name, ticker, and a summary of the research that you have done."
                "IMPORTANT:\n"
                "OUTPUT SHOULD LOOK LIKE:\n"
                "{\n"
                "'company_name': {self.company_name}',\n"
                "'ticker': [the found ticker for {self.company_name}]',\n"
                "'financial_analysis': [your financial analysis summary goes here.]',\n"
                "}\n"
            ),
            context=tasks,
            output_pydantic=FinancialAnalysis
        )
    
    def get_stock_sentiment_task(self, agent: Agent, tasks: list[Task]):
        return Task(
            description=(
                    "Conduct a thorough financial sentiment analysis for the FinancialAnalysis[list[financial_analysis]] that the previous agent provided."
                    "the list of finacial news articls and blog posts should be obtained from the previous agent."
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
            output_file="finacial_analysis.md",
            context=tasks,
            output_json=SentimentAnalysis
        )