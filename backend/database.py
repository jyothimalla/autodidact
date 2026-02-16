import os
from urllib.parse import urlparse, urlunparse
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy import create_engine

# ======================
# Environment Variables
# ======================
load_dotenv()


def _is_running_in_docker() -> bool:
    return os.path.exists("/.dockerenv")


def _mask_db_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.password is None:
        return url
    netloc = parsed.netloc.replace(parsed.password, "***", 1)
    return urlunparse(parsed._replace(netloc=netloc))


def _resolve_database_url() -> str:
    database_url = os.getenv("DATABASE_URL", "")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set")

    parsed = urlparse(database_url)
    if parsed.hostname == "db" and not _is_running_in_docker():
        local_db_host = os.getenv("DB_HOST", "127.0.0.1")
        local_db_port = os.getenv("DB_PORT", str(parsed.port or 3306))
        credentials = ""
        if parsed.username:
            credentials = parsed.username
            if parsed.password:
                credentials += f":{parsed.password}"
            credentials += "@"
        new_netloc = f"{credentials}{local_db_host}:{local_db_port}"
        database_url = urlunparse(parsed._replace(netloc=new_netloc))

    return database_url


DATABASE_URL = _resolve_database_url()
print("Connecting to DB:", _mask_db_url(DATABASE_URL))

# Database connection setup
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
