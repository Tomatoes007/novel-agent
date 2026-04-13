from pydantic import BaseModel
from typing import Any, Dict, List


class CharacterGenerateRequest(BaseModel):
    character_count: int = 5


class CharacterOut(BaseModel):
    id: int
    project_id: int
    name: str
    role: str
    card_json: str
    current_state_json: str

    model_config = {"from_attributes": True}
