from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Novel Agent Backend"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "123456"
    MYSQL_DB: str = "novel_agent"

    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""

    MILVUS_HOST: str = "127.0.0.1"
    MILVUS_PORT: str = "19530"
    MILVUS_COLLECTION: str = "novel_memory_chunks"

    LLM_BASE_URL: str = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    LLM_API_KEY: str = "sk-551570005413438fa86f44da3e6809fa"
    LLM_MODEL: str = "qwen-plus"

    EMBEDDING_MODEL: str = "text-embedding-v4"
    EMBEDDING_DIM: int = 1024

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

MYSQL_URL = (
    f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}"
    f"@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}?charset=utf8mb4"
)
