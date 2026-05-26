import logging

logger = logging.getLogger(__name__)

PIPE_ID = "simulated-pipe-001"

_CREATE_CARD_MUTATION = """
mutation CreateCard($input: CreateCardInput!) {
  createCard(input: $input) {
    card {
      id
      title
    }
  }
}
"""

_UPDATE_CARD_FIELD_MUTATION = """
mutation UpdateCardField($input: UpdateCardFieldInput!) {
  updateCardField(input: $input) {
    success
  }
}
"""


def create_card(
    cliente_nome: str,
    cliente_email: str,
    tipo_solicitacao: str,
    valor_patrimonio: float,
) -> dict:
    payload = {
        "query": _CREATE_CARD_MUTATION,
        "variables": {
            "input": {
                "pipe_id": PIPE_ID,
                "title": cliente_nome,
                "fields_attributes": [
                    {"field_id": "cliente_email", "field_value": cliente_email},
                    {"field_id": "tipo_solicitacao", "field_value": tipo_solicitacao},
                    {"field_id": "valor_patrimonio", "field_value": str(valor_patrimonio)},
                ],
            }
        },
    }
    logger.info("Pipefy createCard (simulated): %s", payload)
    return payload


def update_card_field(card_id: str, field_id: str, new_value: str) -> dict:
    payload = {
        "query": _UPDATE_CARD_FIELD_MUTATION,
        "variables": {
            "input": {
                "card_id": card_id,
                "field_id": field_id,
                "new_value": new_value,
            }
        },
    }
    logger.info("Pipefy updateCardField (simulated): %s", payload)
    return payload
