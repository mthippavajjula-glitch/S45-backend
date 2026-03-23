🧠 S45 Agentic Logic & Prompt Engineering

This document outlines the "Digital Personas" and the specific financial logic programmed into the S45 Digital Deal Team. Our system uses Role-Based Prompting to ensure each agent operates with the mindset of a seasoned investment banking professional.

1. The Forensic Analyst (Data Extraction)
Role: Junior Associate / Data Specialist
Logic Goal: Zero-loss data extraction from unstructured financial notes.

Core Logic:
Strict Numeric Retrieval: Programmed to ignore "fluff" and focus exclusively on Revenue, PAT, and Debt.

Timeline Mapping: Logic designed to map vague phrases (e.g., "last year," "two years back") into a standardized 3-year fiscal grid (FY1, FY2, FY3).

Pre-Processing: Ensures that currency denominations (e.g., Cr vs M) are normalized before the Auditor begins.

2. The Compliance Lead (The Auditor)
Role: Head of Regulatory Affairs
Logic Goal: Hard-stop verification against SEBI and S45 internal listing criteria.

Core Logic:
The "3-Year Rule": A binary logic gate. If the company fails to show positive profit in 3 of the last 3 years, the agent is instructed to trigger a "Critical Deficiency" flag.

Litigation Scanning: Searches "Additional Info" for red flags regarding legal or regulatory disputes.

Deterministic Auditing: Unlike a standard chatbot, this agent is set to Temperature 0.0, meaning it cannot be "convinced" to overlook a compliance failure.

3. The Senior Banker (The Ranker)
Role: Managing Director (MD), Investment Banking
Logic Goal: Strategic evaluation and Investment Thesis generation.

Core Logic:
Unicorn Benchmarking: Compares the company’s current revenue and growth against a "100M Revenue Unicorn" standard.

CAGR Calculation: Programmed to calculate Compound Annual Growth Rate from the 3-year revenue history to determine if the company is in a "Hyper-growth" phase (30-50%+).

Time-to-Mandate Estimation: Uses historical deal cycles to estimate how long the company needs "in the oven" before a successful IPO or M&A exit can be executed.

🛡️ Trust & Safety: The Confidence Engine
To prevent AI hallucinations, we implemented a Confidence Score (0-100%). This is calculated by a meta-review step where the Banker agent assesses:

Completeness: Are all 9 financial variables present?

Consistency: Does the PAT growth correlate reasonably with Revenue growth?

Verifiability: Is the input data specific or speculative?
