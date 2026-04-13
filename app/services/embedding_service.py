from openai import OpenAI
from app.core.config import settings


client = OpenAI(api_key=settings.LLM_API_KEY, base_url=settings.LLM_BASE_URL)


class EmbeddingService:
    @staticmethod
    def embed_text(text: str) -> list[float]:
        resp = client.embeddings.create(model=settings.EMBEDDING_MODEL, input=text)
        return resp.data[0].embedding
