# Repository Map

## Primary flow

1. API routes in `app/api/v1/` receive request payloads.
2. Services in `app/services/` orchestrate business logic.
3. Repositories in `app/repositories/` handle persistence operations.
4. Models in `app/models/` define SQLAlchemy entities.
5. Schemas in `app/schemas/` define request/response contracts.

## Generation workflow files

- `app/agents/orchestrator.py`
- `app/agents/context_loader.py`
- `app/agents/chapter_writer.py`
- `app/prompts/*.py`
- `app/utils/json_parser.py`

## Infra and clients

- `app/core/config.py`
- `app/core/database.py`
- `app/core/redis_client.py`
- `app/core/milvus_client.py`
- `app/core/llm_client.py`

## Common edit points

- Add route: `app/api/v1/<domain>_routes.py` and `app/api/router.py`
- Add service method: `app/services/<domain>_service.py`
- Add repository query: `app/repositories/<domain>_repo.py`
- Add schema field: `app/schemas/<domain>.py`
- Add model field: `app/models/<domain>.py`
