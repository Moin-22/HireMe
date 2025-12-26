from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from app.graph.state import InterviewState
from app.graph.nodes import (
    extract_profile_node,
    generate_question_node,
    analyze_answer_node,
    feedback_node
)

# 1. Initialize the Graph with our State
workflow = StateGraph(InterviewState)

# 2. Add the Nodes (The Agents)
workflow.add_node("extractor", extract_profile_node)
workflow.add_node("question_gen", generate_question_node)
workflow.add_node("analyzer", analyze_answer_node)
workflow.add_node("feedback", feedback_node)

# 3. Define the Entry Point
# When the graph starts, it hits the 'extractor' first
workflow.set_entry_point("extractor")

# 4. Connect the Edges (The Flow)
# After extracting profile -> Generate the first question
workflow.add_edge("extractor", "question_gen")

workflow.add_edge("question_gen", "analyzer")

# 5. Define the Conditional Logic (The Router)
def route_step(state):
    """
    Decides what to do after analyzing an answer:
    - If question_count >= max_questions -> Go to Feedback
    - Else -> Generate another Question
    """
    count = state["question_count"]
    max_q = state["max_questions"]
    
    if count >= max_q:
        return "feedback"
    else:
        return "question_gen"

# 6. Add the Conditional Edge
# After 'analyzer' runs, the graph asks 'route_step' where to go next
workflow.add_conditional_edges(
    "analyzer",
    route_step,
    {
        "feedback": "feedback",
        "question_gen": "question_gen"
    }
)

# 7. Finish the flow
# After feedback is generated, the workflow ends
workflow.add_edge("feedback", END)

# 8. COMPILE THE GRAPH
# We use a MemorySaver to persist state between API calls (e.g., user answering)
checkpointer = MemorySaver()

# interrupt_before=["analyzer"]: 
# This is CRITICAL. It pauses the graph right before the 'analyzer' node runs.
# This gives the FastAPI server time to insert the user's answer into the state.
app_graph = workflow.compile(
    checkpointer=checkpointer, 
    interrupt_before=["analyzer"]
)