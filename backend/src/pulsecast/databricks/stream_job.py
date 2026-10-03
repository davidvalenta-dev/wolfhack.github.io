from __future__ import annotations

from pyspark.sql import functions as F
from pulsecast.config import get_settings
from pulsecast.io.delta import TableNames

s = get_settings()
t = TableNames(s.catalog, s.schema_name)
source = spark.readStream.table(t.bronze_sensor)
minute = (
    source
    .withWatermark("timestamp", "2 minutes")
    .groupBy("subject_id", "sensor", F.window("timestamp", "1 minute"))
    .agg(F.avg("value").alias("mean_value"), F.stddev("value").alias("std_value"))
    .select("subject_id", "sensor", F.col("window.start").alias("minute"), "mean_value", "std_value")
)
query = (
    minute.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", f"{s.artifact_root}/checkpoints/minute")
    .toTable(t.silver_minute)
)
query.awaitTermination()
