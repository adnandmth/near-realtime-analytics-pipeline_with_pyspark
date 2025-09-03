from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from core.config import settings
import os

def get_engine(pg_properties: dict = None):
    """Create and return a SQLAlchemy engine connected to PostgreSQL."""
    if pg_properties is None:
        pg_properties = {
            "user": settings.POSTGRES_USER or os.getenv("POSTGRES_USER"),
            "password": settings.POSTGRES_PASSWORD or os.getenv("POSTGRES_PASSWORD"),
            "host": settings.POSTGRES_HOST or os.getenv("POSTGRES_HOST", "localhost"),
            "port": settings.POSTGRES_PORT or os.getenv("POSTGRES_PORT", 5432),
            "database": settings.POSTGRES_DB or os.getenv("POSTGRES_DB"),
        }

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=pg_properties["user"],
        password=pg_properties["password"],
        host=pg_properties["host"],
        port=pg_properties["port"],
        database=pg_properties["database"]
    )

    return create_engine(url, pool_pre_ping=True)