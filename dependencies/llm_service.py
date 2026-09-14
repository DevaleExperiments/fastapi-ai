from fastapi import Depends

from dependencies.llm import get_llm_provider
from providers.llm.local_llm import LocalLLMProvider
from services.llm_service import LLMService


def get_llm_service(
    llm_provider: LocalLLMProvider = Depends(
        get_llm_provider
    ),
) -> LLMService:
    return LLMService(
        llm_provider=llm_provider,
    )