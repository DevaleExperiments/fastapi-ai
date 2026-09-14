from pydantic import BaseModel


class JobEmbeddingResponse(BaseModel):
    job_id: int
    status: str