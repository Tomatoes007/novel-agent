from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.character import CharacterGenerateRequest
from app.services.character_service import CharacterService
from app.repositories.character_repo import CharacterRepository

router = APIRouter(prefix="/projects/{project_id}/characters", tags=["characters"])


@router.post("/generate")
def generate_characters(project_id: int, req: CharacterGenerateRequest, db: Session = Depends(get_db)):
    try:
        return CharacterService.generate_characters(db, project_id, req.character_count)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("")
def list_characters(project_id: int, db: Session = Depends(get_db)):
    return {"project_id": project_id, "characters": CharacterRepository.list_by_project(db, project_id)}
