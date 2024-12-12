from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

def main():
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("KafkaToPostgres") \
        .getOrCreate()

    # Kafka parameters
    kafka_bootstrap_servers = "broker:29092"  # Kafka broker address
    kafka_topic = "your_kafka_topic"  # Kafka topic

    # PostgreSQL connection details
    postgres_url = "jdbc:postgresql://your_postgres_host:5432/your_database"
    postgres_properties = {
        "user": "your_username",
        "password": "your_password",
        "driver": "org.postgresql.Driver"
    }
    postgres_table = "your_table"  # The table to write to in PostgreSQL

    # Read data from Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic) \
        .load()

    # The data read from Kafka is in binary format, so let's cast it to string
    df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

    # Example transformation - you can replace this with your own logic
    df_transformed = df.withColumn("processed_value", expr("value"))  # Modify as per your data processing logic

    # Write data to PostgreSQL
    query = df_transformed.writeStream \
        .foreachBatch(lambda batch_df, batch_id: batch_df.write.jdbc(
            url=postgres_url,
            table=postgres_table,
            mode="append",  # You can also use "overwrite" based on your use case
            properties=postgres_properties
        )) \
        .outputMode("append") \
        .start()

    query.awaitTermination()


if __name__ == "__main__":
    main()
