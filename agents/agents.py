from crewai import Agent, LLM

class AgentSea():
    def __init__(self):
        print("The Sea of Agents is initializing...")
        print("Please wait.")
        self.llm = LLM(provider="anthropic", model="claude-3-opus-20240229")

    def stock_twits_agent(self, ticker: str) -> Agent:
        return Agent(
            role="Stock Twits Research Analyst",
            goal=(
                f"To provide the current Sentiment and Message Volume for the {ticker} from https://stocktwits.com/symbol/{ticker}. "
                "Thoroughly analyze the website to extract the Sentiment and Message Volume. "
                "IMPORTANT:\n"
                "- The final output should be a JSON object and must include the Sentiment, Message Volume, and Timestamp in UTC.\n"
                "- Ensure that the timestamp is accurate to the minute.\n"
                "- Make sure that if you cannot find the Sentiment you put 0 for Sentiment.\n"
                "- Make sure that if you cannot find the Message Volume that you put 0 for Message Volume.\n"
                "Example Output:\n"
                "{\n"
                "'sentiment': {sentiment},\n"
                "'message_volume': {message_volume},\n"
                "'timestamp': '{timestamp}'\n"
                "}\n"
            ),
            backstory=(
                f"As the Stock Twits Research Analyst, you are a Stock Twits scraper and can find Sentiment and Message Volume for any stock ticker "
                f"on https://stocktwits.com. You are responsible for finding the current Sentiment and Message Volume for the {ticker}."
            ),
            llm=self.llm
        )


