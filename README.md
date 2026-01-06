# **Physiq AI 💪**

### Your Personal AI Fitness Assistant

Physiq AI is a full-stack AI-powered fitness coaching application built with a **modern agent-based architecture**. It combines a FastAPI backend, Google ADK agents, structured prompts, and a lightweight frontend to deliver intelligent, goal-oriented fitness guidance through natural conversation.

This project demonstrates **real-world AI system design**, including agent orchestration, tool usage, session handling, authentication, and scalable backend structure—making it ideal for a professional portfolio.

---

## 🚀 Key Features

### 🤖 Agent-Based AI Architecture

* Built using **Google ADK (Agent Development Kit)**
* Modular agents with clear responsibilities
* Structured prompt engineering for consistent AI behavior

### 🛠 Tool-Driven Intelligence

* Agents can invoke internal tools for:

  * Fitness guidance
  * Data lookup
  * Context-aware responses
* Easily extendable via `tools.py`

### 🔐 Authentication & User Management

* User signup & login
* JWT-based authentication
* Secure dependency-based access control

### 🧠 Session-Based Conversations

* Maintains AI chat sessions per user
* Uses in-memory session service for fast iteration
* Ready for persistent storage if needed

### 🗄 Database Integration

* SQLAlchemy ORM
* Clean separation of models and DB logic
* SQLite/PostgreSQL ready

### 🌐 Simple Frontend

* Lightweight HTML frontend
* Communicates with backend APIs
* Ideal for rapid testing and demos

---

## 🧱 Project Structure

```text
PHYSIQ/
│
├── backend/
│   ├── .adk/                  # Google ADK internal configs
│   ├── app/
│   │   ├── agents/             # AI agent definitions
│   │   ├── schemas/            # Pydantic request/response models
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentication logic (JWT, login/signup)
│   │   ├── db.py               # Database session management
│   │   ├── deps.py             # FastAPI dependencies
│   │   ├── init_db.py          # Database initialization & seeding
│   │   ├── knowledge_base.db   # Fitness knowledge base
│   │   ├── main.py             # FastAPI application entry
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── physiq.db           # Application database
│   │   ├── prompt.py           # System & agent prompts
│   │   ├── tools.py            # AI tools callable by agents
│   │   ├── run.py              # Uvicorn runner
│   │   ├── test.py             # Testing utilities
│   │   └── xtdb.py             # Experimental / extended DB logic
│   │
│   └── __pycache__/
│
├── data/                       # Static or seed data
│
├── frontend/
│   └── index.html              # Frontend UI
│
├── venv/                       # Python virtual environment
├── .env                        # Environment variables
└── README.md
```

---

## 🧑‍💻 Tech Stack

**Backend**

* Python
* FastAPI
* SQLAlchemy
* Google ADK
* JWT Authentication

**AI**

* Google Gemini (via ADK)
* Agent + Tool-based execution
* Structured prompt control

**Frontend**

* HTML
* CSS
* JavaScript

**Database**

* SQLite (default)
* PostgreSQL-ready

---

## ⚙️ Getting Started

### 1️⃣ Clone the Repository

```bash
git clone (https://github.com/jalal1808/PHYSIQ.git)
cd physiq
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_api_key_here
```

---

## ▶️ Running the Application

### Start the Backend

```bash
python backend/app/run.py
```

The API will be available at:

```
http://localhost:8000
```

### Open the Frontend

Open in browser:

```
https://http://127.0.0.1:8000/
```

---

## 🔌 API Usage Example (Postman)

**Endpoint**

```http
POST /chat
```

**Body**

```json
{
  "message": "Create a beginner workout plan for fat loss"
}
```

---


## 🛑 Stopping the Server

Simply stop the terminal or press:

```bash
CTRL + C
```


Just say the word 🚀
