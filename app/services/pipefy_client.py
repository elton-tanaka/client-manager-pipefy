import logging
import os

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

PIPE_ID = "simulated-pipe-001"
_TOKEN = os.environ["PIPEFY_API_TOKEN"]


def create_card(
    cliente_nome: str,
    cliente_email: str,
    tipo_solicitacao: str,
    valor_patrimonio: float,
) -> dict:
    query = """
mutation {
  createCard(input: {
    pipe_id: "%s"
    fields_attributes: [
      {
        field_id: "cliente_nome"
        field_value: "%s"
      },
      {
        field_id: "cliente_email"
        field_value: "%s"
      },
      {
        field_id: "tipo_solicitacao"
        field_value: "%s"
      },
      {
        field_id: "valor_patrimonio"
        field_value: "%s"
      }
    ]
  }) {
    card {
      id
    }
  }
}
""" % (PIPE_ID, cliente_nome, cliente_email, tipo_solicitacao, str(valor_patrimonio))

    payload = {
        "headers": {"Authorization": f"Bearer {_TOKEN}"},
        "query": query,
    }
    logger.info("Pipefy createCard (simulated): %s", payload)
    return payload


def update_card_field(card_id: str, field_id: str, new_value: str) -> dict:
    query = """
mutation {
  updateCardField(input: {
    card_id: "%s"
    field_id: "%s"
    new_value: "%s"
  }) {
    card {
      fields {
        value
        field {
          label
          id
        }
      }
    }
    success
  }
}
""" % (card_id, field_id, new_value)

    payload = {
        "headers": {"Authorization": f"Bearer {_TOKEN}"},
        "query": query,
    }
    logger.info("Pipefy updateCardField (simulated): %s", payload)
    return payload
