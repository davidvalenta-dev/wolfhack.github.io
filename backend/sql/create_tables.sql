CREATE SCHEMA IF NOT EXISTS wolfhacks.pulsecast;

CREATE TABLE IF NOT EXISTS wolfhacks.pulsecast.demographics (
  subject_id STRING NOT NULL,
  hba1c DOUBLE NOT NULL,
  target INT NOT NULL,
  metabolic_class STRING NOT NULL
) USING DELTA;

CREATE TABLE IF NOT EXISTS wolfhacks.pulsecast.gold_risk (
  subject_id STRING NOT NULL,
  window_end TIMESTAMP NOT NULL,
  raw_probability DOUBLE,
  adjusted_probability DOUBLE,
  smoothed_probability DOUBLE,
  signal_confidence DOUBLE,
  velocity DOUBLE,
  trend STRING
) USING DELTA;
