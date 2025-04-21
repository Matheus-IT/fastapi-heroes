import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.pool import StaticPool

from src.main import app
from src.dependencies import get_session


# In‑memory DB that persists for the whole pytest run
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)


# Provide *one* Session for each test function
@pytest.fixture()
def db_session():
    session = Session(test_engine)
    yield session
    session.close()


@pytest.fixture()
def client(db_session):
    def _override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = _override_get_session
    with TestClient(app) as tc:
        yield tc
    app.dependency_overrides.clear()
