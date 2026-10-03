from __future__ import annotations


def create_agent_sql_functions(spark, catalog: str, schema: str) -> None:
    spark.sql(f"""
    CREATE OR REPLACE FUNCTION {catalog}.{schema}.latest_subject_risk(subject STRING)
    RETURNS TABLE(subject_id STRING, window_end TIMESTAMP, risk DOUBLE, confidence DOUBLE, trend STRING)
    RETURN
      SELECT subject_id, window_end, smoothed_probability, signal_confidence, trend
      FROM {catalog}.{schema}.gold_risk
      WHERE subject_id = subject
      QUALIFY ROW_NUMBER() OVER (ORDER BY window_end DESC) = 1
    """)
    spark.sql(f"""
    CREATE OR REPLACE FUNCTION {catalog}.{schema}.subject_risk_history(subject STRING, n INT)
    RETURNS TABLE(subject_id STRING, window_end TIMESTAMP, risk DOUBLE, confidence DOUBLE, trend STRING)
    RETURN
      SELECT subject_id, window_end, smoothed_probability, signal_confidence, trend
      FROM {catalog}.{schema}.gold_risk
      WHERE subject_id = subject
      ORDER BY window_end DESC
      LIMIT n
    """)
