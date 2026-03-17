# **Physiq AI 💪**

### Your Modern AI-Powered Wellness Coach

Physiq AI is a premium, full-stack fitness coaching application. It leverages a **multi-agent AI architecture** powered by the Google ADK, a high-performance FastAPI backend, and a stunning, minimalist **React frontend** inspired by Gemini AI.

This platform provides intelligent, context-aware guidance on nutrition, fitness, sleep, and medical inquiries through a centralized coordinator agent that routes your needs to the right specialist.

---

## ✨ Key Features

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
├── backend/                # FastAPI Core
│   └── app/
│       ├── agents/         # Google ADK Specialist Agents
│       ├── models.py       # User & Session Database Models
│       ├── tools.py        # Local Knowledge Base & AI Tools
│       └── main.py         # Primary API Endpoints
├── frontend-react/         # Modern React + Vite UI (The "Gemini" Experience)
│   ├── src/
│   │   ├── components/     # UI Components (Auth, Chat, Sidebar)
│   │   └── App.jsx         # Core Application Logic
│   └── tailwind.config.js  # Custom Design Tokens
├── data/                   # Seed data for exercises & specialists
├── physiq.db               # Persisted Application Data (Auto-generated)
└── .env                    # Centralized Secrets (Git ignored)
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
git clone https://github.com/jalal1808/PHYSIQ.git
cd PHYSIQ
```

### 2️⃣ Backend Setup
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Seed the database
python backend/app/init_db.py
```

### 3️⃣ Frontend Setup
```bash
cd frontend-react
npm install
```

### 4️⃣ Configure Environment Variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY="your_api_key_here"
SECRET_KEY="generate_a_random_string"
ALGORITHM="HS256"
```

---

## 🐳 Run with Docker (Recommended)

The easiest way to get Physiq AI up and running is using Docker Compose. This will build and launch both the backend and frontend in isolated containers.

### 1️⃣ Ensure Docker is installed
### 2️⃣ Start the platform
```bash
docker-compose up --build
```
- **Frontend**: `http://localhost:5173`
- **Backend API**: `http://localhost:8000`

---

## ▶️ Running the Platform (Manual)

### Start the Backend
From the root directory:
```bash
python backend/run.py
```
*API will be live at `http://localhost:8000`*

### Start the Frontend
In a separate terminal:
```bash
cd frontend-react
npm run dev
```
*UI will be live at `http://localhost:5173` (or check console for port)*

---

## 🔌 API Quick Look
**Chat Endpoint**: `POST /chat`  
**Auth**: `POST /auth/login` | `POST /auth/signup`

Just say the word 🚀
