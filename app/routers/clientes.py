from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ClienteCreate, ClienteResponse
from app.services import cliente_service, pipefy_client

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def criar_cliente(dados: ClienteCreate, db: Session = Depends(get_db)):
    try:
        cliente = cliente_service.criar_cliente(db, dados)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    pipefy_client.criar_card(
        nome=cliente.nome,
        email=cliente.email,
        patrimonio=cliente.patrimonio,
        prioridade=cliente.prioridade,
    )

    return cliente
