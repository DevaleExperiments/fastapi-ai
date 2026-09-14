from sqlalchemy import select
from sqlalchemy.orm import Session

from models.resume_embedding import ResumeEmbedding


class ResumeEmbeddingRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def find_by_resume_id(
        self,
        resume_id: int,
    ) -> ResumeEmbedding | None:
        statement = select(ResumeEmbedding).where(
            ResumeEmbedding.resume_id == resume_id
        )

        return self.db.scalar(statement)

    def save(
        self,
        embedding: ResumeEmbedding,
    ) -> ResumeEmbedding:
        self.db.add(embedding)
        self.db.commit()
        self.db.refresh(embedding)

        return embedding

    def update(
        self,
        embedding: ResumeEmbedding,
        vector: list[float],
        model_name: str,
    ) -> ResumeEmbedding:
        embedding.embedding = vector
        embedding.embedding_model = model_name

        self.db.commit()
        self.db.refresh(embedding)

        return embedding