from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    source_id: Mapped[str] = mapped_column(
        "provider",
        String,
        nullable=False,
    )

    external_job_id: Mapped[str] = mapped_column(
        "external_id",
        String,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    company_name: Mapped[str] = mapped_column(
        "company_name",
        String,
        nullable=False,
    )

    location: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    employment_type: Mapped[str | None] = mapped_column(
        "employment_type",
        String,
        nullable=True,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    requirements: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    salary_min: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    salary_max: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    currency: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    apply_url: Mapped[str | None] = mapped_column(
        "application_url",
        String,
        nullable=True,
    )

    posted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )