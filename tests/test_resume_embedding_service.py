from config import settings
from database import SessionLocal
from models.resume_embedding import ResumeEmbedding
from providers.local_embedding import LocalEmbeddingProvider
from repositories.resume_embedding_repository import ResumeEmbeddingRepository
from repositories.resume_parsed_data_repository import ResumeParsedDataRepository
from services.resume_embedding_service import ResumeEmbeddingService


def main():
    db = SessionLocal()

    try:
        embedding_provider = LocalEmbeddingProvider(
            settings.embedding_model
        )

        parsed_data_repository = ResumeParsedDataRepository(db)
        embedding_repository = ResumeEmbeddingRepository(db)

        service = ResumeEmbeddingService(
            parsed_data_repository=parsed_data_repository,
            embedding_repository=embedding_repository,
            embedding_provider=embedding_provider,
            embedding_model=settings.embedding_model,
        )

        embedding = service.generate_and_save(resume_id=1)

        if embedding is None:
            print("No embedding generated.")
            return

        print("Embedding created")
        print("ID:", embedding.id)
        print("Resume ID:", embedding.resume_id)
        print("Model:", embedding.embedding_model)
        print("Dimensions:", len(embedding.embedding))

    finally:
        db.close()


if __name__ == "__main__":
    main()