import json
from app.core.redis_client import redis_client


class CacheService:
    @staticmethod
    def get_recent_summaries(project_id: int):
        key = f"novel:project:{project_id}:recent_summaries"
        data = redis_client.get(key)
        return json.loads(data) if data else None

    @staticmethod
    def set_recent_summaries(project_id: int, summaries: list, ex: int = 3600):
        key = f"novel:project:{project_id}:recent_summaries"
        redis_client.set(key, json.dumps(summaries, ensure_ascii=False), ex=ex)

    @staticmethod
    def get_context_snapshot(project_id: int):
        key = f"novel:project:{project_id}:context_snapshot"
        data = redis_client.get(key)
        return json.loads(data) if data else None

    @staticmethod
    def set_context_snapshot(project_id: int, data: dict, ex: int = 1800):
        key = f"novel:project:{project_id}:context_snapshot"
        redis_client.set(key, json.dumps(data, ensure_ascii=False), ex=ex)

    @staticmethod
    def invalidate_project_context(project_id: int):
        redis_client.delete(f"novel:project:{project_id}:context_snapshot")
        redis_client.delete(f"novel:project:{project_id}:recent_summaries")
