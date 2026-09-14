from providers.local_embedding import LocalEmbeddingProvider


provider = LocalEmbeddingProvider()

text = "Java Backend Developer with Spring Boot and PostgreSQL"

vector = provider.embed(text)

print(f"Model: {provider.model_name}")
print(f"Vector dimensions: {len(vector)}")
print(f"First 5 values: {vector[:5]}")