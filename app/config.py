from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str

    # Vector DB (Qdrant)
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION_NAME: str = "rag_chunks"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # Database (SQLite fallback or simple storage)
    SQLITE_DB_PATH: str = "./app.db"

    class Config:
        env_file = ".env"
        extra = "ignore"


# Singleton instance (IMPORTANT)
settings = Settings()

#no need to use os.getenv("OPENAI_API_KEY")
#This is called a  Singleton Configuration Pattern