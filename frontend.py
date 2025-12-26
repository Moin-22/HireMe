import streamlit as st
import requests

# 🔗 Connect to your FastAPI Backend
API_URL = "http://127.0.0.1:8000"

# 🛠️ Page Config
st.set_page_config(page_title="AI Interviewer", page_icon="🤖", layout="centered")

# 🧠 Session State Initialization (The "Memory" of the frontend)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "interview_complete" not in st.session_state:
    st.session_state.interview_complete = False

# 🎨 Custom CSS for a cleaner look
st.markdown("""
<style>
    .stChatMessage { padding: 1rem; border-radius: 10px; margin-bottom: 1rem; }
    div[data-testid="stChatMessageContent"] p { font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# 🟢 SIDEBAR: CONTROLS
# ------------------------------------------------------------------
with st.sidebar:
    st.header("Controls")
    if st.button("🔄 Start New Interview", type="primary"):
        # Reset everything to start fresh
        st.session_state.messages = []
        st.session_state.session_id = None
        st.session_state.interview_complete = False
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Status:** " + ("🟢 Active" if st.session_state.session_id else "⚪ Waiting for Resume"))

# ------------------------------------------------------------------
# 🔵 MAIN APP LOGIC
# ------------------------------------------------------------------
st.title("🤖 AI Technical Interviewer")

# === VIEW 1: UPLOAD RESUME (Only shown if no session exists) ===
if not st.session_state.session_id:
    st.info("👋 Welcome! Please upload your resume (PDF) to begin the interview.")
    
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf"], label_visibility="collapsed")

    if uploaded_file is not None:
        if st.button("🚀 Start Interview"):
            with st.spinner("Analyzing your resume and generating questions..."):
                try:
                    # Prepare file for API
                    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                    
                    # Call Backend
                    response = requests.post(f"{API_URL}/start-interview", files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # 1. Save Session ID
                        st.session_state.session_id = data["session_id"]
                        
                        # 2. Add AI's First Question to Chat
                        # 🛡️ FAILSAFE: Only add if history is empty (Prevents duplicate Intro)
                        if not st.session_state.messages:
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": data["message"]
                            })
                        
                        # 3. Force Reload (Crucial to hide the uploader immediately)
                        st.rerun()
                    else:
                        st.error(f"Server Error: {response.text}")
                except Exception as e:
                    st.error(f"❌ Could not connect to backend. Is it running? \n\nDetails: {e}")

# === VIEW 2: CHAT INTERFACE (Shown only after upload) ===
else:
    # 1. Display Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 2. Handle User Input
    # We only show the input box if the interview is NOT complete
    if not st.session_state.interview_complete:
        if user_input := st.chat_input("Type your answer here..."):
            
            # A. Display User Message Immediately
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            # B. Send to Backend
            with st.spinner("The interviewer is thinking..."):
                try:
                    payload = {
                        "session_id": st.session_state.session_id,
                        "answer": user_input
                    }
                    response = requests.post(f"{API_URL}/submit-answer", json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        ai_text = data["message"]
                        status = data.get("status", "in_progress")

                        # C. Display AI Response
                        st.session_state.messages.append({"role": "assistant", "content": ai_text})
                        with st.chat_message("assistant"):
                            st.markdown(ai_text)
                        
                        # D. Check if Finished
                        if status == "completed":
                            st.session_state.interview_complete = True
                            st.balloons()
                            st.rerun() # Rerun to hide the chat input box
                            
                    else:
                        st.error("Error submitting answer.")
                except Exception as e:
                    st.error(f"Connection Error: {e}")

    # 3. Final Success Message
    if st.session_state.interview_complete:
        st.success("✅ Interview Completed! See your feedback report above.")
        st.info("Click 'Start New Interview' in the sidebar to try again with a different resume.")