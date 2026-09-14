from pydantic import BaseModel


class ExperienceEntry(BaseModel):
    company: str | None = None
    job_title: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class ResumeProfile(BaseModel):
    full_name: str | None = None
    current_job_title: str | None = None
    years_of_experience: float | None = None
    technical_skills: list[str] = []
    professional_summary: str | None = None
    experience: list[ExperienceEntry] = []