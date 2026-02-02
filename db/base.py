from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.types import BigInteger, DateTime


class Base(DeclarativeBase):
    @declared_attr # type: ignore
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


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)


class CreatedBaseModel(BaseModel):
    __abstract__ = True

    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
