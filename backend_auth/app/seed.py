from sqlmodel import Session, select
from .models import User
from .auth import hash_password


def seed(engine):
    with Session(engine) as session:

        if not session.exec(
            select(User).where(User.username == "Maxwell")
        ).first():
            session.add(
                User(
                    username="Maxwell",
                    password_hash=hash_password("maxwell"),
                    role="master"
                )
            )

        if not session.exec(
            select(User).where(User.username == "Michel")
        ).first():
            session.add(
                User(
                    username="Michel",
                    password_hash=hash_password("michel"),
                    role="master"
                )
            )

        session.commit()
