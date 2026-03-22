import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

logger = logging.getLogger(__name__)

SQLITE_URL = "sqlite:///./learntoprompt.db"

def _build_postgres_url() -> str | None:
    """Build a PostgreSQL URL from individual Supabase env vars or DATABASE_URL."""
    if url := os.getenv("DATABASE_URL"):
        return url

    user = os.getenv("user") or os.getenv("DB_USER")
    password = os.getenv("password") or os.getenv("DB_PASSWORD")
    host = os.getenv("host") or os.getenv("DB_HOST")
    port = os.getenv("port") or os.getenv("DB_PORT", "5432")
    dbname = os.getenv("dbname") or os.getenv("DB_NAME")

    if all([user, password, host, dbname]):
        return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

    return None


def _create_engine_with_fallback():
    postgres_url = _build_postgres_url()

    if postgres_url:
        try:
            eng = create_engine(postgres_url)
            # Verify the connection is actually reachable
            with eng.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Connected to PostgreSQL database.")
            return eng
        except Exception as e:
            logger.warning("PostgreSQL connection failed (%s). Falling back to SQLite.", e)

    logger.info("Using SQLite database at %s", SQLITE_URL)
    return create_engine(SQLITE_URL, connect_args={"check_same_thread": False})


engine = _create_engine_with_fallback()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
