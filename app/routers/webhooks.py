from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import WebhookPayload, WebhookResponse
from app.services import cliente_service, pipefy_client

router = APIRouter(prefix="/webhooks/pipefy", tags=["webhooks"])


@router.post("/card-updated", response_model=WebhookResponse)
def card_updated(payload: WebhookPayload, db: Session = Depends(get_db)):
    try:
        client = cliente_service.process_webhook(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    pipefy_client.update_card_field(payload.card_id, "status", client.status)
    pipefy_client.update_card_field(payload.card_id, "prioridade", client.prioridade)

    return WebhookResponse(
        event_id=payload.event_id,
        cliente_email=client.cliente_email,
        status=client.status,
        prioridade=client.prioridade,
    )
