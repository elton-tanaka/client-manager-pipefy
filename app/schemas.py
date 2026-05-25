from datetime import datetime
from pydantic import BaseModel, EmailStr


class ClienteCreate(BaseModel):
    nome: str
    email: EmailStr
    patrimonio: float


class ClienteResponse(BaseModel):
    id: int
    nome: str
    email: str
    patrimonio: float
    prioridade: str
    criado_em: datetime

    model_config = {"from_attributes": True}
