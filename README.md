#  Multi-Agent Travel Assistant

##  Project Overview
This project is a Multi-Agent Travel Assistant that automatically plans trips based on user input.

It uses multiple AI agents to:
- Understand the user request
- Ask for missing details
- Generate travel plans
- Combine results into one final response

---

## Features
- Extracts travel details from user input
- Asks clarification if data is missing
- Generates:
  - Flight details (mock)
  - Hotel booking (mock)
  - Travel itinerary
-  Uses vector database for smarter recommendations
- Clean UI using Streamlit

---

## Tech Stack
- FastAPI → Backend API
- Streamlit → Frontend UI
- LangGraph → Multi-agent workflow
- LangChain → Prompt + chaining
- FAISS → Vector database
- Ollama → Local LLM (LLaMA)

---

## Project Structure
travel_assistant_project/ │ ├── app/ │   ├── main.py            # FastAPI backend │   ├── graph.py           # Agent workflow (LangGraph) │   ├── state.py           # State structure │   ├── config.py          # Model configuration │   └── knowledge.py       # Vector DB setup │ ├── ui/ │   └── streamlit_app.py   # Frontend UI │ ├── requirements.txt ├── README.md └── .gitignore

---

##  Setup Instructions

### 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/multi-agent-travel-assistant.git cd multi-agent-travel-assistant

---

### 2. Create virtual environment
python -m venv venv

Activate:

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

---

### 3. Install dependencies
pip install -r requirements.txt

---

### 4. Setup Ollama (IMPORTANT)
Download and install:
 https://ollama.com/download

Run model:
ollama run llama3

---

### 5. Run Backend (FastAPI)
uvicorn app.main:app --reload

Runs at: http://127.0.0.1:8000

---

### 6. Run Frontend (Streamlit)
streamlit run ui/streamlit_app.py

Opens at: http://localhost:8501

---

##  Example Input
My name is Swetha. Plan a 3-day trip to New York from April 10 to April 13 with a budget of 1000 USD.

---

##  Workflow
1. User enters travel request
2. Interaction agent extracts data
3. Router checks missing fields
4. Clarification agent asks questions (if needed)
5. Flight agent generates mock booking
6. Hotel agent generates mock booking
7. Itinerary agent uses vector search
8. Final agent combines all results

---

##  Agents Used
- Interaction Agent
- Clarification Agent
- Flight Agent
- Hotel Agent
- Itinerary Agent
- Final Response Agent

---

##  Limitations
- Flight & hotel are mock (not real booking)
- Requires Ollama running locally
- Basic UI

---

##  Future Improvements
- Real flight APIs (Amadeus, Skyscanner)
- Real hotel APIs (Booking.com)
- Authentication (user login)
- Payment integration
- Better UI design

---



##  If you like this project
Give it a star on GitHub