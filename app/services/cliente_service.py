from sqlalchemy.orm import Session
from app.models import Cliente
from app.schemas import ClienteCreate

LIMITE_PRIORIDADE_ALTA = 200_000


def calcular_prioridade(patrimonio: float) -> str:
    return "prioridade_alta" if patrimonio >= LIMITE_PRIORIDADE_ALTA else "prioridade_normal"


def criar_cliente(db: Session, dados: ClienteCreate) -> Cliente:
    if db.query(Cliente).filter(Cliente.email == dados.email).first():
        raise ValueError(f"Email já cadastrado: {dados.email}")

    cliente = Cliente(
        nome=dados.nome,
        email=dados.email,
        patrimonio=dados.patrimonio,
        prioridade=calcular_prioridade(dados.patrimonio),
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente
