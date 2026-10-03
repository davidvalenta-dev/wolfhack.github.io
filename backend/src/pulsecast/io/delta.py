from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TableNames:
    catalog: str
    schema: str

    @property
    def bronze_sensor(self) -> str:
        return f"{self.catalog}.{self.schema}.bronze_sensor"

    @property
    def silver_minute(self) -> str:
        return f"{self.catalog}.{self.schema}.silver_minute"

    @property
    def gold_features(self) -> str:
        return f"{self.catalog}.{self.schema}.gold_features"

    @property
    def gold_risk(self) -> str:
        return f"{self.catalog}.{self.schema}.gold_risk"

    @property
    def demographics(self) -> str:
        return f"{self.catalog}.{self.schema}.demographics"


class DeltaWriter:
    def __init__(self, spark: Any):
        self.spark = spark

    def overwrite(self, pdf, table_name: str) -> None:
        sdf = self.spark.createDataFrame(pdf)
        sdf.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(table_name)

    def append(self, pdf, table_name: str) -> None:
        sdf = self.spark.createDataFrame(pdf)
        sdf.write.mode("append").saveAsTable(table_name)
