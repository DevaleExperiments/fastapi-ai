from functools import lru_cache

from config import settings
from providers.llm.local_llm import LocalLLMProvider


@lru_cache
def get_llm_provider() -> LocalLLMProvider:
    return LocalLLMProvider(
        base_url=settings.llm_base_url,
        model_name=settings.llm_model,
    )