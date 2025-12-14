from sqlmodel import Session, create_engine

DATABASE_URL = "sqlite:///nhd_auth.db"

engine = create_engine(DATABASE_URL, echo=False)


def get_engine():
    return engine


def get_session():
    with Session(engine) as session:
        yield session
