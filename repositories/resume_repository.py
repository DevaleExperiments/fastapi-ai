from sqlalchemy import select
from sqlalchemy.orm import Session

from models.resume import Resume


class ResumeRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, resume_id: int) -> Resume | None:
        statement = select(Resume).where(
            Resume.id == resume_id
        )

        return self.db.scalar(statement)