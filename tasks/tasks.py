from crewai import Agent, Task

class AgentTasks():
    def __init__(self, ticker: str):
        self.ticker = ticker
    
    def search_stock_twits_task(self, agent: Agent, tasks: list[Task]) -> Task:
        return Task(
            description=(
                f"Search for recent Sentiment and Message Volume on https://stocktwits.com related to the stock {self.ticker}. "
            ),
            agent=agent,
            expeceted_output_type=(
                "A JSON object containing the Sentiment Message Volume and timestamp for the ticker symbol."
            ),
            context=tasks,
            # output_json=StockTwitsOutput
        )