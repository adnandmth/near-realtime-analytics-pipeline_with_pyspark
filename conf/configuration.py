import os

AWS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET = os.environ.get("AWS_SECRET_ACCESS_KEY")
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "broker:29092")
KAFKA_IDEAL_TOPIC = os.environ.get("KAFKA_IDEAL_TOPIC", "ideal")
KAFKA_CORE03ASIA_TOPIC = os.environ.get("KAFKA_CORE03ASIA_TOPIC", "core03-asia")
PGHOST = os.environ.get("PGHOST", "localhost")
PGUSER = os.environ.get("PGUSER", "postgres")
PGPASSWORD = os.environ.get("PGPASSWORD")
PGDATABASE = os.environ.get("PGDATABASE", "postgres")
PGPORT = os.environ.get("PGPORT", "5432")
PGDRIVER = os.environ.get("PGDRIVER", "org.postgresql.Driver")

configuration = {
    "AWS_ACCESS_KEY": AWS_KEY,
    "AWS_SECRET_KEY": AWS_SECRET,
    "KAFKA_BOOTSTRAP_SERVERS": KAFKA_BOOTSTRAP_SERVERS,
    "KAFKA_IDEAL_TOPIC": KAFKA_BOOTSTRAP_SERVERS,
    "KAFKA_CORE03ASIA_TOPIC": KAFKA_BOOTSTRAP_SERVERS,
    "PGHOST": PGHOST,
    "PGUSER": PGUSER,
    "PGPASSWORD": PGPASSWORD,
    "PGDATABASE": PGDATABASE,
    "PGPORT": PGPORT,
    "PGDRIVER": PGDRIVER
}

