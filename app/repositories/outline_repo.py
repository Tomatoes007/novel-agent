import json
from sqlalchemy.orm import Session
from app.models.outline import Outline


class OutlineRepository:
    @staticmethod
    def upsert(db: Session, project_id: int, level: str, ref_no: int, title: str, content_json: str) -> Outline:
        row = (
            db.query(Outline)
            .filter(Outline.project_id == project_id, Outline.level == level, Outline.ref_no == ref_no)
            .first()
        )
        if row is None:
            row = Outline(
                project_id=project_id,
                level=level,
                ref_no=ref_no,
                title=title,
                content_json=content_json,
            )
            db.add(row)
        else:
            row.title = title
            row.content_json = content_json
        db.commit()
        db.refresh(row)
        return row

    @staticmethod
    def get_by_level_and_ref(db: Session, project_id: int, level: str, ref_no: int) -> Outline | None:
        return (
            db.query(Outline)
            .filter(Outline.project_id == project_id, Outline.level == level, Outline.ref_no == ref_no)
            .first()
        )

    @staticmethod
    def get_chapter_outline(db: Session, project_id: int, chapter_no: int) -> dict:
        row = OutlineRepository.get_by_level_and_ref(db, project_id, "chapter", chapter_no)
        if not row:
            return {}
        try:
            return json.loads(row.content_json)
        except Exception:
            return {}

    @staticmethod
    def get_volume_outline(db: Session, project_id: int, volume_no: int) -> dict:
        row = OutlineRepository.get_by_level_and_ref(db, project_id, "volume", volume_no)
        if not row:
            return {}
        try:
            return json.loads(row.content_json)
        except Exception:
            return {}

    @staticmethod
    def list_by_project(db: Session, project_id: int) -> list[Outline]:
        return db.query(Outline).filter(Outline.project_id == project_id).order_by(Outline.level, Outline.ref_no).all()
