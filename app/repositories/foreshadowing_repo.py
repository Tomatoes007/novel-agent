from sqlalchemy.orm import Session
from app.models.foreshadowing import Foreshadowing


class ForeshadowingRepository:
    @staticmethod
    def create(
        db: Session,
        project_id: int,
        content: str,
        related_characters: str = "[]",
        introduced_in_chapter: int = 0,
        status: str = "open",
        payoff_plan: str = "",
    ) -> Foreshadowing:
        row = Foreshadowing(
            project_id=project_id,
            content=content,
            related_characters=related_characters,
            introduced_in_chapter=introduced_in_chapter,
            status=status,
            payoff_plan=payoff_plan,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return row

    @staticmethod
    def list_open(db: Session, project_id: int) -> list[dict]:
        rows = (
            db.query(Foreshadowing)
            .filter(Foreshadowing.project_id == project_id, Foreshadowing.status != "paid_off")
            .order_by(Foreshadowing.introduced_in_chapter.asc())
            .all()
        )
        return [
            {
                "id": row.id,
                "content": row.content,
                "status": row.status,
                "introduced_in_chapter": row.introduced_in_chapter,
                "payoff_plan": row.payoff_plan,
            }
            for row in rows
        ]

    @staticmethod
    def mark_paid_off(db: Session, project_id: int, content: str, chapter_no: int) -> bool:
        row = (
            db.query(Foreshadowing)
            .filter(Foreshadowing.project_id == project_id, Foreshadowing.content == content)
            .first()
        )
        if row is None:
            return False
        row.status = "paid_off"
        row.resolved_in_chapter = chapter_no
        db.commit()
        return True
