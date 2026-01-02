import logging
from fastapi import FastAPI, HTTPException, Depends
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from .agents.agent import root_agent
from .schemas.chat import ChatRequest, ChatResponse, SignupRequest, LoginRequest

from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import User, ChatSession
from .auth import hash_password, verify_password, create_token
from .deps import current_user, get_db

from fastapi.security import OAuth2PasswordRequestForm # Add this import

logging.getLogger("google.adk").setLevel(logging.ERROR)

app = FastAPI(title="Physiq AI")

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name="PhysiqApp",
    session_service=session_service,
)

@app.post("/auth/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email exists")

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password)
    )
    db.add(user)
    db.commit()

    return {"message": "User created"}

@app.post("/auth/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(401)

    token = create_token(user.id)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user: User = Depends(current_user),
    db: Session = Depends(get_db)
):
    # Get or create chat session
    chat_session = (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user.id)
        .first()
    )

    if chat_session:
        session = await session_service.get_session(
            app_name="PhysiqApp",
            user_id=str(user.id),
            session_id=chat_session.adk_session_id
        )

        if session is None:
            session = await session_service.create_session(
                app_name="PhysiqApp",
                user_id=str(user.id)
            )
            chat_session.adk_session_id = session.id
            db.commit()
    else:
        session = await session_service.create_session(
            app_name="PhysiqApp",
            user_id=str(user.id)
        )
        chat_session = ChatSession(
            user_id=user.id,
            adk_session_id=session.id
        )
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)

    # Build context CONDITIONALLY
    base_context = f"""
User Profile:
Weight: {user.weight_kg or 'N/A'}
Height: {user.height_cm or 'N/A'}
Age: {user.age or 'N/A'}
Gender: {user.gender or 'N/A'}
""".strip()

    if chat_session.conversation_summary:
        memory_context = f"""
{base_context}

Conversation Memory:
{chat_session.conversation_summary}
""".strip()
    else:
        memory_context = base_context

    # Send user message
    user_message = genai_types.Content(
        role="user",
        parts=[genai_types.Part(
            text=memory_context + "\n\nUser says: " + request.message
        )]
    )

    final_response = ""

    async for event in runner.run_async(
        user_id=str(user.id),
        session_id=session.id,
        new_message=user_message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text
            break

    # Update conversation summary ONLY after response
    summary_prompt = f"""
Summarize the following conversation briefly so it can be used as memory later.

User: {request.message}
Assistant: {final_response}
"""

    summary_message = genai_types.Content(
        role="user",
        parts=[genai_types.Part(text=summary_prompt)]
    )

    summary_text = ""

    async for event in runner.run_async(
        user_id=str(user.id),
        session_id=session.id,
        new_message=summary_message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            summary_text = event.content.parts[0].text
            break

    if summary_text:
        chat_session.conversation_summary = summary_text
        db.commit()

    return ChatResponse(
        response=final_response,
        session_id=session.id
    )

# import uvicorn

# uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
