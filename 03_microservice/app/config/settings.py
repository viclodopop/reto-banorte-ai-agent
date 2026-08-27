from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Banorte CV RAG Agent"
    VERSION: str = "1.0.0"
    API_KEY: str = "banorte-live-secret-key-2026"
    GEMINI_API_KEY: str = ""
    MODEL_NAME: str = "gemini-3.6-flash"
    KNOWLEDGE_DIR: str = "knowledge"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()