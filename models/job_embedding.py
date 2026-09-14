from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String, text

from models.base import Base


class JobEmbedding(Base):
    __tablename__ = "job_embeddings"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    job_id: Mapped[int] = mapped_column(
        nullable=False,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(384),
        nullable=False,
    )

    embedding_model: Mapped[str] = mapped_column(
        "model_name",
        String(100),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )