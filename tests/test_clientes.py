import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_client_valid():
    response = client.post("/clientes/", json={
        "cliente_nome": "João Silva",
        "cliente_email": "joao@example.com",
        "tipo_solicitacao": "Atualização cadastral",
        "valor_patrimonio": 150_000.0,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["cliente_email"] == "joao@example.com"
    assert data["status"] == "Aguardando Análise"
    assert data["prioridade"] is None
    assert "id" in data
    assert "created_at" in data


def test_create_client_invalid_email():
    response = client.post("/clientes/", json={
        "cliente_nome": "Test",
        "cliente_email": "not-an-email",
        "tipo_solicitacao": "Abertura de conta",
        "valor_patrimonio": 50_000.0,
    })
    assert response.status_code == 422


def test_create_client_duplicate_email():
    payload = {
        "cliente_nome": "Dup",
        "cliente_email": "dup@example.com",
        "tipo_solicitacao": "Abertura de conta",
        "valor_patrimonio": 50_000.0,
    }
    client.post("/clientes/", json=payload)
    response = client.post("/clientes/", json=payload)
    assert response.status_code == 409
