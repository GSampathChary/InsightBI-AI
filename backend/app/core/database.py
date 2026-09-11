import socket
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.app.core.config import settings

logger = logging.getLogger("insightbi.database")

def is_postgres_running(host: str = "127.0.0.1", port: int = 5432) -> bool:
    """Instant socket test (200ms max) to check if PostgreSQL/Docker is listening."""
    try:
        with socket.create_connection((host, port), timeout=0.2):
            return True
    except Exception:
        return False

def get_engine():
    # Instant non-blocking check for Postgres
    host = settings.DB_HOST or "127.0.0.1"
    port = settings.DB_PORT or 5432

    if is_postgres_running(host, port):
        try:
            logger.info(f"PostgreSQL detected on {host}:{port}. Connecting...")
            return create_engine(
                settings.DATABASE_URL,
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10
            )
        except Exception as e:
            logger.warning(f"PostgreSQL connection failed: {e}. Falling back to SQLite.")

    logger.info("PostgreSQL/Docker not running. Instant fallback to SQLite local database.")
    sqlite_url = "sqlite:///./insightbi_local.db"
    return create_engine(sqlite_url, connect_args={"check_same_thread": False})

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
