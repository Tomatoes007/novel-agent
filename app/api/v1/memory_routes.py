from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.repositories.foreshadowing_repo import ForeshadowingRepository
from app.repositories.timeline_repo import TimelineRepository
from app.repositories.memory_repo import MemoryRepository
from app.services.retrieval_service import RetrievalService

router = APIRouter(prefix="/projects/{project_id}/memory", tags=["memory"])


@router.get("/foreshadowings")
def get_foreshadowings(project_id: int, db: Session = Depends(get_db)):
    return {"project_id": project_id, "foreshadowings": ForeshadowingRepository.list_open(db, project_id)}


@router.get("/timeline")
def get_timeline(project_id: int, db: Session = Depends(get_db)):
    return {"project_id": project_id, "timeline": TimelineRepository.list_by_project(db, project_id)}


@router.get("/recent")
def get_recent_memory(project_id: int, db: Session = Depends(get_db)):
    return {"project_id": project_id, "memory": MemoryRepository.list_recent_contents(db, project_id)}


@router.get("/search")
def search_memory(project_id: int, query: str, top_k: int = 5):
    return {"project_id": project_id, "results": RetrievalService.search_relevant_memories(project_id, query, top_k)}
