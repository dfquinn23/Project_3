from crewai import Agent, Task
from models import CompanyInfo, FinancialAnalysis, SentimentAnalysis

class AgentTasks:
    def __init__(self, company_name) -> None:
        self.company_name = company_name
        self.timestamp = None
    
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
                f"'company_name': {self.company_name}',\n"
                "'ticker': 'the ticker symbol you found'',\n"
                "}\n"
            ),
            # context=tasks,
            output_json=CompanyInfo
        )
    

    def get_stock_information_task(self, agent: Agent, tasks: list[Task]):
        return Task(
            description=(
                    f"Conduct a thorough research about {self.company_name} for 10 of the current financial"
                    "news articles and blogs."
                    "Conduct a thorough financial analysis using your research."
                    "You are to analze ten of the most recent articles and posts and conduct a thorough financial analysis about the company.\n"
                    "You are to obtain ten of the most recent financial news articles and blog posts and pass them\n"
                    "to the Senior Financial Sentiment Analyst"
            ),
            agent=agent,
            expected_output=(
                "A JSON object containing the company_name, ticker, and a summary of the research that you have done."
                "IMPORTANT:\n"
                "OUTPUT SHOULD LOOK LIKE:\n"
                "{\n"
                f"'company_name': {self.company_name}',\n"
                f"'ticker': [the found ticker for {self.company_name}]',\n"
                "'financial_summary': [your financial analysis summary goes here.]',\n"
                "}\n"
            ),
            context=tasks,
            output_pydantic=FinancialAnalysis
        )

    def get_stock_sentiment_task(self, agent: Agent, tasks: list[Task]):
        return Task(

            description=(
                    "Conduct a financial sentiment analysis for the news articles and blog posts that the previous agent provided."
                    "Remember to also get a timestamp for when you save the file and save the timestamp to {self.timestamp}"
                    "Dont forget to use the obtained timestamp in the saved file name."
                    "example of saved file name: [finacial_analysis[timestamp].md]"
            
            ),

            agent=agent,
            expected_output=(
                f"A JSON object containing the {self.company_name}, ticker, and a summary of the research that you have done."
                "IMPORTANT:\n"
                "OUTPUT SHOULD LOOK LIKE:\n"
                "{\n"
                f"'company_name': {self.company_name}',\n"
                f"'ticker': [the found ticker for {self.company_name}]',\n"
                f"'timestamp': '[the timestamp you found]',\n"
                f"'financial_summary': '[the financial summary provided by the previous agent]',\n"
                "'sentiment_analysis': 'your overall financial sentiment analysis summary goes here.'',\n"
                "'analysis': list[SentementAnalysisToolOutput]\n"
                "'average_sentiment_score': [float of an average sentimentscore]',\n"
                "}\n"
            ),
            output_file=f"output/finacial_analysis{self.timestamp}.md",
            context=tasks,
            output_json=SentimentAnalysis
        )