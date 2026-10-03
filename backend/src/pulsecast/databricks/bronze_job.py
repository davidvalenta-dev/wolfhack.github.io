from __future__ import annotations

from pyspark.sql import functions as F, types as T
from pulsecast.config import get_settings
from pulsecast.io.delta import TableNames

s = get_settings()
t = TableNames(s.catalog, s.schema_name)
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {s.catalog}.{s.schema_name}")

schema = T.StructType([
    T.StructField("Timestamp", T.StringType()),
    T.StructField("Value", T.DoubleType()),
])

raw_path = f"{s.data_root}/*/HR_*.csv"
hr = (
    spark.read.format("csv")
    .option("header", "true")
    .schema(schema)
    .load(raw_path)
    .withColumn("timestamp", F.to_timestamp("Timestamp"))
    .withColumn("subject_id", F.regexp_extract(F.input_file_name(), r"HR_(\\d{3})\\.csv", 1))
    .withColumn("sensor", F.lit("hr"))
    .select("subject_id", "sensor", "timestamp", F.col("Value").alias("value"))
)
hr.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(t.bronze_sensor)
