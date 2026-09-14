from datetime import datetime

from sqlalchemy import DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class ResumeParsedData(Base):
    __tablename__ = "resume_parsed_data"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    resume_id: Mapped[int] = mapped_column(
        nullable=False,
    )

    raw_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    cleaned_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    parsed_json: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )