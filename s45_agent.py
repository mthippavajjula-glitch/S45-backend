import os
from crewai import Agent, Task, Crew, Process, LLM

os.environ["GEMINI_API_KEY"] = "AIzaSyANp61u3s7eLlI6iFv-LrYWuiaEe9Tglk4"

gemini_llm = LLM(
    model="gemini/gemini-2.5-flash", 
    api_key=os.environ["GEMINI_API_KEY"],
    temperature=0.7
)

# Define Agents Globally so they stay in memory
extractor = Agent(
    role='S45 Forensic Analyst',
    goal='Accurately extract financial metrics from raw company documents.',
    backstory='You specialize in converting messy PDF text into structured data. You focus on Revenue, PAT (Profit After Tax), and Debt.',
    llm=gemini_llm,
    verbose=True
)

auditor = Agent(
    role='S45 Compliance Lead',
    goal='Verify if the company meets S45’s strict IPO readiness criteria.',
    backstory='You are an expert on SEBI guidelines. You check for "3 Years Positive Profit" and "Clean Litigation History."',
    llm=gemini_llm,
    verbose=True
)

ranker = Agent(
    role='S45 Senior Investment Banker',
    goal='Rank the deal readiness from 1-10 and estimate a "Time-to-Mandate" score.',
    backstory='You look at the "Intent" and "Growth" of a company to see if they are a 10x opportunity for the S45 platform.',
    llm=gemini_llm,
    verbose=True
)

# =================================================================
# 2. THE BRIDGING FUNCTION (Called by FastAPI or Lovable)
# =================================================================

def run_s45_screening(company_name, revenue, pat, debt):
    """
    Takes dynamic inputs from a web form and runs the agentic workflow.
    """
    
    # Construct the raw document string using the inputs
    dynamic_document = f"""
    Company Name: {company_name}
    Recent Financial Performance:
    - Revenue: ${revenue}M
    - Profit (PAT): ${pat}M
    - Total Debt: ${debt}M
    Additional Info: The company has been profitable for the last few years.
    """

    # Tasks are defined inside the function so they use the new data every time
    extract_task = Task(
        description=f"Analyze this company data: {dynamic_document}. Extract the key financial numbers.",
        expected_output="A structured summary of Revenue, Profit, and Debt.",
        agent=extractor
    )

    audit_task = Task(
        description="Check the extracted numbers against S45 standards: 3 years of profit is required.",
        expected_output="A pass/fail report on IPO eligibility.",
        agent=auditor,
        context=[extract_task]
    )

    rank_task = Task(
        description="Compare this company's profile to a benchmark of a $100M revenue unicorn. Give a Rank (1-10).",
        expected_output="A final 'S45 Readiness Score' with 3 reasons for the rank.",
        agent=ranker,
        context=[audit_task]
    )

    # Initialize the Crew
    s45_crew = Crew(
    agents=[extractor, auditor, ranker],
    tasks=[extract_task, audit_task, rank_task],
    process=Process.sequential,
    verbose=True
)

    # Run the orchestration and return the string result
    result = s45_crew.kickoff()
    return str(result)

# =================================================================
# 3. STANDALONE TEST GUARD
# =================================================================
# This allows you to still run 'python s45_agent.py' to test it locally.
if __name__ == "__main__":
    print("--- STARTING LOCAL TEST RUN ---")
    final_report = run_s45_screening(
        company_name="InnovateTech M&A",
        revenue=45.0,
        pat=8.0,
        debt=2.0
    )
    print("\n\n########################")
    print("## FINAL S45 REPORT ##")
    print("########################\n")
    print(final_report)