from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectRepository:
    @staticmethod
    def create(db: Session, data: ProjectCreate) -> Project:
        project = Project(**data.model_dump())
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def get_by_id(db: Session, project_id: int) -> Project | None:
        return db.query(Project).filter(Project.id == project_id).first()

    @staticmethod
    def list_all(db: Session) -> list[Project]:
        return db.query(Project).order_by(Project.id.desc()).all()

    @staticmethod
    def update(db: Session, project: Project, data: ProjectUpdate) -> Project:
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(project, key, value)
        db.commit()
        db.refresh(project)
        return project
