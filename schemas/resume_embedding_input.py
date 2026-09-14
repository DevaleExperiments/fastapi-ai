from dataclasses import dataclass


@dataclass
class ResumeEmbeddingInput:
    resume_id: int
    summary: str | None
    skills: list[str]
    education: list[str]
    experience: list[str]
    projects: list[str]