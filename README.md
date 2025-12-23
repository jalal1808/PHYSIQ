# 🧠 PhySiq (Google ADK)

This repository contains a **multi-agent AI system built using Google Agent Development Kit (ADK)**.  
The system is designed to provide **health and wellness assistance strictly from structured data stored in a SQLite database**, accessed via **MCP servers**.

🚫 **Agents are explicitly restricted from using the LLM’s own pretrained knowledge**.  
✅ **All responses are generated only from database-backed knowledge sources**.

---

## 🚀 Project Overview

This project demonstrates a **controlled, data-grounded multi-agent architecture** where multiple specialized agents collaborate to answer user queries using **only verified, locally stored data**.

The LLM acts purely as a **reasoning and orchestration layer**, not a knowledge source.

---

## 🔐 Knowledge Access Policy (Strict)

- All agents retrieve information **exclusively from a SQLite database**
- Data is accessed through **MCP (Model Context Protocol) servers**
- **No agent is allowed to answer from its own pretrained or external knowledge**
- If relevant data is not found in the database, the agent must:
  - Ask for clarification, or
  - Explicitly state that the information is unavailable

This ensures:
- Deterministic and auditable responses
- Reduced hallucinations
- Full control over knowledge sources

---

## 🤖 Agents Included

### 🩺 Medical Assistant Agent
- Analyzes user-reported symptoms using medical datasets
- Suggests possible conditions (non-diagnostic)
- Recommends appropriate medical specialists
- Uses **only medical records stored in SQLite**

### 🥗 Nutritionist Agent
- Generates diet plans from nutrition datasets
- Suggests meals based on stored food and dietary data
- Adjusts recommendations using medical constraints from the database

### 🏋️ Fitness Trainer Agent
- Recommends workouts using exercise and equipment datasets
- Builds routines based on stored fitness plans and levels
- Avoids unsafe recommendations using medical data constraints

### 😴 Sleep Agent
- Provides sleep optimization guidance from sleep datasets
- Analyzes sleep routines and recovery metrics
- Uses structured sleep rules and patterns stored in the database


## 🧩 System Architecture

- **Google ADK** for agent orchestration
- **SQLite** as the single source of truth
- **MCP Servers** for controlled data access
- **Multi-agent coordination** with shared context
- **LLM restricted to reasoning, routing, and formatting only**

---

## 🛠 Tech Stack

- **Python**
- **Google Agent Development Kit (ADK)**
- **SQLite**
- **MCP (Model Context Protocol)**
- **LiteLLM / LLM Provider**
- **dotenv** for environment variables

---

## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone (https://github.com/jalal1808/PHYSIQ.git)
   cd physiq_agent

Create and activate virtual environment

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate


Install dependencies

pip install -r requirements.txt


⚠️ Disclaimer

This system is data-driven and non-diagnostic.
It does not replace professional medical advice and relies entirely on the accuracy of stored datasets.

🌱 Future Enhancements

Role-based access control for datasets

Dataset versioning and auditing

User profiles stored in SQLite

Expanded medical and fitness datasets

UI dashboard for database management
