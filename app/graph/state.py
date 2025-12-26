from typing import List, TypedDict, Optional

class InterviewState(TypedDict):
    session_id: str
    resume_text: str          # The raw text from the PDF
    candidate_profile: str    # Summarized info (Skills, Role, Experience)
    messages: List[str]       # History of Question & Answer
    current_question: str     # The question waiting for the user
    feedback_reports: List[str] # Hidden technical analysis of every answer
    question_count: int       # Tracker (0, 1, 2...)
    max_questions: int        # Limit (e.g., 5 questions)
    interview_complete: bool  # Flag to stop the loop