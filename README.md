# HireME

AI-powered mock interview platform that conducts realistic, context-aware technical interviews based on a candidate's resume. Built with FastAPI, LangGraph, and Streamlit to deliver interactive interviews, real-time feedback, and adaptive question flows.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue)](#)

## Table of contents
- [Features](#features)
- [Tech stack](#tech-stack)
- [Quick start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Roadmap / TODO](#roadmap--todo)

## Features
- Resume parsing: Extract skills, experience, and projects from PDF resumes.
- Context-aware questions: Interview questions generated from the candidate's actual projects and skills.
- Adaptive flow: Interview follows Introduction → Project Deep Dive → Technical Skills → Behavioral questions.
- Real-time feedback: Summarizes strengths and weaknesses and provides suggestions at the end.
- Configurable LLM backend: Integrates LLM(s) via LangGraph for question generation and evaluation.

## Tech stack
- Backend: FastAPI (Python)
- Frontend: Streamlit
- LLM / Orchestration: Llama 3 (via Groq), LangChain, LangGraph
- Utilities: PyPDF (resume parsing), python-dotenv
- Dev tools: uvicorn for running FastAPI

## Quick start (local)
Prerequisites: Python 3.10+, pip, and a valid LLM / API credentials if required.

1. Clone the repo
   git clone https://github.com/Moin-22/HireMe.git
2. Create and activate a virtual environment
   python -m venv .venv
   source .venv/bin/activate  # macOS / Linux
   .venv\Scripts\activate     # Windows
3. Install dependencies
   pip install -r requirements.txt
4. Copy the example env and add your keys
   cp .env.example .env
   # Then edit .env with your LLM / API keys
5. Run the backend
   uvicorn app.main:app --reload
6. Run the frontend
   streamlit run frontend.py

## Configuration
Store secrets and configuration in `.env`. Example variables:
- LLM_API_KEY=your_key_here
- LLM_PROVIDER=groq|openai|local
- PORT=8000

(If your repo already contains `.env.example`, list exact variables there. Do not commit real keys.)

## Usage
- Upload resume (PDF) through the Streamlit frontend.
- The backend parses resume contents and extracts skills/projects.
- LangGraph / LLM generates targeted interview questions and scores answers.
- At the end, the user receives a feedback report covering strengths, weaknesses, and suggested improvements.

## API (example)
- POST /api/parse_resume — Accepts resume file, returns parsed profile
- POST /api/start_interview — Starts an interview session for a parsed profile
- POST /api/answer — Submit an answer for evaluation
- GET /api/session/{id}/report — Retrieve final feedback report

(Adjust endpoints to match your implementation in `app/`.)

## Project structure
- app/             — FastAPI backend
- frontend.py      — Streamlit frontend
- requirements.txt — Python dependencies
- README.md        — This file
- docs/            — Optional: screenshots, design notes, demo assets

## Development notes
- Keep model API calls and expensive processing off the request thread (use background tasks or a worker).
- Cache parsed resume results to avoid re-parsing the same file.
- Add authentication if you intend to deploy for multiple users.

## Testing
- Add unit tests for resume parsing and question-generation logic.
- Consider integration tests that mock LLM responses.

## Contributing
Contributions welcome! Suggested workflow:
1. Fork the repo
2. Create a topic branch: git checkout -b feat/your-feature
3. Make changes and add tests
4. Open a pull request describing your changes

Please follow a consistent commit message style and include tests for new logic.

## Roadmap / TODO
- Add CI (GitHub Actions) to run tests and linting
- Improve resume parsing accuracy and robust PDF handling
- Add user accounts and session persistence
- Add downloadable interview report (PDF)

## License
This project is released under the MIT License. See LICENSE for details.

## Contact
Created by Moin-22 — open an issue or PR for feedback, features, or bugs.

---
I updated README.md to change the title to "hireME" and remove the Demo section. Please confirm the update.
