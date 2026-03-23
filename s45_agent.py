import os
from crewai import Agent, Task, Crew, Process, LLM

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

gemini_llm = LLM(
    model="gemini/gemini-2.5-flash", 
    api_key=os.environ["GEMINI_API_KEY"],
    temperature=0.0
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

def run_s45_screening(company_name, rev_y1, rev_y2, rev_y3, pat_y1, pat_y2, pat_y3, debt, additional_info):
    """
    Takes dynamic inputs from a web form and runs the agentic workflow.
    """
    
    # Construct the raw document string using the inputs
    dynamic_document = f"""
    COMPANY: {company_name}
    
    FINANCIAL HISTORY (Last 3 Years):
    - REVENUE: Year 1: ${rev_y1}M | Year 2: ${rev_y2}M | Year 3: ${rev_y3}M
    - PROFIT (PAT): Year 1: ${pat_y1}M | Year 2: ${pat_y2}M | Year 3: ${pat_y3}M
    - CURRENT DEBT: ${debt}M
    
    NOTES: {additional_info}
    """
    # Tasks are defined inside the function so they use the new data every time
    extract_task = Task(
        description=f"Analyze this company data: {dynamic_document}. Extract the key financial numbers.",
        expected_output="A structured summary of Revenue, Profit, and Debt.",
        agent=extractor
    )

    audit_task = Task(
        description=(
            "Verify the 3-year profit trend. SEBI criteria requires positive profit "
            "in at least 3 of the last years. Calculate the Revenue CAGR."
        ),
        expected_output="A PASS/FAIL compliance audit based on the 3-year history provided.",
        agent=auditor,
        context=[extract_task]
    )
    
    rank_task = Task(
    description=(
        "Based on the audit and extraction, provide a final Investment Readiness Report. "
        "At the very end of your report, add a single line: 'CONFIDENCE_SCORE: [0-100]'. "
        "Calculate this based on: "
        "1. Data Completeness (Is there a full 3-year history?) "
        "2. Data Verifiability (Are there specific numbers vs vague phrases?) "
        "3. Calculation Consistency (Does the profit align with revenue growth?)"
        
        "Use the following STRICT FORMATTING rules: "
        "1. Use '---' to separate sections. "
        "2. STRICT FORMATTING: Do NOT use HTML tags like <br>."
        "3. Add two empty lines between every numbered point. "
        "4. Use clear, bold headers without excessive markdown symbols. "
        "5. Ensure the score is prominently at the top."
    ),
    expected_output="""
    S45 READINESS SCORE: [X]/10
    
    INVESTMENT THESIS
    [3-4 sentences on the overall opportunity]
    
    
    DETAILED ANALYSIS:
    
    1. GROWTH TRAJECTORY: [Detailed text]
    
    
    2. COMPLIANCE & AUDIT: [Detailed text]
    
    
    3. STRATEGIC POSITIONING: [Detailed text]

    CONFIDENCE_SCORE: [Percentage]%
    """,
    agent=ranker,
    context=[extract_task, audit_task]
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
