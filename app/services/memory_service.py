import json
from sqlalchemy.orm import Session
from app.repositories.foreshadowing_repo import ForeshadowingRepository
from app.repositories.timeline_repo import TimelineRepository
from app.repositories.memory_repo import MemoryRepository
from app.repositories.character_repo import CharacterRepository
from app.models.character import Character
from app.core.milvus_client import get_or_create_memory_collection
from app.services.embedding_service import EmbeddingService


class VectorMemoryService:
    @staticmethod
    def insert_chunk(
        project_id: int,
        source_type: str,
        source_ref: int,
        chunk_type: str,
        content: str,
    ) -> None:
        if not content.strip():
            return
        collection = get_or_create_memory_collection()
        vector = EmbeddingService.embed_text(content)
        data = [
            [project_id],
            [source_type],
            [source_ref],
            [chunk_type],
            [content],
            [vector],
        ]
        collection.insert(data)
        collection.flush()


class MemoryService:
    @staticmethod
    def update_from_chapter_delta(db: Session, project_id: int, chapter_no: int, delta: dict) -> None:
        if not delta:
            return

        chapter_summary = delta.get("chapter_summary", "")
        if chapter_summary:
            MemoryRepository.create(
                db=db,
                project_id=project_id,
                chunk_type="chapter_summary",
                source_type="chapter",
                source_ref=chapter_no,
                content=chapter_summary,
            )
            VectorMemoryService.insert_chunk(
                project_id=project_id,
                source_type="chapter",
                source_ref=chapter_no,
                chunk_type="chapter_summary",
                content=chapter_summary,
            )

        for item in delta.get("new_foreshadowing", []):
            if not isinstance(item, str):
                item = json.dumps(item, ensure_ascii=False) if item is not None else ""
            item = item.strip()
            if not item:
                continue
            ForeshadowingRepository.create(
                db=db,
                project_id=project_id,
                content=item,
                introduced_in_chapter=chapter_no,
                status="open",
            )
            MemoryRepository.create(
                db=db,
                project_id=project_id,
                chunk_type="foreshadowing",
                source_type="chapter",
                source_ref=chapter_no,
                content=item,
            )
            VectorMemoryService.insert_chunk(project_id, "chapter", chapter_no, "foreshadowing", item)

        for item in delta.get("resolved_foreshadowing", []):
            if not isinstance(item, str):
                item = json.dumps(item, ensure_ascii=False) if item is not None else ""
            item = item.strip()
            if not item:
                continue
            ForeshadowingRepository.mark_paid_off(db, project_id, item, chapter_no)

        for event in delta.get("timeline_events", []):
            if isinstance(event, str):
                TimelineRepository.create(db, project_id, chapter_no, "general", event, "")
                MemoryRepository.create(db, project_id, "plot_event", "chapter", chapter_no, event)
                VectorMemoryService.insert_chunk(project_id, "chapter", chapter_no, "plot_event", event)
            elif isinstance(event, dict):
                TimelineRepository.create(
                    db,
                    project_id,
                    chapter_no,
                    event.get("type", "general"),
                    event.get("event", ""),
                    event.get("impact", ""),
                )
                content = event.get("event", "")
                if content:
                    MemoryRepository.create(db, project_id, "plot_event", "chapter", chapter_no, content)
                    VectorMemoryService.insert_chunk(project_id, "chapter", chapter_no, "plot_event", content)
            else:
                content = str(event).strip()
                if content:
                    TimelineRepository.create(db, project_id, chapter_no, "general", content, "")
                    MemoryRepository.create(db, project_id, "plot_event", "chapter", chapter_no, content)
                    VectorMemoryService.insert_chunk(project_id, "chapter", chapter_no, "plot_event", content)

        for power_change in delta.get("power_changes", []):
            # LLM may return string items; keep them as memory but skip state update parsing.
            if isinstance(power_change, str):
                content = power_change.strip()
                if content:
                    MemoryRepository.create(db, project_id, "power_change", "chapter", chapter_no, content)
                    VectorMemoryService.insert_chunk(project_id, "chapter", chapter_no, "power_change", content)
                continue
            if not isinstance(power_change, dict):
                continue

            name = power_change.get("name")
            if not name:
                continue
            row = db.query(Character).filter(Character.project_id == project_id, Character.name == name).first()
            if row is None:
                continue
            state = json.loads(row.current_state_json or "{}")
            if power_change.get("power_level"):
                state["power_level"] = power_change["power_level"]
            if power_change.get("note"):
                state["latest_power_note"] = power_change["note"]
            row.current_state_json = json.dumps(state, ensure_ascii=False)

        for rel in delta.get("relationship_changes", []):
            content = rel if isinstance(rel, str) else json.dumps(rel, ensure_ascii=False)
            MemoryRepository.create(db, project_id, "relationship_change", "chapter", chapter_no, content)
            VectorMemoryService.insert_chunk(project_id, "chapter", chapter_no, "relationship_change", content)

        db.commit()
