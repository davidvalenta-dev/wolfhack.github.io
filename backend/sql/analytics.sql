SELECT
  subject_id,
  MAX_BY(smoothed_probability, window_end) AS latest_risk,
  MAX_BY(signal_confidence, window_end) AS latest_confidence,
  MAX_BY(trend, window_end) AS latest_trend
FROM wolfhacks.pulsecast.gold_risk
GROUP BY subject_id;

SELECT
  d.metabolic_class,
  AVG(r.smoothed_probability) AS mean_risk,
  PERCENTILE(r.smoothed_probability, 0.5) AS median_risk,
  AVG(r.signal_confidence) AS mean_confidence
FROM wolfhacks.pulsecast.gold_risk r
JOIN wolfhacks.pulsecast.demographics d USING(subject_id)
GROUP BY d.metabolic_class;
