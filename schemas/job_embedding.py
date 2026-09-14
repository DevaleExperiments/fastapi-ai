from pydantic import BaseModel


class JobEmbeddingRequest(BaseModel):
    job_id: int