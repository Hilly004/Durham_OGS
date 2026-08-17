from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class Satellite(Base):
    __tablename__ = "satellites"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
        index=True
    )

    tle_line1: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    tle_line2: Mapped[str] = mapped_column(
        String,
        nullable=False
    )