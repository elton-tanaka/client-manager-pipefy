from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class ClienteCreate(BaseModel):
    cliente_nome: str
    cliente_email: EmailStr
    tipo_solicitacao: str
    valor_patrimonio: float


class ClienteResponse(BaseModel):
    id: int
    cliente_nome: str
    cliente_email: str
    tipo_solicitacao: str
    valor_patrimonio: float
    status: str
    prioridade: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class WebhookPayload(BaseModel):
    event_id: str
    card_id: str
    cliente_email: EmailStr
    timestamp: datetime


class WebhookResponse(BaseModel):
    event_id: str
    cliente_email: str
    status: str
    prioridade: str
