# Client Manager — Pipefy Integration

Backend technical test: client management API with simulated Pipefy GraphQL integration.

## Setup

```bash
cp .env.example .env   # then set PIPEFY_API_TOKEN to your bearer token (any value works for local simulation)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Running tests

```bash
pytest -v
# Single file
pytest tests/test_webhooks.py -v
```

## Endpoints

### POST /clientes

Creates a client and simulates a Pipefy `createCard` mutation.

```bash
curl -X POST http://localhost:8000/clientes/ \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_nome": "João Silva",
    "cliente_email": "joao.silva@example.com",
    "tipo_solicitacao": "Atualização cadastral",
    "valor_patrimonio": 250000
  }'
```

**Response (201):**
```json
{
  "id": 1,
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualização cadastral",
  "valor_patrimonio": 250000.0,
  "status": "Aguardando Análise",
  "prioridade": null,
  "created_at": "2026-05-18T12:00:00"
}
```

---

### POST /webhooks/pipefy/card-updated

Simulates a Pipefy webhook. Applies the priority rule and updates the client status. Idempotent by `event_id`.

```bash
curl -X POST http://localhost:8000/webhooks/pipefy/card-updated \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt_123",
    "card_id": "card_456",
    "cliente_email": "joao.silva@example.com",
    "timestamp": "2026-05-18T12:00:00Z"
  }'
```

**Response (200):**
```json
{
  "event_id": "evt_123",
  "cliente_email": "joao.silva@example.com",
  "status": "Processado",
  "prioridade": "prioridade_alta"
}
```

**Priority rule:** `valor_patrimonio >= 200000` → `prioridade_alta`, otherwise `prioridade_normal`.

---

## AWS Production Architecture (optional)

To scale this on AWS:

**API Layer:** Replace `uvicorn` with **API Gateway + Lambda** (one function per endpoint). Lambda handles stateless request processing and scales automatically.

**Webhook idempotency:** Replace the `webhook_events` SQLite table with a **DynamoDB** table using `event_id` as the partition key and a TTL attribute for automatic expiry. DynamoDB's conditional writes (`attribute_not_exists`) guarantee atomic idempotency checks even under concurrent requests.

**Client data:** Move SQLite to **RDS (PostgreSQL)** inside a VPC. Lambda functions connect via RDS Proxy to handle connection pooling efficiently under burst traffic.

**Pipefy integration:** When real HTTP calls to Pipefy are needed, publish events to **SQS** from the Lambda handler and process them with a separate consumer Lambda. This decouples the client-facing response time from Pipefy's API latency and provides built-in retry with dead-letter queues for failed mutations.
