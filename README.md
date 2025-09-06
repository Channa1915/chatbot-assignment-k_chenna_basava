■ STAN Chatbot
A personality-driven chatbot with long-term memory, context awareness, and tone adaptation, built
using FastAPI (backend) and a simple HTML/JS frontend.
■ Features
■ Long-term memory recall (remembers user name, preferences, favorite color, etc.)
■ Context-aware tone adaptation (supportive, playful, formal responses based on input)
■ Personalization over time — tailors responses based on past interactions
■ Identity consistency (always stays as Stan Pal)
■ Hallucination resistance (avoids making up false details)
■ Frontend with stylish chat UI (works in browser)
■ SQLite-based memory persistence
■■ Project Structure
stan-chatbot/
■■ backend/ # FastAPI backend
■ ■■ main.py # Main API with chat endpoint
■ ■■ memory.py # SQLite-based memory store
■ ■■ llm_provider.py # Mock LLM provider
■ ■■ prompts.py # System prompts (bot persona, rules)
■ ■■ utils.py # Helper functions
■ ■■ requirements.txt # Backend dependencies
■■ frontend/
■ ■■ index.html # Chat UI (HTML, CSS, JS)
■■ .env.example # Example environment variables
■■ README.md # Project documentation
■■ ARCHITECTURE.md # Detailed architecture explanation
■■ TESTING.md # Test cases & validation
■■ VIDEO_SCRIPT.md # Suggested demo video script
■■ Installation & Setup
1■■ Clone Repository
 git clone https://github.com/your-username/stan-chatbot.git
 cd stan-chatbot
2■■ Backend Setup
 cd backend
 python -m venv venv
 .\venv\Scripts\activate # On Windows
 # source venv/bin/activate # On Mac/Linux
 pip install -r requirements.txt
3■■ Run Server
 uvicorn main:app --reload --host 127.0.0.1 --port 8000
 (API will be running at http://127.0.0.1:8000)
4■■ Frontend Setup
 Open frontend/index.html in your browser
 Start chatting with Stan ■
■ Testing
Refer to TESTING.md for test cases & expected outputs. Key scenarios tested:
• Long-term memory recall
• Context-aware tone adaptation
• Personalization over time
• Response naturalness & diversity
• Identity consistency
• Hallucination resistance
• Memory stability under repetition
■ Demo Video
A 2–5 minute demo showcasing Stan’s key features (memory, tone, identity, hallucination
resistance). Script in VIDEO_SCRIPT.md.
■■ Tech Stack
• Backend: FastAPI, SQLAlchemy, SQLite
• Frontend: HTML, CSS, Vanilla JS
• Language: Python 3.10+
• Other: dotenv, Uvicorn
■ Repository
■ GitHub Link: [https://github.com/Channa1915/chatbot-assignment-k_chenna_basava/]
■ Author
K Chenna Basava (gkchanna23@gmail.com)
