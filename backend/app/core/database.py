from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_url = "postgresql://mycrm_user:mycrm_admin@123@database:5432/mycrm_db"
engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base =declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
