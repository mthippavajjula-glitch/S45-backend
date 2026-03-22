__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# Import your actual agent logic (assuming it's in s45_agent.py)
# We will wrap the execution logic in a function
from s45_agent import run_s45_screening 

app = FastAPI()

# CRITICAL: This allows your Lovable frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, you'd put your Lovable URL here
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define what the input data should look like
# --- At the top of main.py ---
class DealRequest(BaseModel):
    company_name: str
    # Replace single year inputs with 3-year history
    revenue_y1: float  # Current Year
    revenue_y2: float  # Previous Year
    revenue_y3: float  # 2 Years Ago
    profit_y1: float
    profit_y2: float
    profit_y3: float
    debt: float
    additional_info: str = ""

@app.post("/analyze-deal")
async def analyze_deal(request: DealRequest):
    print(f"🚀 Received 3-year data for: {request.company_name}")
    
    # Pass all new variables to the agent runner
    result = run_s45_screening(
        company_name=request.company_name,
        rev_y1=request.revenue_y1, rev_y2=request.revenue_y2, rev_y3=request.revenue_y3,
        pat_y1=request.profit_y1, pat_y2=request.profit_y2, pat_y3=request.profit_y3,
        debt=request.debt,
        additional_info=request.additional_info
    )
    return {"status": "success", "analysis_report": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
