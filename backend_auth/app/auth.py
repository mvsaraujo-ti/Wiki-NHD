from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from sqlmodel import Session, select
from .models import User

SECRET_KEY = "nhd_super_secret_key"     # depois troque por algo seguro
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -----------------------------
# HASH e verificação de senha
# -----------------------------
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hash_db: str):
    return pwd_context.verify(password, hash_db)


# -----------------------------
# Autenticação
# -----------------------------
def authenticate_user(session: Session, username: str, password: str):
    query = select(User).where(User.username == username)
    user = session.exec(query).first()

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


# -----------------------------
# GERAR TOKEN JWT
# -----------------------------
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
