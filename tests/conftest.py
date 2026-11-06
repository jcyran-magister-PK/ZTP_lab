import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from data.database import engine, SessionLocal, get_db
from main import app

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()

    session = SessionLocal(bind=connection)
    
    session.commit = session.flush

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db_session: Session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
