from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from app.graph.state import InterviewState
from dotenv import load_dotenv  # <--- IMPORT THIS
import os

load_dotenv()

from app.graph.prompts import (
    EXTRACT_PROFILE_PROMPT, 
    GENERATE_QUESTION_PROMPT, 
    ANALYZE_ANSWER_PROMPT, 
    FINAL_FEEDBACK_PROMPT
)

# Initialize the LLM
# NEW (Working)
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

def extract_profile_node(state: InterviewState):
    """Agent 1: Reads resume and creates a profile summary."""
    print("--- 1. EXTRACTING PROFILE ---")
    resume_text = state["resume_text"]
    
    # Format the prompt
    prompt = EXTRACT_PROFILE_PROMPT.format(resume_text=resume_text)
    response = llm.invoke([HumanMessage(content=prompt)])
    
    return {"candidate_profile": response.content}

# app/graph/nodes.py (Update ONLY this function)

# Open app/graph/nodes.py and replace ONLY the 'generate_question_node' function

# app/graph/nodes.py

def generate_question_node(state: InterviewState):
    """Agent 2: Decides what to ask next based on the interview stage."""
    
    history = state.get("messages", [])
    profile = state["candidate_profile"]
    count = state["question_count"]
    max_q = state.get("max_questions", 5)

    # 🛡️ FAILSAFE: Prevent Intro Loop
    if len(history) > 0 and count == 0:
        count = 1 

    print(f"--- 2. GENERATING QUESTION (Count: {count}) ---")
    
    # --- 🧠 STRATEGY SELECTOR ---
    # We change the prompt instructions based on the 'count'
    
    if count == 0:
        # STAGE 1: INTRODUCTION
        instruction = """
        Ask exactly: "Hello! To start, could you please introduce yourself and tell me a bit about your background?"
        """
    
    elif count < 3:
        # STAGE 2: EXPERIENCE & PROJECTS (Questions 1 & 2)
        instruction = f"""
        Topic: **Deep Dive into Experience/Projects**
        - Look at the candidate's 'Key Projects' or 'Work Experience' in the profile.
        - Ask a specific implementation question (e.g., "How did you optimize X?", "What challenges did you face building Y?").
        - Do not ask generic definitions. Ask about THEIR work.
        """
    
    elif count < max_q - 1:
        # STAGE 3: TECHNICAL KNOWLEDGE (Questions 3 & 4)
        instruction = f"""
        Topic: **Core Technical Skills (Programming Languages)**
        - Look at the 'Top Skills' in the profile (e.g., Python, Java, React, SQL).
        - Ask a conceptual or debugging question related to those languages.
        - Example: "In Python, how do you handle memory management?" or "Explain the React Virtual DOM."
        """
        
    else:
        # STAGE 4: BEHAVIORAL / SCENARIO (Final Question)
        instruction = """
        Topic: **Behavioral & Soft Skills**
        - Ask a question about teamwork, conflict resolution, or problem-solving under pressure.
        - Example: "Tell me about a time you had a disagreement with a team member. How did you resolve it?"
        """

    # --- FINAL PROMPT ASSEMBLY ---
    prompt = f"""
    You are a professional Technical Interviewer.
    Current Status: Question {count + 1} of {max_q}.
    
    Candidate Profile: {profile}
    Chat History: {history}
    
    YOUR INSTRUCTIONS FOR THIS TURN:
    {instruction}
    
    OUTPUT RULES:
    1. Keep it professional but conversational.
    2. Acknowledge the previous answer briefly if it exists.
    3. Output **ONLY** the question text.
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    return {
        "current_question": response.content, 
        "question_count": count + 1
    }
def analyze_answer_node(state: InterviewState):
    """Agent 3: Grades the answer silently."""
    print("--- 3. ANALYZING ANSWER ---")
    
    current_q = state["current_question"]
    # The last message in 'messages' is the User's answer (we will ensure this in step 3)
    user_answer = state["messages"][-1] 
    
    prompt = ANALYZE_ANSWER_PROMPT.format(question=current_q, answer=user_answer)
    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Add this report to the list of reports
    current_reports = state.get("feedback_reports", [])
    return {"feedback_reports": current_reports + [response.content]}

def feedback_node(state: InterviewState):
    """Agent 4: Compiles the final report."""
    print("--- 4. COMPILING FEEDBACK ---")
    
    reports = state["feedback_reports"]
    prompt = FINAL_FEEDBACK_PROMPT.format(reports=reports)
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    return {
        "current_question": response.content, # We use current_question field to send the final text
        "interview_complete": True
    }