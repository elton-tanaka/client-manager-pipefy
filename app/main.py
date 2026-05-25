from fastapi import FastAPI
from app.database import Base, engine
from app.routers import clientes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Client Manager")
app.include_router(clientes.router)
