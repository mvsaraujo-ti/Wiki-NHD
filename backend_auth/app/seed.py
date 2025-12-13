from sqlmodel import Session
from .models import User
from .auth import hash_password

def seed(engine):
    with Session(engine) as session:

        # Usuário Maxwell
        if not session.exec(
            session.query(User).filter(User.username == "Maxwell")
        ).first():
            session.add(User(
                username="Maxwell",
                password_hash=hash_password("maxwell"),
                role="master"
            ))

        # Usuário Michel
        if not session.exec(
            session.query(User).filter(User.username == "Michel")
        ).first():
            session.add(User(
                username="Michel",
                password_hash=hash_password("michel"),
                role="master"
            ))

        session.commit()
