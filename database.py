from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

# Replace postgresql:// with postgresql+psycopg:// for psycopg3 driver
database_url = settings.database_url.replace("postgresql://", "postgresql+psycopg://")

engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

