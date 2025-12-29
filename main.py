import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.runners import InMemoryRunner
from physiq_agent.agent import app  # your ADK App

# -----------------------------
# FastAPI setup
# -----------------------------
fastapi_app = FastAPI(title="Physiq AI")

# ADK runner (stateful in-memory)
runner = InMemoryRunner(app=app)

# -----------------------------
# Models
# -----------------------------
class ChatQuery(BaseModel):
    message: str
    session_id: str


# -----------------------------
# Start a new chat session
# -----------------------------
@fastapi_app.post("/chat/start")
async def start_chat():
    return {
        "session_id": str(uuid.uuid4())
    }


# -----------------------------
# Chat endpoint
# -----------------------------
@fastapi_app.post("/chat")
async def chat(query: ChatQuery):
    try:
        events = runner.run(
            new_message=query.message,
            user_id="anonymous_user",
            session_id=query.session_id
        )

        final_text = ""

        async for event in events:
            if hasattr(event, "text") and event.text:
                final_text += event.text

        return {
            "session_id": query.session_id,
            "reply": final_text.strip()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Local run
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
