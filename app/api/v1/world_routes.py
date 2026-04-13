from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.world_service import WorldService
from app.repositories.world_repo import WorldRepository

router = APIRouter(prefix="/projects/{project_id}/world", tags=["world"])


@router.post("/generate")
def generate_world(project_id: int, db: Session = Depends(get_db)):
    try:
        return WorldService.generate_world(db, project_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("")
def get_world(project_id: int, db: Session = Depends(get_db)):
    return {"project_id": project_id, "world": WorldRepository.list_by_project(db, project_id)}
