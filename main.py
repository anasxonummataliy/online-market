from sqlalchemy import create_engine
from config import conf
from db import Base

engine = create_engine(conf.db.db_url)
Base.metadata.create_all(engine) 