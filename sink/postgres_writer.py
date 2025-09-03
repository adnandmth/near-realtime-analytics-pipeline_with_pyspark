from sqlalchemy import text
from core.database import get_engine
from core.config import settings
from pyspark.sql import functions as F
from pyspark.sql.types import LongType
import re

def write_to_postgres(batch_df, batch_id) -> None:
    print(f"Processing batch {batch_id} with {batch_df.count()} rows")

    if batch_df.isEmpty():
        print(f"Skipping empty batch {batch_id}")
        return
    
    # 1. Cast "timestamp" to BIGINT
    batch_df = batch_df.withColumn(
        "timestamp",
        F.col("timestamp").cast(LongType())
    )

    # 2. Add partition timestamp + created_at
    batch_df = batch_df.withColumn(
        "date_partition",
        F.from_unixtime(F.col("timestamp") / 1000).cast("timestamp")
    ).withColumn(
        "created_at",
        F.current_timestamp()
    )
    
    # Connection setup
    pg_properties = {
        "user": settings.POSTGRES_USER,
        "password": settings.POSTGRES_PASSWORD,
        "host": settings.POSTGRES_HOST,
        "port": settings.POSTGRES_PORT,
        "database": settings.POSTGRES_DB
    }
    
    ddl_engine = get_engine(pg_properties)
    jdbc_url = (
        f"jdbc:postgresql://{pg_properties['host']}:{pg_properties['port']}/"
        f"{pg_properties['database']}"
    )
    
    # Handle multiple target tables
    table_names = [row["table"] for row in batch_df.select("table").distinct().collect()]

    for tbl_name in table_names:
        safe_tbl_name = re.sub(r"[^a-zA-Z0-9_]", "_", tbl_name)
        target_table = f"stg_kinesis__{safe_tbl_name}"

        print(f"Preparing table: {target_table}")

        # 2a. DDL
        ddl_sql = f"""
            CREATE TABLE IF NOT EXISTS public.{target_table} (
                "timestamp" BIGINT NULL,
                country TEXT NULL,
                service TEXT NULL,
                "table" TEXT NULL,
                "event" TEXT NULL,
                record TEXT NULL,
                date_partition TIMESTAMP NULL,
                created_at TIMESTAMP NULL
            )
        """
        with ddl_engine.begin() as conn:
            conn.execute(text(ddl_sql))

        # 2b. DML
        subset_df = batch_df.filter(F.col("table") == tbl_name)

        try:
            subset_df.write.jdbc(
                url=jdbc_url,
                table=target_table,
                mode="append",
                properties=pg_properties
            )
            print(f"Inserted rows into {target_table}: {subset_df.count()}")
        except Exception as e:
            print(f"An error occurred while inserting into {target_table}:", e)
            import traceback
            traceback.print_exc()