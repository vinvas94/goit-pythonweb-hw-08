from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    CLOUDINARY_CLOUD_NAME: str | None = None
    CLOUDINARY_API_KEY: str | None = None
    CLOUDINARY_API_SECRET: str | None = None

    EMAIL_USER: str | None = None
    EMAIL_PASSWORD: str | None = None

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    BACKEND_URL: str = "http://localhost:8000"

    DB_URL: str = ""

    class Config:
        env_file = ".env"

    def model_post_init(self, __context):
        self.DB_URL = (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

settings = Settings()
