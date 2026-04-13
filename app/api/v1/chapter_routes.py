from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.chapter import ChapterGenerateRequest, ChapterUpdateRequest
from app.services.chapter_service import ChapterService
from app.services.review_service import ReviewService
from app.repositories.chapter_repo import ChapterRepository

router = APIRouter(prefix="/projects/{project_id}/chapters", tags=["chapters"])


@router.post("/{chapter_no}/generate")
def generate_chapter(project_id: int, chapter_no: int, req: ChapterGenerateRequest, db: Session = Depends(get_db)):
    try:
        return ChapterService.generate_and_save_chapter(
            db=db,
            project_id=project_id,
            chapter_no=chapter_no,
            word_count=req.word_count,
            extra_requirements=req.extra_requirements,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
def list_chapters(project_id: int, db: Session = Depends(get_db)):
    return {"project_id": project_id, "chapters": ChapterRepository.list_by_project(db, project_id)}


@router.get("/{chapter_no}")
def get_chapter(project_id: int, chapter_no: int, db: Session = Depends(get_db)):
    row = ChapterRepository.get_by_project_and_no(db, project_id, chapter_no)
    if row is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return row


@router.put("/{chapter_no}")
def update_chapter(project_id: int, chapter_no: int, req: ChapterUpdateRequest, db: Session = Depends(get_db)):
    row = ChapterRepository.get_by_project_and_no(db, project_id, chapter_no)
    if row is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    updated = ChapterRepository.update_partial(db, row, **req.model_dump(exclude_none=True))
    return updated


@router.post("/{chapter_no}/review")
def review_chapter(project_id: int, chapter_no: int, db: Session = Depends(get_db)):
    try:
        return ReviewService.review_chapter(db, project_id, chapter_no)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
