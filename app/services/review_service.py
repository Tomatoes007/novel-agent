from sqlalchemy.orm import Session
from app.core.llm_client import llm_client
from app.prompts.system_prompts import NOVEL_AGENT_SYSTEM_PROMPT
from app.prompts.review_prompts import REVIEW_TEMPLATE
from app.services.prompt_service import PromptService
from app.repositories.chapter_repo import ChapterRepository


class ReviewService:
    @staticmethod
    def review_chapter(db: Session, project_id: int, chapter_no: int) -> dict:
        chapter = ChapterRepository.get_by_project_and_no(db, project_id, chapter_no)
        if chapter is None:
            raise ValueError("chapter not found")
        prompt = PromptService.render(REVIEW_TEMPLATE, chapter_title=chapter.title, chapter_content=chapter.content)
        result = llm_client.chat(NOVEL_AGENT_SYSTEM_PROMPT, prompt, temperature=0.3)
        return {"review": result}
