from pydantic import BaseModel
from typing import Optional, List


class ProjectCreate(BaseModel):
    title: str
    genre: str
    platform_style: str = "男频"
    tone: str = ""
    audience: str = ""
    summary: str = ""


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    platform_style: Optional[str] = None
    tone: Optional[str] = None
    audience: Optional[str] = None
    summary: Optional[str] = None


class ProjectOut(BaseModel):
    id: int
    title: str
    genre: str
    platform_style: str
    tone: str
    audience: str
    summary: str

    model_config = {"from_attributes": True}
