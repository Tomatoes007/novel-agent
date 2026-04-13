from sqlalchemy.orm import Session
from app.agents.chapter_writer import ChapterWriterAgent
from app.repositories.chapter_repo import ChapterRepository
from app.services.memory_service import MemoryService
from app.services.cache_service import CacheService


class ChapterService:
    @staticmethod
    def generate_and_save_chapter(
        db: Session,
        project_id: int,
        chapter_no: int,
        word_count: int = 2500,
        extra_requirements: str = "",
    ) -> dict:
        result = ChapterWriterAgent.generate_chapter(
            db=db,
            project_id=project_id,
            chapter_no=chapter_no,
            word_count=word_count,
            extra_requirements=extra_requirements,
        )

        content = result["content"]
        memory_delta = result["memory_delta"]
        title = memory_delta.get("title", f"第{chapter_no}章")
        summary = memory_delta.get("chapter_summary", "")

        ChapterRepository.upsert(
            db=db,
            project_id=project_id,
            chapter_no=chapter_no,
            title=title,
            content=content,
            summary=summary,
            word_count=len(content),
            status="draft",
        )

        MemoryService.update_from_chapter_delta(
            db=db,
            project_id=project_id,
            chapter_no=chapter_no,
            delta=memory_delta,
        )
        CacheService.invalidate_project_context(project_id)

        return {
            "chapter_no": chapter_no,
            "title": title,
            "content": content,
            "summary": summary,
            "memory_delta": memory_delta,
        }
