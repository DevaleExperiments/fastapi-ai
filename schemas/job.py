from pydantic import BaseModel

class JobInput(BaseModel):
    job_id: int
    title: str
    company_name: str
    description: str
    requirements: str | None = None