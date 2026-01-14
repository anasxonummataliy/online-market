from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[BigInteger] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[String] = mapped_column(String)
    last_name: Mapped[String] = mapped_column(String)

