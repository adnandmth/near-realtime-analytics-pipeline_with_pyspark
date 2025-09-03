# config.py
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional, List


class Settings(BaseSettings):
    """Configuration for PySpark Data Pipeline"""

    # Application
    APP_NAME: str = "SparkDataPipeline"
    DEBUG: bool = False

    # Kafka
    KAFKA_BROKERS: str
    KAFKA_INPUT_TOPIC: str
    KAFKA_OUTPUT_TOPIC: Optional[str] = None
    KAFKA_STARTING_OFFSETS: str = "earliest"  # or "latest"

    # Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "postgres"
    
    # Spark
    SPARK_MASTER: str = "local[*]"
    SPARK_LOG_LEVEL: str = "WARN"
    SPARK_PACKAGES: List[str]
    
    @field_validator("KAFKA_BROKERS", mode="before")
    def validate_kafka_brokers(cls, v):
        if v is None:
            return v
        if isinstance(v, str):
            return v
        if isinstance(v, list):
            return v
        raise ValueError("KAFKA_BROKERS must be a literal string")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()