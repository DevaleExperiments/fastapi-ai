from sentence_transformers import SentenceTransformer

from providers.embedding import EmbeddingProvider


class LocalEmbeddingProvider(EmbeddingProvider):

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list[float]:
        vector = self.model.encode(text)

        return vector.tolist()