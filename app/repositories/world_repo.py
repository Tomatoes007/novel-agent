from sqlalchemy.orm import Session
from app.models.world import WorldSetting


class WorldRepository:
    @staticmethod
    def upsert(db: Session, project_id: int, category: str, key_name: str, content_json: str) -> WorldSetting:
        row = (
            db.query(WorldSetting)
            .filter(
                WorldSetting.project_id == project_id,
                WorldSetting.category == category,
                WorldSetting.key_name == key_name,
            )
            .first()
        )
        if row is None:
            row = WorldSetting(
                project_id=project_id,
                category=category,
                key_name=key_name,
                content_json=content_json,
            )
            db.add(row)
        else:
            row.content_json = content_json
        db.commit()
        db.refresh(row)
        return row

    @staticmethod
    def list_by_project(db: Session, project_id: int) -> list[dict]:
        rows = db.query(WorldSetting).filter(WorldSetting.project_id == project_id).all()
        return [
            {
                "category": row.category,
                "key_name": row.key_name,
                "content_json": row.content_json,
            }
            for row in rows
        ]
