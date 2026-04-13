import json
from sqlalchemy.orm import Session
from app.repositories.project_repo import ProjectRepository
from app.repositories.chapter_repo import ChapterRepository
from app.repositories.outline_repo import OutlineRepository
from app.repositories.world_repo import WorldRepository
from app.repositories.character_repo import CharacterRepository
from app.repositories.foreshadowing_repo import ForeshadowingRepository
from app.services.cache_service import CacheService
from app.services.retrieval_service import RetrievalService


class ContextLoader:
    @staticmethod
    def load_for_chapter_generation(db: Session, project_id: int, chapter_no: int) -> dict:
        project = ProjectRepository.get_by_id(db, project_id)
        chapter_outline = OutlineRepository.get_chapter_outline(db, project_id, chapter_no)
        volume_outline = OutlineRepository.get_volume_outline(db, project_id, 1)
        world_settings = WorldRepository.list_by_project(db, project_id)
        characters = CharacterRepository.list_by_project(db, project_id)
        open_foreshadowings = ForeshadowingRepository.list_open(db, project_id)

        recent_summaries = CacheService.get_recent_summaries(project_id)
        if recent_summaries is None:
            recent_summaries = ChapterRepository.get_recent_summaries(db, project_id, limit=5)
            CacheService.set_recent_summaries(project_id, recent_summaries)

        retrieve_query = " ".join(
            [
                json.dumps(chapter_outline, ensure_ascii=False),
                volume_outline.get("volume_goal", "") if isinstance(volume_outline, dict) else "",
                " ".join([item.get("content", "") for item in open_foreshadowings[:3]]),
            ]
        ).strip()
        retrieved_memories = RetrievalService.search_relevant_memories(project_id, retrieve_query, top_k=5) if retrieve_query else []

        context = {
            "project_profile": {
                "title": project.title if project else "",
                "genre": project.genre if project else "",
                "platform_style": project.platform_style if project else "",
                "tone": project.tone if project else "",
                "summary": project.summary if project else "",
            },
            "chapter_outline": chapter_outline,
            "volume_goal": volume_outline.get("volume_goal", "") if isinstance(volume_outline, dict) else "",
            "world_rules": world_settings,
            "character_cards": characters,
            "recent_summaries": recent_summaries,
            "open_foreshadowings": open_foreshadowings,
            "retrieved_memories": retrieved_memories,
        }
        CacheService.set_context_snapshot(project_id, context)
        return context
