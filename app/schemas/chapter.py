from pydantic import BaseModel
from typing import Any, Dict


class ChapterGenerateRequest(BaseModel):
    word_count: int = 2500
    extra_requirements: str = ""


class ChapterUpdateRequest(BaseModel):
    title: str | None = None
    content: str | None = None
    summary: str | None = None
    status: str | None = None


class ChapterGenerateResponse(BaseModel):
    chapter_no: int
    title: str
    content: str
    summary: str
    memory_delta: Dict[str, Any]
