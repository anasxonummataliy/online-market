import os
from dataclasses import dataclass


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
class Configuration:
    db = PostgresConfig()
