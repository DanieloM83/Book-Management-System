from functools import cached_property

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    FRONTEND_URL: str

    POSTGRES_USER: str
    POSTGRES_PASS: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_BASE: str

    REDIS_USER: str
    REDIS_PASS: str
    REDIS_HOST: str
    REDIS_PORT: int

    JWT_SECRET_KEY: str
    COOKIE_NAME: str
    COOKIE_AGE: int

    @cached_property
    def POSTGRES_DSN(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASS}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_BASE}"

    @cached_property
    def ALEMBIC_DSN(self):
        """DSN for alembic migrations. Psycopg2 is used as driver."""
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASS}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_BASE}"

    @cached_property
    def REDIS_DSN(self) -> str:
        return f"redis://{self.REDIS_USER}:{self.REDIS_PASS}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
