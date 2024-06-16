from pydantic_settings import BaseSettings
import sqlalchemy
from sqlalchemy import create_engine
# from yarl import URL


class Settings(BaseSettings):
    """Application settings."""

    db: str = 'db'
    db_host: str = "localhost"
    db_port: int = 5134
    db_user: str = ''
    db_password: str = ''

    @property
    def get_engine(self) -> sqlalchemy.engine.Engine:
        """Assemble backend URL from settings.

        Returns:
            URL: backend URL.
        """
        uri = f"postgresql+psycopg://{self.db_user}:\{self.db_password}@{self.db_host}:{self.db_port}/{self.db}"
        return create_engine(uri)

    class Config:
        env_file = "doc_hack.env"
        env_prefix = "_"
        env_file_encoding = "utf-8"


settings = Settings()
