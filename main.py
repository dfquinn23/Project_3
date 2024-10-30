from c_crew import CompanyResearchCrew
from utils.agentsealogo import display_logo
import json

def main():
    # Display the Agent Sea logo
    display_logo()
    
    # Get user input
    company_name = input("\nEnter the name of the company you want the Research Agents to research: ")
    print(f"Company name entered: {company_name}")

    # Create and run the crew
    crew = CompanyResearchCrew(company_name)
    crew.setup_crew()
    res = crew.kickoff()
    print(f"Results from crew:")
    print(res)

if __name__ == "__main__":
    main()
