from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Grading Backend (NoSQL)"
    MONGODB_URL: str
    DB_NAME: str = "grading_db"

    class Config:
        env_file = ".env"

settings = Settings()