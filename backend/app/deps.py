from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import User
from .auth import SECRET_KEY, ALGORITHM

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def current_user(
    token: str = Depends(oauth2),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid = payload.get("user_id")
    except Exception:
        raise HTTPException(status_code=401)

    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=401)

    return user
