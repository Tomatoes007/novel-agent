from pydantic import BaseModel


class ProposalRequest(BaseModel):
    user_idea: str


class WorldGenerateRequest(BaseModel):
    project_id: int


class GenericAgentRequest(BaseModel):
    action: str
    payload: dict
