from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .settings import settings

# Define Base for models
Base = declarative_base()

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# DB Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

