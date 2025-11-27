from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create database engine
# For SQLite: need check_same_thread=False
# For PostgreSQL/other: no special connect_args needed
connect_args = {}
if "sqlite" in settings.database_url.lower():
    connect_args = {"check_same_thread": False}

# For PostgreSQL, use connection pooling
if "postgresql" in settings.database_url.lower() or "postgres" in settings.database_url.lower():
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=5,
        max_overflow=10
    )
else:
    engine = create_engine(
        settings.database_url,
        connect_args=connect_args
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
