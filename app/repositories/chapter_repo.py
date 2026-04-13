from sqlalchemy.orm import Session
from app.models.chapter import Chapter


class ChapterRepository:
    @staticmethod
    def get_by_project_and_no(db: Session, project_id: int, chapter_no: int) -> Chapter | None:
        return (
            db.query(Chapter)
            .filter(Chapter.project_id == project_id, Chapter.chapter_no == chapter_no)
            .first()
        )

    @staticmethod
    def upsert(
        db: Session,
        project_id: int,
        chapter_no: int,
        title: str,
        content: str,
        summary: str,
        word_count: int,
        status: str = "draft",
    ) -> Chapter:
        row = ChapterRepository.get_by_project_and_no(db, project_id, chapter_no)
        if row is None:
            row = Chapter(
                project_id=project_id,
                chapter_no=chapter_no,
                title=title,
                content=content,
                summary=summary,
                word_count=word_count,
                status=status,
            )
            db.add(row)
        else:
            row.title = title
            row.content = content
            row.summary = summary
            row.word_count = word_count
            row.status = status
            row.version += 1
        db.commit()
        db.refresh(row)
        return row

    @staticmethod
    def update_partial(db: Session, row: Chapter, **kwargs) -> Chapter:
        for key, value in kwargs.items():
            if value is not None:
                setattr(row, key, value)
        row.version += 1
        db.commit()
        db.refresh(row)
        return row

    @staticmethod
    def get_recent_summaries(db: Session, project_id: int, limit: int = 5) -> list[dict]:
        rows = (
            db.query(Chapter)
            .filter(Chapter.project_id == project_id)
            .order_by(Chapter.chapter_no.desc())
            .limit(limit)
            .all()
        )
        rows = list(reversed(rows))
        return [
            {"chapter_no": row.chapter_no, "summary": row.summary}
            for row in rows
            if row.summary
        ]

    @staticmethod
    def list_by_project(db: Session, project_id: int) -> list[Chapter]:
        return db.query(Chapter).filter(Chapter.project_id == project_id).order_by(Chapter.chapter_no).all()
