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
class DealRequest(BaseModel):
    company_name: str
    revenue: float
    pat: float
    debt: float

@app.post("/analyze-deal")
async def analyze_deal(request: DealRequest):
    # This calls your CrewAI logic using the data from the form
    result = run_s45_screening(
        company_name=request.company_name,
        revenue=request.revenue,
        pat=request.pat,
        debt=request.debt
    )
    
    return {
        "status": "success",
        "analysis_report": result
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)