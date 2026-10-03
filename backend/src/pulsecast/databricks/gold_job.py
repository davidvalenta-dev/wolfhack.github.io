from __future__ import annotations

from pyspark.sql import Window, functions as F
from pulsecast.config import get_settings
from pulsecast.io.delta import TableNames

s = get_settings()
t = TableNames(s.catalog, s.schema_name)
silver = spark.table(t.silver_minute).filter(F.col("sensor") == "hr")
seconds = s.window_minutes * 60
w = Window.partitionBy("subject_id").orderBy(F.col("minute").cast("long")).rangeBetween(-seconds, 0)
gold = (
    silver
    .withColumn("hr_mean_15m", F.avg("mean_value").over(w))
    .withColumn("hr_std_15m", F.stddev("mean_value").over(w))
    .withColumn("hr_min_15m", F.min("min_value").over(w))
    .withColumn("hr_max_15m", F.max("max_value").over(w))
    .withColumn("window_samples", F.sum("n").over(w))
)
gold.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(t.gold_features)
