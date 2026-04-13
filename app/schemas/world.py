from pydantic import BaseModel
from typing import Any, Dict, List


class WorldSettingIn(BaseModel):
    category: str
    key_name: str = ""
    content: Dict[str, Any] | List[Any] | str


class WorldGenerateResponse(BaseModel):
    project_id: int
    world: dict
