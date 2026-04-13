from app.core.milvus_client import get_or_create_memory_collection
from app.services.embedding_service import EmbeddingService


class RetrievalService:
    @staticmethod
    def search_relevant_memories(project_id: int, query: str, top_k: int = 5) -> list[dict]:
        if not query.strip():
            return []
        collection = get_or_create_memory_collection()
        vector = EmbeddingService.embed_text(query)
        expr = f"project_id == {project_id}"
        results = collection.search(
            data=[vector],
            anns_field="embedding",
            param={"metric_type": "COSINE", "params": {"nprobe": 10}},
            limit=top_k,
            expr=expr,
            output_fields=["project_id", "source_type", "source_ref", "chunk_type", "content"],
        )
        output = []
        for hit in results[0]:
            entity = hit.entity
            output.append(
                {
                    "score": float(hit.distance),
                    "source_type": entity.get("source_type"),
                    "source_ref": entity.get("source_ref"),
                    "chunk_type": entity.get("chunk_type"),
                    "content": entity.get("content"),
                }
            )
        return output
