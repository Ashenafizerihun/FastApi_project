from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

DATABASE_URL = f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Function to get a database connection
def get_db():
    """
    This function creates a new database connection using the SessionLocal.
    It returns a new session object that can be used to interact with the database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
