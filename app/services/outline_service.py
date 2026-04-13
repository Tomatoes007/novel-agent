import json
from sqlalchemy.orm import Session
from app.core.llm_client import llm_client
from app.prompts.system_prompts import NOVEL_AGENT_SYSTEM_PROMPT
from app.prompts.outline_prompts import OUTLINE_TEMPLATE
from app.services.project_service import ProjectService
from app.services.prompt_service import PromptService
from app.repositories.outline_repo import OutlineRepository
from app.repositories.character_repo import CharacterRepository
from app.repositories.world_repo import WorldRepository


class OutlineService:
    @staticmethod
    def generate_outline(db: Session, project_id: int, volume_no: int = 1, chapter_count: int = 10) -> dict:
        project = ProjectService.get_project_or_raise(db, project_id)
        characters = CharacterRepository.list_by_project(db, project_id)
        world = WorldRepository.list_by_project(db, project_id)
        prompt = PromptService.render(
            OUTLINE_TEMPLATE,
            title=project.title,
            genre=project.genre,
            platform_style=project.platform_style,
            tone=project.tone,
            summary=project.summary,
            character_cards=json.dumps(characters, ensure_ascii=False, indent=2),
            world_rules=json.dumps(world, ensure_ascii=False, indent=2),
            chapter_count=chapter_count,
            volume_no=volume_no,
        )
        result = llm_client.chat(NOVEL_AGENT_SYSTEM_PROMPT, prompt, temperature=0.8)
        try:
            outline = json.loads(result)
        except Exception:
            outline = {"raw_text": result}

        OutlineRepository.upsert(
            db=db,
            project_id=project_id,
            level="volume",
            ref_no=volume_no,
            title=outline.get("volume_title", f"第{volume_no}卷") if isinstance(outline, dict) else f"第{volume_no}卷",
            content_json=json.dumps(outline, ensure_ascii=False),
        )
        if isinstance(outline, dict):
            for chapter in outline.get("chapters", []):
                chapter_no = int(chapter.get("chapter_no", 0))
                if chapter_no <= 0:
                    continue
                OutlineRepository.upsert(
                    db=db,
                    project_id=project_id,
                    level="chapter",
                    ref_no=chapter_no,
                    title=chapter.get("title", f"第{chapter_no}章"),
                    content_json=json.dumps(chapter, ensure_ascii=False),
                )
        return {"project_id": project_id, "outline": outline}
