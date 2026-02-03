import logging
from datetime import datetime
from typing import Optional
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.types import BigInteger, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, sessionmaker
from sqlalchemy import (
    create_engine,
    select,
    delete as sqlalchemy_delete,
    update as sqlalchemy_update,
)

from config import conf


class Base(AsyncAttrs, DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        name = cls.__name__[1:]
        _name = cls.__name__[0]
        for i in name:
            if i.isupper():
                _name += "_"
            _name += i
        _name = _name.lower()

        if _name.endswith("y"):
            _name = _name[:-1] + "ie"
        return _name + "s"


class AbstractClass:
    @staticmethod
    async def commit():
        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            logging.info(f"postgres commit error: {e}")

    @classmethod
    async def get_all(cls):
        return (await db.execute(select(cls))).scalars()

    @classmethod
    async def create(cls, **kwargs):
        obj = cls(**kwargs)
        db.add(obj)
        await cls.commit()
        return obj

    @classmethod
    async def update(
        cls, _id: Optional[int] = None, telegram_id: Optional[int] = None, **kwargs
    ):
        if _id is not None:
            query = (
                sqlalchemy_update(cls)
                .where(cls.id == _id)
                .values(**kwargs)
                .execution_options(synchronize_session="fetch")
            )
        else:
            query = (
                sqlalchemy_update(cls)
                .where(cls.telegram_id == telegram_id)
                .values(**kwargs)
                .execution_options(synchronize_session="fetch")
            )
        db.execute(query)
        await cls.commit()

    @classmethod
    async def delete(cls, _id: Optional[int] = None, telegram_id: Optional[int] = None):
        if _id is not None:
            query = sqlalchemy_delete(cls).where(cls.id == _id)
        else:
            query = sqlalchemy_delete(cls).where(cls.telegram_id == telegram_id)
        db.execute(query)
        await cls.commit()
        return (await db.execute(select(cls))).scalars()


class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self):
        self._engine = create_async_engine(conf.db.db_url)
        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


db = AsyncDatabaseSession()
db.init()


class BaseModel(Base, AbstractClass):
    __abstract__ = True
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)


class TimeBasedModel(BaseModel):
    __abstract__ = True

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())


engine = create_engine(conf.db.db_url, echo=True)
