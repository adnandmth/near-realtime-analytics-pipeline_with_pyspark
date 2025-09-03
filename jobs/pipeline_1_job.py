import tempfile
from conf.spark_session import create_spark_session
from ingestion.kafka_reader import read_from_kafka
from sink.postgres_writer import write_to_postgres
from transform.column_utils import get_required_columns
from core.config import settings
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType

# Schema for the outer envelope
outer_schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("country", StringType(), True),
    StructField("service", StringType(), True),
    StructField("table", StringType(), True),
    StructField("event", StringType(), True),
    StructField("record", StringType(), True)  # keep dynamic JSON as string
])

def main():
    kafka_bootstrap_servers = settings.KAFKA_BROKERS 
    kafka_topic = settings.KAFKA_INPUT_TOPIC

    spark = create_spark_session()
    spark_log_level = settings.SPARK_LOG_LEVEL.upper()
    
    if spark_log_level:
      spark.sparkContext.setLogLevel(spark_log_level)
      print(f"✅ Spark log level set to: {spark_log_level}")

    df = read_from_kafka(spark, kafka_bootstrap_servers, kafka_topic)
    
    df_parsed = df.withColumn("parsed", from_json(col("value"), outer_schema))
    
     # Start both queries
    console_query = (
        df_parsed.select("parsed.*")
        .writeStream
        .format("console")
        .option("truncate", "false")
        .start()
    )

    postgres_query = (
        df_parsed.select("parsed.*")
        .writeStream
        .foreachBatch(lambda batch_df, batch_id: write_to_postgres(
            batch_df,
            batch_id
        ))
        .start()
    )

    # Wait for *either* to terminate
    spark.streams.awaitAnyTermination() 

if __name__ == "__main__":
    main()