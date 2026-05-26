from fastapi import FastAPI
from app.database import Base, engine
from app.routers import clientes, webhooks
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("pipefy.log"),
    ],
)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Client Manager")
app.include_router(clientes.router)
app.include_router(webhooks.router)
