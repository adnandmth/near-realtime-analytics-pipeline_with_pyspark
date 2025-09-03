from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType
from core.config import settings

def read_from_kafka(spark, kafka_bootstrap_servers, kafka_topic):
    """
    Kafka reader that parses only the outer JSON envelope.
    The 'record' field stays as raw JSON string (dynamic).
    """
    df_raw = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic) \
        .option("startingOffsets", settings.KAFKA_STARTING_OFFSETS) \
        .load()

    # Convert Kafka key/value to string
    df_kv = df_raw.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
    
    return df_kv