🤖 STAN Chatbot – Architecture Document

This document explains the system design, architecture, and workflow of the STAN Chatbot project.

🎯 Objectives

Create a human-like chatbot that can engage naturally.

Support long-term memory (remembers user preferences).

Adapt tone and context based on user input.

Ensure identity consistency and reduce hallucinations.

Work with a modular backend (FastAPI) and browser frontend.

🏗️ High-Level Architecture
-------------------------------------------------------------
                ┌────────────────────────┐
                │        Frontend        │
                │  (index.html, JS, CSS) │
                └───────────┬────────────┘
                            │  (fetch API call)
                            ▼
                ┌────────────────────────┐
                │        Backend         │
                │       (FastAPI)        │
                └───────────┬────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
   Memory Module        LLM Provider     Persona/Prompts


   
   
 -------------------------------------------------------------

🔹 Components
1. Frontend (UI)

File: frontend/index.html

Technologies: HTML, CSS, Vanilla JS

Role: Provides a chat interface with text input and chat bubbles.

Function:

Captures user input.

Sends input to backend API (/chat).

Displays chatbot responses dynamically.

2. Backend (API Layer)

Framework: FastAPI (Python)

Entry point: backend/main.py

Responsibilities:

Expose a /chat endpoint.

Receive user messages + user ID.

Load previous conversation memory.

Build prompt with context + persona.

Call LLM Provider (e.g., Gemini API).

Save chatbot response + user message into SQLite memory.

Return the chatbot reply to the frontend.

3. Memory Module

File: backend/memory.py

Database: SQLite

Purpose: Store user interactions for long-term memory.

Structure:

userId (string)

role (user/assistant)

content (message text)

timestamp

Behavior:

On every chat, load the last 10–15 messages for context.

Recall user preferences (e.g., name, favorite color).

Maintain identity consistency across sessions.

4. LLM Provider

File: backend/llm_provider.py

Handles requests to Gemini API (gemini-2.5-flash) or other LLMs.

Wraps the API so it can be swapped easily with OpenAI, Claude, or local models (Mistral, Llama2).

Ensures cost efficiency by trimming context length.

5. Persona & Prompts

File: backend/prompts.py

Defines chatbot identity:

Name: Stan Pal

Role: Friendly, empathetic assistant.

Rules:

Stay consistent in personality.

Avoid hallucination (don’t make up details).

Adapt tone based on user input (supportive if sad, playful if casual).

🔹 Data Flow

User types a message in frontend UI.

JS fetch() sends the message to /chat API with userId.

Backend checks SQLite memory for past conversation.

Backend builds a prompt with persona + context.

LLM Provider sends the prompt to Gemini API.

Gemini API returns response → backend saves it to memory.

Response sent back to frontend, displayed in chat UI.

📦 Scalability Considerations

Stateless backend → conversation memory stored in DB, not RAM.

Can swap SQLite with Postgres, MongoDB, or Redis for production.

Supports multiple users (each has separate userId).

Modular design → can integrate with UGC platforms (social media, forums, etc.).

🛡️ Hallucination Resistance

Bot is instructed to say:

“I don’t remember that clearly” instead of inventing details.

Give vague but natural answers if asked impossible things.

📖 Example Scenario

User: “My name is Channa”

Bot saves: {userId:1, key:name, value:"Channa"}

Later…

User: “What’s my name?”

Bot recalls from memory → “You told me earlier your name is Channa 😊”

⚙️ Tech Stack

Backend: FastAPI, Uvicorn, SQLite, SQLAlchemy

Frontend: HTML, CSS, JavaScript

LLM: Gemini API (gemini-2.5-flash)

Language: Python 3.10+





