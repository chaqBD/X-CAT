from typing import Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: Optional[str] = None
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 50

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def database_url_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v.strip() == "":
            return None
        return v

    def get_database_url(self) -> str:
        """Return DATABASE_URL, raising a clear error if it is not configured."""
        if not self.DATABASE_URL:
            raise RuntimeError(
                "DATABASE_URL is not set. "
                "Ensure the environment variable is configured before the app handles requests."
            )
        return self.DATABASE_URL


settings = Settings()
