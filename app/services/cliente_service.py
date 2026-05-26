from sqlalchemy.orm import Session
from app.models import Cliente, WebhookEvent
from app.schemas import ClienteCreate, WebhookPayload

PRIORITY_THRESHOLD = 200_000


def calculate_priority(valor_patrimonio: float) -> str:
    return "prioridade_alta" if valor_patrimonio >= PRIORITY_THRESHOLD else "prioridade_normal"


def create_client(db: Session, data: ClienteCreate) -> Cliente:
    if db.query(Cliente).filter(Cliente.cliente_email == data.cliente_email).first():
        raise ValueError(f"Email already registered: {data.cliente_email}")

    client = Cliente(
        cliente_nome=data.cliente_nome,
        cliente_email=data.cliente_email,
        tipo_solicitacao=data.tipo_solicitacao,
        valor_patrimonio=data.valor_patrimonio,
        status="Aguardando Análise",
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def process_webhook(db: Session, payload: WebhookPayload) -> Cliente:
    if db.query(WebhookEvent).filter(WebhookEvent.event_id == payload.event_id).first():
        raise ValueError(f"Event already processed: {payload.event_id}")

    client = db.query(Cliente).filter(Cliente.cliente_email == payload.cliente_email).first()
    if not client:
        raise LookupError(f"Client not found: {payload.cliente_email}")

    client.prioridade = calculate_priority(client.valor_patrimonio)
    client.status = "Processado"

    db.add(WebhookEvent(event_id=payload.event_id))
    db.commit()
    db.refresh(client)
    return client
