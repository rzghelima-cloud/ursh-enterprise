import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.api.deps import get_db
from app.main import create_app
from app.core.security import hash_password
from app.models.user import User

@pytest.fixture(scope="session")
def client():
    # SQLite for tests
    engine = create_engine("sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    app = create_app()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Seed one admin user
    db = TestingSessionLocal()
    db.add(User(username="admin", full_name="Admin", password_hash=hash_password("12345"), role="admin", member_type="admin"))
    db.commit()
    db.close()

    return TestClient(app)
