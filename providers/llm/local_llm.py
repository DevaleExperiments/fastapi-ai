import requests

from providers.llm.base import LLMProvider


class LocalLLMProvider(LLMProvider):

    def __init__(
        self,
        base_url: str,
        model_name: str,
    ):
        self.base_url = base_url
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]