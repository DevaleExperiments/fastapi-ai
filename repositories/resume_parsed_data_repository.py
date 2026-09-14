from sqlalchemy import select
from sqlalchemy.orm import Session

from models.resume_parsed_data import ResumeParsedData


class ResumeParsedDataRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_by_resume_id(
        self,
        resume_id: int,
    ) -> ResumeParsedData | None:
        statement = select(ResumeParsedData).where(
            ResumeParsedData.resume_id == resume_id
        )

        return self.db.scalar(statement)

    def update_parsed_json(
            self,
            resume_id: int,
            parsed_json: str,
    ) -> ResumeParsedData | None:
        data = self.find_by_resume_id(resume_id)

        if data is None:
            return None

        data.parsed_json = parsed_json

        self.db.commit()
        self.db.refresh(data)

        return data