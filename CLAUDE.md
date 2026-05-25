# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest -v
```

Run a single test file: `pytest tests/test_clientes.py -v`

## Architecture

FastAPI + SQLite (SQLAlchemy sync) + simulated Pipefy GraphQL integration.

```
app/
  main.py                    # FastAPI app init, router registration
  database.py                # SQLAlchemy engine, session, Base
  models.py                  # ORM models
  routers/                   # HTTP layer only — no business logic here
  services/
    cliente_service.py       # Validation, priority rule, idempotency logic
    pipefy_client.py         # GraphQL mutation payloads (no real HTTP — simulate only)
tests/
```

## Business rules

- **Email validation** on `POST /clientes`
- **Priority**: `patrimônio >= 200_000` → `prioridade_alta`, else `prioridade_normal`
- **Idempotency**: webhook endpoint rejects duplicate `event_id` values
- **Pipefy mutations**: `createCard` and `updateCardField` must match the official Pipefy GraphQL spec; log/return the payload instead of making a real HTTP call

## Test coverage requirements

Tests must cover: valid client creation, priority rule (both thresholds), and duplicate `event_id` blocking.

## Style

- Lean and explicit — no unnecessary abstractions or over-engineering.
- Routers own HTTP concerns only; push all logic into services.
