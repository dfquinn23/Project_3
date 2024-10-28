from c_crew import CompanyResearchCrew

company_name = input("Enter the name of the company you want the Research Agents to research: ")

crew = CompanyResearchCrew(company_name)
crew.setup_crew()
res = crew.kickoff()
print(res)
