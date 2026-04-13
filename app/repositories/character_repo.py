from sqlalchemy.orm import Session
from app.models.character import Character


class CharacterRepository:
    @staticmethod
    def create(db: Session, project_id: int, name: str, role: str, card_json: str, current_state_json: str, first_appearance_chapter: int = 0) -> Character:
        row = Character(
            project_id=project_id,
            name=name,
            role=role,
            card_json=card_json,
            current_state_json=current_state_json,
            first_appearance_chapter=first_appearance_chapter,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return row

    @staticmethod
    def upsert_by_name(db: Session, project_id: int, name: str, role: str, card_json: str, current_state_json: str, first_appearance_chapter: int = 0) -> Character:
        row = (
            db.query(Character)
            .filter(Character.project_id == project_id, Character.name == name)
            .first()
        )
        if row is None:
            return CharacterRepository.create(
                db,
                project_id,
                name,
                role,
                card_json,
                current_state_json,
                first_appearance_chapter,
            )
        row.role = role
        row.card_json = card_json
        row.current_state_json = current_state_json
        row.first_appearance_chapter = first_appearance_chapter
        db.commit()
        db.refresh(row)
        return row

    @staticmethod
    def list_by_project(db: Session, project_id: int) -> list[dict]:
        rows = db.query(Character).filter(Character.project_id == project_id).all()
        return [
            {
                "name": row.name,
                "role": row.role,
                "card_json": row.card_json,
                "current_state_json": row.current_state_json,
            }
            for row in rows
        ]
