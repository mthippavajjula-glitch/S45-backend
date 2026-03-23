🚀 S45 Agentic AI: Deal Screening Portal
The S45 Deal Screening Portal is an enterprise-grade, AI-native platform designed to automate the initial due diligence and IPO readiness assessment for high-growth companies. By leveraging a multi-agent orchestration framework, the system simulates a full investment banking deal team in seconds.

🏛️ The Architecture
This solution follows a modern "Agentic Stack" architecture:

The Face (UI): A high-fidelity dashboard built on Lovable, providing bankers with seamless data intake and visual reporting.

The Bridge (API): A FastAPI backend hosted on Render, handling secure data transmission and PDF generation.

The Brain (AI): A CrewAI multi-agent system powered by Google Gemini 2.5 Flash, performing forensic analysis, compliance auditing, and deal ranking.

🤖 The Digital Deal Team
Our "Crew" consists of three specialized agents:

S45 Forensic Analyst: Extracts and cleans raw financial data, identifying trends across a 3-year historical window.

S45 Compliance Lead: Verifies the company against strict SEBI listing criteria (e.g., the 3-year positive profit rule).

S45 Senior Banker: Ranks the deal on a scale of 1-10 based on "10x Opportunity" benchmarks and provides a high-level Investment Thesis.

✨ Key Features

3-Year Financial Audit: Analyzes Revenue, PAT, and Debt across three fiscal years to ensure data consistency.

AI Confidence Scoring: A proprietary metric (0-100%) reflecting the AI's certainty based on data completeness and verifiability.

Automated Deal Memos: One-click PDF generation of branded, professional investment memorandums.

Secure Infrastructure: Zero-leak API key management using environment variables and stateless deployment.

🛠️ Technical Implementation & Challenges
During development, several "real-world" engineering hurdles were overcome:

SQLite Version Bridge: Resolved Render's Linux environment constraints by implementing a pysqlite3 monkey-patch to support modern vector-based operations.

Deterministic Logic: Fine-tuned LLM temperatures to 0.0 to ensure consistent, audit-grade financial scoring.

Security Hardening: Pivoted from hardcoded keys to a secure Environment Variable pattern after identifying potential leak risks.

🚀 Getting Started

Prerequisites: 
Python 3.10+
Google Gemini API Key

Installation

Clone the repo:
git clone https://github.com/your-username/s45-backend.git
cd s45-backend

Install dependencies:
pip install -r requirements.txt

Set Environment Variables:
Create a .env file or export to your shell:
export GEMINI_API_KEY='your_api_key_here'

Run Locally:
python -m uvicorn main:app --reload

📈 Deployment
The backend is optimized for deployment on Render. Ensure the "Start Command" is set to:
python -m uvicorn main:app --host 0.0.0.0 --port $PORT
