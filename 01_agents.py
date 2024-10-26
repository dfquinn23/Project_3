from crewai import Agent, LLM

class AgentSea():
    # TODO ADD TOOLS
    def __call__(self):
        print(f"The Sea of Agents is initializing...")
        print(f"please wait.")

        self.llm = LLM(model='ollama/crewai-llama3:latest')

    def stock_twits_agent(self, ticker: str) -> Agent:
        return Agent(
            role="Stock Twits Research Analyst",
            goal=(
                "To provide the current Sentiment and Message Volume for the {ticker} from https://stocktwits.com/symbol/{ticker}"
                "Thoroughly analyze the website to extract the Sentiment and Message Volume."
                "IMPORTANT:\n"
                "- The final output should be a list of JSON objects and must include the Sentiement, Message Volume, and Timestamp in UTC.\n"
                "- Ensure that the timestamp is accurate to the minute.\n"
                "- Make sure that if you cannot find the Sentiment you put 0 for Sentiment.\n"
                "- Make sure that if you cannot find the Message Volume tha tyou put 0 for Message Volume.\n"
                "Example Output:\n"
                "{\n"
                "'sentiment: {sentiment},\n"
                "'message_volume: {message_volume},\n"
                "'timestamp: {timestamp},\n"
                "}\n"
            ),
            backstory=(
                "As the Stock Twits Research Analyst, you are an a Stock Twits scraper and can find Sentiment and Message Volume for any stock ticker"
                "on https://stocktwits.com. You are responsible for finding the current Sentiment and Message Volume for the {ticker}."
            )
        ),



