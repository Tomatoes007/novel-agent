---
name: novel-agent-backend
description: Build, modify, and debug the Novel Agent backend built with FastAPI, SQLAlchemy, Redis, Milvus, and OpenAI-compatible APIs. Use when requests involve API routes, services, repositories, prompts, schema/model alignment, chapter-generation workflow, or backend bug fixing and validation in this repository.
---

# Novel Agent Backend

## Overview

Implement backend features end-to-end for this repository with predictable file-level edits and validation.
Follow the project layering (`api -> services -> repositories -> models/schemas -> core`) and preserve existing conventions.

## Quick Routing

- If the request is about endpoints, read `app/api/router.py` and `app/api/v1/*.py`.
- If the request is about business behavior, read `app/services/*.py` first.
- If the request is about persistence, read `app/repositories/*.py` and `app/models/*.py`.
- If the request is about request/response format, read `app/schemas/*.py`.
- If the request is about generation quality, inspect `app/prompts/*.py` and `app/agents/*.py`.
- If the request is about infra/runtime errors, inspect `app/core/config.py`, `app/core/database.py`, and client wrappers in `app/core/`.

## Implementation Workflow

1. Locate impacted files by layer and read adjacent modules before editing.
2. Apply minimal, consistent changes across model/schema/repository/service/api as needed.
3. Keep API contracts explicit in schemas and route docstrings where useful.
4. Preserve prompt-output parsing compatibility when modifying generation flows.
5. Validate with focused commands (import checks, app startup, or targeted tests if present).

## Change Patterns

- Add a new domain resource:
  1. Create SQLAlchemy model in `app/models/`.
  2. Add Pydantic schemas in `app/schemas/`.
  3. Add repository CRUD methods in `app/repositories/`.
  4. Add service orchestration in `app/services/`.
  5. Expose endpoints in `app/api/v1/` and register in router.
- Extend chapter-generation context:
  1. Update context loading in `app/agents/context_loader.py`.
  2. Update relevant prompt templates in `app/prompts/`.
  3. Ensure JSON parsing compatibility in `app/utils/json_parser.py`.
- Fix data mismatch:
  1. Verify schema/model field names and nullability.
  2. Verify repository query filters and service-level transformations.
  3. Validate API response against schema.

## Validation Checklist

- Confirm changed routes are mounted and request/response schemas align.
- Confirm service writes and reads still map to model fields correctly.
- Confirm generation outputs still parse to expected JSON shapes.
- Confirm no unrelated module imports or style regressions were introduced.

## References

- For repository layout and common edit entry points, read `references/repo-map.md`.
