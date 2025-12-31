# app/main.py
import logging
from fastapi import FastAPI, HTTPException
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from .agents.agent import root_agent
from .schemas.chat import ChatRequest, ChatResponse

logging.getLogger("google.adk").setLevel(logging.ERROR)

app = FastAPI(title="Physiq AI")

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name="PhysiqApp",
    session_service=session_service,
)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # --- Session handling (same as FitForge) ---
        if request.session_id:
            session = await session_service.get_session(
                app_name="PhysiqApp",
                user_id="api_user",
                session_id=request.session_id
            )
            if not session:
                session = await session_service.create_session(
                    app_name="PhysiqApp",
                    user_id="api_user"
                )
        else:
            session = await session_service.create_session(
                app_name="PhysiqApp",
                user_id="api_user"
            )

        # --- Wrap message correctly ---
        user_message = genai_types.Content(
            role="user",
            parts=[genai_types.Part(text=request.message)]
        )

        final_response = "[Agent did not produce a final response]"

        # --- Proper async streaming ---
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=user_message
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_response = event.content.parts[0].text
                break

        return ChatResponse(
            response=final_response,
            session_id=session.id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# import uvicorn

# uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
