from pyspark.sql import SparkSession
from core.config import settings

def create_spark_session(app_name="SparkDataPipeline"):
    """
    Initialize and return a SparkSession.
    """
    spark = SparkSession.builder \
        .appName(settings.APP_NAME) \
        .config("spark.jars", ",".join(settings.SPARK_PACKAGES)) \
        .getOrCreate()
        
    return spark
