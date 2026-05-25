from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    patrimonio = Column(Float, nullable=False)
    prioridade = Column(String, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)
