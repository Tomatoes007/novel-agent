from sqlalchemy.orm import Session
from app.models.timeline import TimelineEvent


class TimelineRepository:
    @staticmethod
    def create(db: Session, project_id: int, chapter_no: int, event_type: str, event_content: str, impact: str = "") -> TimelineEvent:
        row = TimelineEvent(
            project_id=project_id,
            chapter_no=chapter_no,
            event_type=event_type,
            event_content=event_content,
            impact=impact,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return row

    @staticmethod
    def list_by_project(db: Session, project_id: int) -> list[TimelineEvent]:
        return db.query(TimelineEvent).filter(TimelineEvent.project_id == project_id).order_by(TimelineEvent.chapter_no).all()
