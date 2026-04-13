from pydantic import BaseModel
from typing import Any, Dict, List


class OutlineGenerateRequest(BaseModel):
    volume_no: int = 1
    chapter_count: int = 10


class OutlineOut(BaseModel):
    id: int
    project_id: int
    level: str
    ref_no: int
    title: str
    content_json: str

    model_config = {"from_attributes": True}
