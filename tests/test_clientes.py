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


def test_criar_cliente_valido():
    response = client.post("/clientes/", json={
        "nome": "João Silva",
        "email": "joao@example.com",
        "patrimonio": 150_000.0,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "joao@example.com"
    assert data["prioridade"] == "prioridade_normal"
    assert "id" in data
    assert "criado_em" in data


def test_prioridade_alta_no_limite():
    response = client.post("/clientes/", json={
        "nome": "Maria Souza",
        "email": "maria@example.com",
        "patrimonio": 200_000.0,
    })
    assert response.status_code == 201
    assert response.json()["prioridade"] == "prioridade_alta"


def test_prioridade_normal_abaixo_limite():
    response = client.post("/clientes/", json={
        "nome": "Carlos Lima",
        "email": "carlos@example.com",
        "patrimonio": 199_999.99,
    })
    assert response.status_code == 201
    assert response.json()["prioridade"] == "prioridade_normal"


def test_email_invalido_retorna_422():
    response = client.post("/clientes/", json={
        "nome": "Teste",
        "email": "not-an-email",
        "patrimonio": 50_000.0,
    })
    assert response.status_code == 422


def test_email_duplicado_retorna_409():
    payload = {"nome": "Dup", "email": "dup@example.com", "patrimonio": 50_000.0}
    client.post("/clientes/", json=payload)
    response = client.post("/clientes/", json=payload)
    assert response.status_code == 409
    assert "Email já cadastrado" in response.json()["detail"]
