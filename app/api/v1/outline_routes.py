from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.outline import OutlineGenerateRequest
from app.services.outline_service import OutlineService
from app.repositories.outline_repo import OutlineRepository

router = APIRouter(prefix="/projects/{project_id}/outlines", tags=["outlines"])


@router.post("/generate")
def generate_outline(project_id: int, req: OutlineGenerateRequest, db: Session = Depends(get_db)):
    try:
        return OutlineService.generate_outline(db, project_id, req.volume_no, req.chapter_count)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("")
def list_outlines(project_id: int, db: Session = Depends(get_db)):
    return {"project_id": project_id, "outlines": OutlineRepository.list_by_project(db, project_id)}
