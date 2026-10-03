from __future__ import annotations

from pyspark.sql import functions as F
from pulsecast.config import get_settings
from pulsecast.io.delta import TableNames

s = get_settings()
t = TableNames(s.catalog, s.schema_name)
bronze = spark.table(t.bronze_sensor)
silver = (
    bronze
    .filter(F.col("timestamp").isNotNull())
    .filter(F.col("value").isNotNull())
    .withColumn("minute", F.window("timestamp", "1 minute").getField("start"))
    .groupBy("subject_id", "sensor", "minute")
    .agg(
        F.avg("value").alias("mean_value"),
        F.stddev("value").alias("std_value"),
        F.min("value").alias("min_value"),
        F.max("value").alias("max_value"),
        F.count("value").alias("n"),
    )
)
silver.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(t.silver_minute)
