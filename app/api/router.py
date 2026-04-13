from fastapi import APIRouter
from app.api.v1.project_routes import router as project_router
from app.api.v1.world_routes import router as world_router
from app.api.v1.character_routes import router as character_router
from app.api.v1.outline_routes import router as outline_router
from app.api.v1.chapter_routes import router as chapter_router
from app.api.v1.memory_routes import router as memory_router
from app.api.v1.agent_routes import router as agent_router


api_router = APIRouter()
api_router.include_router(project_router)
api_router.include_router(world_router)
api_router.include_router(character_router)
api_router.include_router(outline_router)
api_router.include_router(chapter_router)
api_router.include_router(memory_router)
api_router.include_router(agent_router)
