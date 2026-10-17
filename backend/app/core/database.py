"""
Database Connection and Session Management for KrishiRakshak
Supports PostgreSQL as primary database with automated graceful fallback to SQLite
for zero-friction college project evaluation and local development.
"""
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

Base = declarative_base()

def get_engine():
    db_url = settings.DATABASE_URL
    # Try connecting to configured database
    try:
        engine = create_engine(db_url, pool_pre_ping=True)
        # Test connection
        with engine.connect() as conn:
            logger.info("Successfully connected to primary database: %s", db_url.split('@')[-1] if '@' in db_url else db_url)
        return engine
    except Exception as e:
        logger.warning(
            "Could not connect to configured PostgreSQL database (%s). Falling back to SQLite for academic demo.", e
        )
        sqlite_path = os.path.join(settings.BASE_DIR, "krishirakshak.db")
        sqlite_url = f"sqlite:///{sqlite_path}"
        engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
        return engine

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """FastAPI Dependency for database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
