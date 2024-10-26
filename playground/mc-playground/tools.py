from langchain_ollama.llms import OllamaLLM
# from langchain_community.llms.ollama import Ollama
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
from typing import List, Type


llm = OllamaLLM(model="mattarad/llama3.2-1b-instruct-mqc-sa", temperature=0.25)
# llm = Ollama(model="Llama-3.2-3B-Instruct-LoRa-mqc-Sentiment_Analysis:0.77", temperature=0.9)


class SentementAnalysisToolInput(BaseModel):
    text: str = Field(..., description="The text you want to run a sentiment analysis on.")

class SentementAnalysisToolOutput(BaseModel):
    reasoning: str
    sentiment_score: float
    confidence_score: float

class SentimentAnalysisTool(BaseTool):
    name: str = "Sentiment Analysis Tool"
    description: str = "This tool analyzes the sentiment of a given text and returns the a SentementAnalysisToolOutput."
    args_schema: Type[BaseModel] = SentementAnalysisToolInput

    def _run(self, input_data: SentementAnalysisToolInput) -> SentementAnalysisToolOutput:
        self.call_sentiment_slm(input_data.text)

    def call_sentiment_slm(text: str) -> SentementAnalysisToolOutput:
        print(text)
        # prompt = [
        #     {'content': 'You are an advanced AI assistant created to perform sentiment analysis on text. Your task is to carefully read the text and analyze the sentiment it expresses towards the potential future stock value of any company mentioned.  Analyze the sentiment of this text and respond with the appropriate JSON:',
        #     'role': 'system'},
        #     {'content': text,
        #     'role': 'user'}
        # ]
        result = llm.invoke(text)
        print(result)
        return result


# def get_llm() -> LLM:
#     return LLM(model="Llama-3.2-3B-Instruct-LoRa-mqc-Sentiment_Analysis:0.77", temperature=0.5)
# call_sentiment_slm("where is the taco stand?")
