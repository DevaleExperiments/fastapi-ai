from sqlalchemy import select
from sqlalchemy.orm import Session

from models.job import Job


class JobRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, job_id: int) -> Job | None:
        statement = select(Job).where(Job.id == job_id)

        return self.db.scalar(statement)

    def get_by_ids(self, job_ids: list[int]) -> list[Job]:
        if not job_ids:
            return []

        statement = select(Job).where(
            Job.id.in_(job_ids)
        )

        return list(self.db.scalars(statement).all())