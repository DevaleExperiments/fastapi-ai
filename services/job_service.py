from providers.embedding import EmbeddingProvider
from repositories.job_embedding_repository import JobEmbeddingRepository
from repositories.job_repository import JobRepository
from schemas.job import JobInput

from models.job_embedding import JobEmbedding


class JobService:

    def __init__(
        self,
        job_repository: JobRepository,
        embedding_provider: EmbeddingProvider,
        embedding_repository: JobEmbeddingRepository,
    ):
        self.job_repository = job_repository
        self.embedding_provider = embedding_provider
        self.embedding_repository = embedding_repository

    def prepare_job_text(self, job: JobInput) -> str:
        parts = [
            job.title,
            job.company_name,
            job.description,
        ]

        if job.requirements:
            parts.append(job.requirements)

        return "\n".join(parts)

    def generate_embedding(self, job: JobInput) -> list[float]:
        text = self.prepare_job_text(job)

        return self.embedding_provider.embed(text)

    def generate_and_save_embedding(self, job_id: int) -> JobEmbedding | None:
        job = self.job_repository.get_by_id(job_id)

        if job is None:
            return None

        job_input = JobInput(
            job_id=job.id,
            title=job.title,
            company_name=job.company_name,
            description=job.description,
            requirements=job.requirements,
        )

        vector = self.generate_embedding(job_input)

        existing_embedding = self.embedding_repository.find_by_job_id(job.id)

        if existing_embedding is not None:
            return self.embedding_repository.update(
                embedding=existing_embedding,
                vector=vector,
                model_name=self.embedding_provider.model_name,
            )

        embedding = JobEmbedding(
            job_id=job.id,
            embedding_model=self.embedding_provider.model_name,
            embedding=vector,
        )

        return self.embedding_repository.save(embedding)