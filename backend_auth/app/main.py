from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from .auth import verify_password, create_access_token
from .database import get_engine, get_session
from .models import User

app = FastAPI()

# ---------------------------
# CORS (DEMO LOCAL)
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8500",   # Portal NHD+
        "http://127.0.0.1:8500"
    ],
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

engine = get_engine()

# ---------------------------
# LOGIN
# ---------------------------
@app.post("/auth/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.exec(
        select(User).where(User.username == form_data.username)
    ).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")

    token = create_access_token(user.username, user.role)

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }


# ---------------------------
# TESTE
# ---------------------------
@app.get("/")
def root():
    return RedirectResponse("/portal")
def health():
    return {"status": "Auth API funcionando"}
