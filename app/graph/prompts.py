# app/graph/prompts.py

# 1. IMPROVED EXTRACTOR: Captures Projects now
EXTRACT_PROFILE_PROMPT = """
You are an expert technical recruiter. 
Read the resume below and extract a structured summary.
Focus heavily on **Projects** and **Work Experience**.

Output format:
- Candidate Name: [Name]
- Role: [Role]
- Top Skills: [List of skills]
- Key Projects/Experience: [Summarize 1-2 specific projects or roles mentioned, e.g., "Built a Bike Theft Analysis Dashboard using React"]

Resume Text:
{resume_text}
"""

# 2. IMPROVED QUESTION GENERATOR: Forces Resume-based questions
GENERATE_QUESTION_PROMPT = """
You are a technical interviewer for the role of {role}.
Current status: Question {count}.

Candidate Profile:
{skills}

INSTRUCTIONS:
1. **If {count} is 0 (The Start):** Output EXACTLY: "Hello! To start, could you please introduce yourself and tell me a bit about your background?"
2. **If {count} > 0:**
   - Look at the "Key Projects/Experience" in the profile above.
   - Ask a specific technical question about ONE of those projects.
   - Example: "You mentioned the Bike Theft project. How did you handle the data visualization in React?"
   - If no projects are found, ask a tough technical question based on their Top Skills.
3. **CRITICAL:** Output **ONLY** the question text. Do NOT output reasoning like "Since this is question 2...".
"""

# 3. IMPROVED ANALYZER: Better grading
ANALYZE_ANSWER_PROMPT = """
You are a Senior Engineer grading an interview answer.

Question Asked: {question}
Candidate's Answer: {answer}

INSTRUCTIONS:
1. If the question was "Introduce yourself", check if they mentioned their name and relevant experience.
2. If technical, check for correctness and depth.

Output a brief 2-sentence assessment for the system's internal records.
"""

# 4. FINAL FEEDBACK
FINAL_FEEDBACK_PROMPT = """
The interview is finished.
Analysis Reports: {reports}

INSTRUCTIONS:
1. Start exactly with: "Thank you for taking the time to interview with us today."
2. Provide constructive feedback:
   - **Strengths:** What did they do well?
   - **Improvements:** What technical gaps did they have?
3. Keep it professional and encouraging.
"""