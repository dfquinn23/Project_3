from crewai import Agent, Task, Crew

from pd_models import CompanyInfo, FinancialAnalysis, SentimentAnalysis

class AgentTasks:
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
                    f"Conduct a thorough financial analysis about the company using the correct stock market ticker symbol for {self.company_name}."
                    "The stock market ticker symbol should be obtained from the previous task."
            ),
            agent=agent,
            expected_output=(
                "A JSON object containing the company_name, ticker, and a summary of the research that you have done."
                "IMPORTANT:\n"
                "OUTPUT SHOULD LOOK LIKE:\n"
                "{\n"
                "'company_name': {self.company_name}',\n"
                "'ticker': 'ticker'',\n"
                "'financial_analysis': 'your financial analysis summary goes here.'',\n"
                "}\n"
            ),
            context=tasks,
            output_json=FinancialAnalysis
        )
    
    def get_stock_sentiment_task(self, agent: Agent, tasks: list[Task]):
        return Task(
            description=(
                    f"Conduct a thorough search for financial news articles and blog posts about the company using the correct stock market ticker symbol for {self.company_name}."
                    "The stock market ticker symbol should be obtained from the previous task."
            ),
            agent=agent,
            expected_output=(
                "A JSON object containing the company_name, ticker, and a summary of the research that you have done."
                "IMPORTANT:\n"
                "OUTPUT SHOULD LOOK LIKE:\n"
                "{\n"
                "'name': name of article',\n"
                "'article': name of article',\n"
                "'sentiment_analysis': 'your sentiment analysis summary goes here.'',\n"
                "'analysis': list[SentementAnalysisToolOutput]\n"
                "}\n"
            ),
            context=tasks,
            output_json=SentimentAnalysis
        )