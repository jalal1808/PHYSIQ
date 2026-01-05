import os
import logging
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from .agents.agent import root_agent
from .schemas.chat import (
    ChatRequest,
    ChatResponse,
    SignupRequest,
    LoginRequest,
    UpdateProfileRequest
)
from .db import SessionLocal
from .models import User, ChatSession
from .auth import hash_password, verify_password, create_token
from .deps import current_user, get_db, oauth2

logging.getLogger("google.adk").setLevel(logging.ERROR)

app = FastAPI(title="Physiq AI")

# ------------------ ADK SETUP ------------------

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name="PhysiqApp",
    session_service=session_service,
)

# ------------------ AUTH ------------------

@app.post("/auth/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email already exists")

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        weight_kg=data.weight_kg,
        height_cm=data.height_cm,
        age=data.age,
        gender=data.gender,
    )
    db.add(user)
    db.commit()

    return {"message": "User created successfully"}


@app.post("/auth/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    return {
        "access_token": create_token(user.id),
        "token_type": "bearer",
    }


@app.post("/auth/logout")
def logout(
    token: str = Depends(oauth2),
    db: Session = Depends(get_db)
):
    from .models import TokenBlacklist

    if not db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first():
        db.add(TokenBlacklist(token=token))
        db.commit()

    return {"message": "Logged out successfully"}


# ------------------ CHAT HELPERS ------------------

def build_profile_context(user: User) -> str:
    return (
        "User profile (for internal context only):\n"
        f"- Weight: {user.weight_kg or 'N/A'} kg\n"
        f"- Height: {user.height_cm or 'N/A'} cm\n"
        f"- Age: {user.age or 'N/A'}\n"
        f"- Gender: {user.gender or 'N/A'}"
    )


def lightweight_summary(user_msg: str) -> str:
    return f"User last asked about: {user_msg[:120]}"


# ------------------ CHAT ------------------

@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    # --------- DB session record ---------

    chat_session = (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user.id)
        .first()
    )

    # --------- ADK session handling ---------

    session = None

    if chat_session:
        session = await session_service.get_session(
            app_name="PhysiqApp",
            user_id=str(user.id),
            session_id=chat_session.adk_session_id,
        )

    # 🔥 FIX: recreate session if missing
    if not chat_session or session is None:
        session = await session_service.create_session(
            app_name="PhysiqApp",
            user_id=str(user.id),
        )

        if not chat_session:
            chat_session = ChatSession(
                user_id=user.id,
                adk_session_id=session.id,
            )
            db.add(chat_session)
        else:
            chat_session.adk_session_id = session.id

        db.commit()
        db.refresh(chat_session)

        # Inject profile ONCE
        profile_message = genai_types.Content(
            role="system",
            parts=[genai_types.Part(text=build_profile_context(user))],
        )

        async for _ in runner.run_async(
            user_id=str(user.id),
            session_id=session.id,
            new_message=profile_message,
        ):
            pass

    # --------- user message ---------

    user_message = genai_types.Content(
        role="user",
        parts=[genai_types.Part(text=request.message)],
    )

    final_response = ""

    async for event in runner.run_async(
        user_id=str(user.id),
        session_id=session.id,
        new_message=user_message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text
            break

    if not final_response:
        raise HTTPException(500, "No response generated")

    # --------- lightweight memory ---------

    chat_session.conversation_summary = lightweight_summary(request.message)
    db.commit()

    return ChatResponse(
        response=final_response,
        session_id=session.id,
    )


# ------------------ PROFILE UPDATE ------------------

@app.patch("/user/profile")
def update_profile(
    data: UpdateProfileRequest,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    if data.weight_kg is not None:
        user.weight_kg = data.weight_kg
    if data.height_cm is not None:
        user.height_cm = data.height_cm
    if data.age is not None:
        user.age = data.age
    if data.gender is not None:
        user.gender = data.gender

    db.commit()
    db.refresh(user)

    return {
        "message": "Profile updated",
        "profile": {
            "weight_kg": user.weight_kg,
            "height_cm": user.height_cm,
            "age": user.age,
            "gender": user.gender,
        },
    }
