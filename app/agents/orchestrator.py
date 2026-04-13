from sqlalchemy.orm import Session
from app.services.chapter_service import ChapterService
from app.services.project_service import ProjectService
from app.services.world_service import WorldService
from app.services.character_service import CharacterService
from app.services.outline_service import OutlineService
from app.services.review_service import ReviewService


class AgentOrchestrator:
    @staticmethod
    def run(db: Session, action: str, payload: dict) -> dict:
        if action == "generate_chapter":
            return ChapterService.generate_and_save_chapter(
                db=db,
                project_id=payload["project_id"],
                chapter_no=payload["chapter_no"],
                word_count=payload.get("word_count", 2500),
                extra_requirements=payload.get("extra_requirements", ""),
            )
        if action == "generate_proposal":
            return ProjectService.generate_proposal(db=db, user_idea=payload["user_idea"])
        if action == "generate_world":
            return WorldService.generate_world(db=db, project_id=payload["project_id"])
        if action == "generate_characters":
            return CharacterService.generate_characters(
                db=db,
                project_id=payload["project_id"],
                character_count=payload.get("character_count", 5),
            )
        if action == "generate_outline":
            return OutlineService.generate_outline(
                db=db,
                project_id=payload["project_id"],
                volume_no=payload.get("volume_no", 1),
                chapter_count=payload.get("chapter_count", 10),
            )
        if action == "review_chapter":
            return ReviewService.review_chapter(
                db=db,
                project_id=payload["project_id"],
                chapter_no=payload["chapter_no"],
            )
        raise ValueError(f"Unsupported action: {action}")
