from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy import create_engine

# Database Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./database/job_scheduler.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


Base.metadata.create_all(bind=engine)


# DB
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
