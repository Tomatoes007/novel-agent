from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.repositories.project_repo import ProjectRepository

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("")
def create_project(req: ProjectCreate, db: Session = Depends(get_db)):
    return ProjectRepository.create(db, req)


@router.get("")
def list_projects(db: Session = Depends(get_db)):
    return ProjectRepository.list_all(db)


@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = ProjectRepository.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}")
def update_project(project_id: int, req: ProjectUpdate, db: Session = Depends(get_db)):
    project = ProjectRepository.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectRepository.update(db, project, req)
