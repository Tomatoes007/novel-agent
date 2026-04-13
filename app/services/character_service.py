import json
import re
from sqlalchemy.orm import Session
from app.core.llm_client import llm_client
from app.prompts.system_prompts import NOVEL_AGENT_SYSTEM_PROMPT
from app.prompts.character_prompts import CHARACTER_TEMPLATE
from app.services.prompt_service import PromptService
from app.services.project_service import ProjectService
from app.repositories.character_repo import CharacterRepository


class CharacterService:
    @staticmethod
    def _parse_character_result(result: str):
        # 1. 先尝试直接解析
        try:
            data = json.loads(result)
        except Exception:
            data = None

        # 2. 如果失败，尝试提取 markdown json 代码块
        if data is None:
            match = re.search(r"```json\s*(.*?)\s*```", result, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group(1))
                except Exception:
                    data = None

        # 3. 兼容对象结构
        if isinstance(data, dict) and "characters" in data:
            data = data["characters"]

        # 4. 最终兜底
        if not isinstance(data, list):
            data = []

        return data

    @staticmethod
    def generate_characters(db: Session, project_id: int, character_count: int = 5) -> dict:
        project = ProjectService.get_project_or_raise(db, project_id)
        prompt = PromptService.render(
            CHARACTER_TEMPLATE,
            title=project.title,
            genre=project.genre,
            platform_style=project.platform_style,
            tone=project.tone,
            summary=project.summary,
            character_count=character_count,
        )

        result = llm_client.chat(NOVEL_AGENT_SYSTEM_PROMPT, prompt, temperature=0.8)
        data = CharacterService._parse_character_result(result)

        saved = []
        for item in data:
            row = CharacterRepository.upsert_by_name(
                db=db,
                project_id=project_id,
                name=item.get("name", "未命名角色"),
                role=item.get("role", "配角"),
                card_json=json.dumps(item, ensure_ascii=False),
                current_state_json=json.dumps(item.get("current_state", {}), ensure_ascii=False),
                first_appearance_chapter=item.get("first_appearance_chapter", 0),
            )
            saved.append({"id": row.id, "name": row.name, "role": row.role})

        return {"project_id": project_id, "characters": saved, "raw": data, "llm_raw": result}