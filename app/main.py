from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.database import Base, engine
from app import models  # noqa: F401
from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
app.include_router(api_router, prefix=settings.API_PREFIX)
app.mount("/ui", StaticFiles(directory="app/web", html=True), name="ui")


@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
