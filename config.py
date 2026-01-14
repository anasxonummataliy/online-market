import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()

@dataclass
class PostgresConfig:
    PG_USER: str = os.getenv("PG_USER")
    PG_PASS: int = os.getenv("PG_PASS")
    PG_HOST: str = os.getenv("PG_HOST")
    PG_PORT: int = os.getenv("PG_PORT")
    PG_DB: str = os.getenv("PG_DB")

    @property
    def db_url(self) -> str:
        return f"postgresql://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"

@dataclass
class RedisConfig:
    pass
    # REDIS_HOST: str = os.getenv("REDIS_HOST")
    # REDIS_PORT: int = os.getenv("REDIS_PORT")
    # REDIS_DB: int = os.getenv("REDIS_DB")

@dataclass
class Configuration:
    db = PostgresConfig()


conf = Configuration()