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


def criar_card(nome: str, email: str, patrimonio: float, prioridade: str) -> dict:
    payload = {
        "query": _CREATE_CARD_MUTATION,
        "variables": {
            "input": {
                "pipe_id": PIPE_ID,
                "fields_attributes": [
                    {"field_id": "nome", "field_value": nome},
                    {"field_id": "email", "field_value": email},
                    {"field_id": "patrimonio", "field_value": str(patrimonio)},
                    {"field_id": "prioridade", "field_value": prioridade},
                ],
            }
        },
    }
    logger.info("Pipefy createCard (simulated): %s", payload)
    return payload
