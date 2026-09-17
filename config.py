from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NextRole AI Engine"
    app_version: str = "0.1.0"
    database_url: str

    embedding_model: str = "all-MiniLM-L6-v2"

    llm_base_url: str = "http://localhost:11434"
    llm_model: str = "llama3.2:3b"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()


if __name__ == "__main__":
    print(settings.app_name)
    print(settings.app_version)
    print(settings.embedding_model)
    print(settings.llm_base_url)
    print(settings.llm_model)

