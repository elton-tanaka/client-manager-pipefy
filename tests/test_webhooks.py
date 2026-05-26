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


def _create_client(email: str, valor_patrimonio: float):
    client.post("/clientes/", json={
        "cliente_nome": "Test User",
        "cliente_email": email,
        "tipo_solicitacao": "Abertura de conta",
        "valor_patrimonio": valor_patrimonio,
    })


def test_webhook_sets_priority_alta():
    _create_client("rica@example.com", 200_000.0)
    response = client.post("/webhooks/pipefy/card-updated", json={
        "event_id": "evt_001",
        "card_id": "card_001",
        "cliente_email": "rica@example.com",
        "timestamp": "2026-05-18T12:00:00Z",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["prioridade"] == "prioridade_alta"
    assert data["status"] == "Processado"


def test_webhook_sets_priority_normal():
    _create_client("normal@example.com", 199_999.99)
    response = client.post("/webhooks/pipefy/card-updated", json={
        "event_id": "evt_002",
        "card_id": "card_002",
        "cliente_email": "normal@example.com",
        "timestamp": "2026-05-18T12:00:00Z",
    })
    assert response.status_code == 200
    assert response.json()["prioridade"] == "prioridade_normal"


def test_webhook_duplicate_event_id_blocked():
    _create_client("dup@example.com", 50_000.0)
    payload = {
        "event_id": "evt_dup",
        "card_id": "card_003",
        "cliente_email": "dup@example.com",
        "timestamp": "2026-05-18T12:00:00Z",
    }
    client.post("/webhooks/pipefy/card-updated", json=payload)
    response = client.post("/webhooks/pipefy/card-updated", json=payload)
    assert response.status_code == 409
    assert "already processed" in response.json()["detail"]


def test_webhook_client_not_found():
    response = client.post("/webhooks/pipefy/card-updated", json={
        "event_id": "evt_ghost",
        "card_id": "card_999",
        "cliente_email": "ghost@example.com",
        "timestamp": "2026-05-18T12:00:00Z",
    })
    assert response.status_code == 404
