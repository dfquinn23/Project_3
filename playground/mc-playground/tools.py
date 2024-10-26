from datetime import datetime, timezone
from langchain_ollama.llms import OllamaLLM
# from langchain_community.llms.ollama import Ollama
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
from typing import List, Type

# 1B model
llm = OllamaLLM(model="mattarad/llama3.2-1b-instruct-mqc-sa", temperature=0.25)
# 3B model
# llm = OllamaLLM(model="mattarad/llama3.2-3b-instruct-mqc-sa", temperature=0.25)

# newer version of langchain_community
# 1B model
# llm = Ollama(model="mattarad/llama3.2-1b-instruct-mqc-sa", temperature=0.25)
# 3B model
# llm = Ollama(model="mattarad/llama3.2-3b-instruct-mqc-sa", temperature=0.25)


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

class TimestampOutput(BaseModel):
    timemstamp: str

class GetTimestampTool(BaseTool):
    name: str = "Get Timestamp Tool"
    description: str = "This tool is used to obtain a timestamp"

    def _run(self) -> TimestampOutput:
        
        return str(datetime.timestamp())
