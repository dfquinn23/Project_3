from c_crew import CompanyResearchCrew

# input = input("enter the name of the company you want the Research Agents to research: ")

crew = CompanyResearchCrew("apple")
crew.setup_crew()
res = crew.kickoff()
print(res)