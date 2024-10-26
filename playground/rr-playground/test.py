# Import required libraries
from crewai import Crew
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

# Import our custom modules
from agents import StockAnalysisAgents
from tools import StockAnalyzer

# Load environment variables
load_dotenv()

# Check if the API key is set
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Initialize OpenAI LLM
llm = OpenAI(api_key=api_key, model="gpt-4o-mini", temperature=0.3)  # Changed to gpt-4

# Define the stock symbol and analysis period
symbol = "SOFI"
days = 1

# Create StockAnalysisAgents instance
stock_analysis_agents = StockAnalysisAgents(llm, symbol)

# Create agents
agents = stock_analysis_agents.create_agents()

# Create tasks
tasks = stock_analysis_agents.create_tasks(agents, days)

# Create the crew
crew = Crew(
    agents=agents,
    tasks=tasks,
    verbose=True,
    max_iterations=5  # Increase this value if needed
)

# Run the crew
result = crew.kickoff()

# Generate JSON output
stock_analyzer = StockAnalyzer(symbol, days)
stock_analyzer.generate_json_output()

print("Analysis complete. Check the JSON file for results.")
print(f"Crew result: {result}")
