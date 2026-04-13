import json
from sqlalchemy.orm import Session
from app.core.llm_client import llm_client
from app.prompts.system_prompts import NOVEL_AGENT_SYSTEM_PROMPT
from app.prompts.proposal_prompts import PROPOSAL_TEMPLATE
from app.services.prompt_service import PromptService
from app.repositories.project_repo import ProjectRepository


class ProjectService:
    @staticmethod
    def generate_proposal(db: Session, user_idea: str) -> dict:
        prompt = PromptService.render(PROPOSAL_TEMPLATE, user_idea=user_idea)
        result = llm_client.chat(NOVEL_AGENT_SYSTEM_PROMPT, prompt, temperature=0.8)
        return {"proposal": result}

    @staticmethod
    def get_project_or_raise(db: Session, project_id: int):
        project = ProjectRepository.get_by_id(db, project_id)
        if project is None:
            raise ValueError(f"Project {project_id} not found")
        return project
