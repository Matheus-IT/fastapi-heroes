import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, StaticPool, Session, SQLModel
from src.main import app
from src.dependencies import get_session


test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create fresh schema before any tests run"""
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)


def get_session_override():
    """Dependency to get the test session"""
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def client():
    """Test client with test override"""
    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def db_session():
    """Begin a nested transaction (ROLLBACK after each test)"""
    with Session(test_engine) as session:
        yield session
