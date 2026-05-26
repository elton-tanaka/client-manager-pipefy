from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ClienteCreate, ClienteResponse
from app.services import cliente_service, pipefy_client

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def create_client(data: ClienteCreate, db: Session = Depends(get_db)):
    try:
        client = cliente_service.create_client(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    pipefy_client.create_card(
        cliente_nome=client.cliente_nome,
        cliente_email=client.cliente_email,
        tipo_solicitacao=client.tipo_solicitacao,
        valor_patrimonio=client.valor_patrimonio,
    )

    return client
