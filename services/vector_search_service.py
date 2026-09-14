from repositories.job_embedding_repository import JobEmbeddingRepository
from repositories.resume_embedding_repository import ResumeEmbeddingRepository


class VectorSearchService:

    def __init__(
        self,
        resume_embedding_repository: ResumeEmbeddingRepository,
        job_embedding_repository: JobEmbeddingRepository,
    ):
        self.resume_embedding_repository = resume_embedding_repository
        self.job_embedding_repository = job_embedding_repository

    def search(
        self,
        resume_id: int,
        top_n: int,
    ) -> list[tuple[int, float]] | None:

        resume_embedding = (
            self.resume_embedding_repository.find_by_resume_id(resume_id)
        )

        if resume_embedding is None:
            return None

        return self.job_embedding_repository.search_similar_jobs(
            resume_embedding=resume_embedding.embedding,
            top_n=top_n,
        )