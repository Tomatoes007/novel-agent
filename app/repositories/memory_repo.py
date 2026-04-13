from sqlalchemy.orm import Session
from app.models.memory_chunk import MemoryChunk


class MemoryRepository:
    @staticmethod
    def create(db: Session, project_id: int, chunk_type: str, source_type: str, source_ref: int, content: str) -> MemoryChunk:
        row = MemoryChunk(
            project_id=project_id,
            chunk_type=chunk_type,
            source_type=source_type,
            source_ref=source_ref,
            content=content,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return row

    @staticmethod
    def list_recent_contents(db: Session, project_id: int, limit: int = 5) -> list[str]:
        rows = (
            db.query(MemoryChunk)
            .filter(MemoryChunk.project_id == project_id)
            .order_by(MemoryChunk.id.desc())
            .limit(limit)
            .all()
        )
        return [row.content for row in rows]
