from providers.embedding import EmbeddingProvider
from repositories.resume_embedding_repository import ResumeEmbeddingRepository
from repositories.resume_parsed_data_repository import ResumeParsedDataRepository
from models.resume_embedding import ResumeEmbedding



class ResumeEmbeddingService:

    def __init__(
        self,
        parsed_data_repository: ResumeParsedDataRepository,
        embedding_repository: ResumeEmbeddingRepository,
        embedding_provider: EmbeddingProvider,
        embedding_model: str,
    ):
        self.parsed_data_repository = parsed_data_repository
        self.embedding_repository = embedding_repository
        self.embedding_provider = embedding_provider
        self.embedding_model = embedding_model

    def generate_and_save(
            self,
            resume_id: int,
    ) -> ResumeEmbedding | None:

        parsed_data = self.parsed_data_repository.find_by_resume_id(
            resume_id
        )

        if parsed_data is None:
            return None

        text = parsed_data.cleaned_text

        if not text:
            return None

        vector = self.embedding_provider.embed(text)

        existing_embedding = self.embedding_repository.find_by_resume_id(
            resume_id
        )

        if existing_embedding is not None:
            return self.embedding_repository.update(
                embedding=existing_embedding,
                vector=vector,
                model_name=self.embedding_model,
            )

        embedding = ResumeEmbedding(
            resume_id=resume_id,
            embedding=vector,
            embedding_model=self.embedding_model,
        )

        return self.embedding_repository.save(embedding)