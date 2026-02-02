import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class PostgresConfig:
    PG_USER: str = os.getenv("PG_USER", "")
    PG_PASS: str = os.getenv("PG_PASS", "")
    PG_HOST: str = os.getenv("PG_HOST", "localhost")
    PG_PORT: int = int(os.getenv("PG_PORT", "5432"))
    PG_DB: str = os.getenv("PG_DB", "")

    @property
    def db_url(self) -> str:
        return f"postgresql+psycopg2://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"


@dataclass
class RedisConfig:
    pass
    # REDIS_HOST: str = os.getenv("REDIS_HOST")
    # REDIS_PORT: int = os.getenv("REDIS_PORT")
    # REDIS_DB: int = os.getenv("REDIS_DB")


@dataclass
class BotConfig:
    TOKEN = os.getenv("BOT_TOKEN") or ""
    ADMIN = os.getenv("ADMIN") or ""


@dataclass
class Configuration:
    db = PostgresConfig()
    redis = RedisConfig()
    bot = BotConfig()


conf = Configuration()
