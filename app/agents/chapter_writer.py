import json
from sqlalchemy.orm import Session
from app.core.llm_client import llm_client
from app.prompts.system_prompts import NOVEL_AGENT_SYSTEM_PROMPT
from app.prompts.chapter_prompts import CHAPTER_WRITE_TEMPLATE
from app.agents.context_loader import ContextLoader
from app.services.prompt_service import PromptService
from app.utils.json_parser import extract_json_block
from app.utils.text_utils import extract_main_content


class ChapterWriterAgent:
    @staticmethod
    def generate_chapter(
        db: Session,
        project_id: int,
        chapter_no: int,
        word_count: int = 2500,
        extra_requirements: str = "",
    ) -> dict:
        context = ContextLoader.load_for_chapter_generation(db, project_id, chapter_no)

        user_prompt = PromptService.render(
            CHAPTER_WRITE_TEMPLATE,
            project_profile=json.dumps(context["project_profile"], ensure_ascii=False, indent=2),
            volume_goal=context["volume_goal"],
            chapter_outline=json.dumps(context["chapter_outline"], ensure_ascii=False, indent=2),
            character_cards=json.dumps(context["character_cards"], ensure_ascii=False, indent=2),
            world_rules=json.dumps(context["world_rules"], ensure_ascii=False, indent=2),
            recent_summaries=json.dumps(context["recent_summaries"], ensure_ascii=False, indent=2),
            open_foreshadowings=json.dumps(context["open_foreshadowings"], ensure_ascii=False, indent=2),
            retrieved_memories=json.dumps(context["retrieved_memories"], ensure_ascii=False, indent=2),
            extra_requirements=extra_requirements,
            word_count=word_count,
        )

        raw_output = llm_client.chat(
            system_prompt=NOVEL_AGENT_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.85,
        )
        content = extract_main_content(raw_output)
        summary_json = extract_json_block(raw_output)
        return {
            "content": content,
            "memory_delta": summary_json,
            "raw_output": raw_output,
        }
