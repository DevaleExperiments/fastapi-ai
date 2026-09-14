from sqlalchemy import select
from sqlalchemy.orm import Session

from models.job_embedding import JobEmbedding


class JobEmbeddingRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_by_job_id(self, job_id: int) -> JobEmbedding | None:
        statement = select(JobEmbedding).where(
            JobEmbedding.job_id == job_id
        )

        return self.db.scalar(statement)

    def save(self, embedding: JobEmbedding) -> JobEmbedding:
        self.db.add(embedding)
        self.db.commit()
        self.db.refresh(embedding)

        return embedding

    def update(
        self,
        embedding: JobEmbedding,
        vector: list[float],
        model_name: str,
    ) -> JobEmbedding:
        embedding.embedding = vector
        embedding.embedding_model = model_name

        self.db.commit()
        self.db.refresh(embedding)

        return embedding

    def search_similar_jobs(
            self,
            resume_embedding: list[float],
            top_n: int,
    ) -> list[tuple[int, float]]:
        distance = JobEmbedding.embedding.cosine_distance(
            resume_embedding
        )

        statement = (
            select(
                JobEmbedding.job_id,
                distance.label("distance"),
            )
            .order_by(distance)
            .limit(top_n)
        )

        results = self.db.execute(statement).all()

        return [
            (job_id, 1 - distance)
            for job_id, distance in results
        ]