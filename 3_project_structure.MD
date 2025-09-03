pyspark_streaming_pipeline/
│
├── config/
│   └── spark_config.py               # SparkSession setup
|   └── configuration.py              # Pydantic config setup
|
├── core/
│   ├── config.py                     # Pydantic config setup
│   └── database.py                   # Database connections
│
├── ingestion/
│   └── kafka_reader.py               # Reads from Kafka topics
|
├── kafka_utils/
│   └── kafka_client.py               # Kafka broker producer setup
|
├── sink/
│   ├── bigquery_writer.py            # Sink to BigQuery
│   ├── clickhouse_writer.py          # Sink to ClickHouse
│   └── postgres_writer.py            # Optional intermediate storage
│
├── transform/
│   ├── base_transformer.py           # Shared transformation logic
│   ├── data/
│   │   ├── fraud_model.py            
│   │   ├── recommendation_model.py   
│   │   └── segmentation_model.py     
│   └── column_utils.py                # Pre-defined schema
│                    
└── jobs/
    ├── pipeline_1_job.py             # Main app driver             