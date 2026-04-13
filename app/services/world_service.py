import json
from sqlalchemy.orm import Session
from app.core.llm_client import llm_client
from app.prompts.system_prompts import NOVEL_AGENT_SYSTEM_PROMPT
from app.prompts.world_prompts import WORLD_TEMPLATE
from app.services.prompt_service import PromptService
from app.services.project_service import ProjectService
from app.repositories.world_repo import WorldRepository


class WorldService:
    @staticmethod
    def generate_world(db: Session, project_id: int) -> dict:
        project = ProjectService.get_project_or_raise(db, project_id)
        prompt = PromptService.render(
            WORLD_TEMPLATE,
            title=project.title,
            genre=project.genre,
            platform_style=project.platform_style,
            tone=project.tone,
            summary=project.summary,
        )
        result = llm_client.chat(NOVEL_AGENT_SYSTEM_PROMPT, prompt, temperature=0.7)
        try:
            world_data = json.loads(result)
        except Exception:
            world_data = {"raw_text": result}

        if isinstance(world_data, dict):
            for key, value in world_data.items():
                WorldRepository.upsert(db, project_id, "world", key, json.dumps(value, ensure_ascii=False))
        else:
            WorldRepository.upsert(db, project_id, "world", "raw_text", json.dumps(world_data, ensure_ascii=False))

        return {"project_id": project_id, "world": world_data}
