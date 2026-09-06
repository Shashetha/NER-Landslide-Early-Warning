import { Droplets, Mountain, ArrowUpRight, Compass, CalendarDays, Activity } from 'lucide-react';
import RiskBadge from './RiskBadge';
import RiskGauge from './RiskGauge';
import styles from './RiskCard.module.css';

const RiskCard = ({ prediction, loading }) => {
  if (loading) {
    return (
      <div className={styles.card}>
        <div className={styles.loadingContainer}>
          <div className={styles.spinner}></div>
          <p>Analyzing terrain &amp; environmental factors...</p>
        </div>
      </div>
    );
  }

  if (!prediction) {
    return (
      <div className={styles.card}>
        <div className={styles.emptyState}>
          <Mountain size={48} className={styles.emptyIcon} />
          <h3>No Location Selected</h3>
          <p>Click anywhere on the map or use your current location to analyze landslide risk.</p>
        </div>
      </div>
    );
  }

  const { riskLevel, probability, features = {}, explanation, confidence, modelName } = prediction;

  const fmt = (v, decimals = 1) =>
    v != null && !isNaN(v) ? Number(v).toFixed(decimals) : '—';

  // Soil moisture is fraction (0.0 - 1.0) -> display as percentage (e.g. 35.2%)
  const soilMoisturePct =
    features.soilMoisture != null && !isNaN(features.soilMoisture)
      ? (features.soilMoisture <= 1.0 ? features.soilMoisture * 100 : features.soilMoisture)
      : null;

  const confidencePct =
    confidence != null && !isNaN(confidence) ? Math.round(confidence * 100) : null;

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <div>
          <span className={styles.subtitle}>Risk Assessment Result</span>
          <h2 className={styles.title}>Landslide Threat Level</h2>
        </div>
        <RiskBadge riskLevel={riskLevel} size="large" />
      </div>

      <div className={styles.mainGrid}>
        <div className={styles.gaugeSection}>
          <RiskGauge probability={probability} riskLevel={riskLevel} size={160} />
          {confidencePct != null && (
            <div className={styles.confidenceBadge}>
              <span>Confidence: {confidencePct}%</span>
            </div>
          )}
          {modelName && (
            <div className={styles.confidenceBadge} style={{ marginTop: '0.25rem', fontSize: '0.7rem' }}>
              <span>{modelName}</span>
            </div>
          )}
        </div>

        <div className={styles.featuresGrid}>
          <div className={styles.featureItem}>
            <div className={styles.featureIcon}>
              <Droplets size={20} />
            </div>
            <div className={styles.featureInfo}>
              <span className={styles.featureLabel}>Rainfall (1-day)</span>
              <span className={styles.featureValue}>{fmt(features.rainfall1d)} mm</span>
            </div>
          </div>

          <div className={styles.featureItem}>
            <div className={styles.featureIcon}>
              <CalendarDays size={20} />
            </div>
            <div className={styles.featureInfo}>
              <span className={styles.featureLabel}>Rainfall (7-day)</span>
              <span className={styles.featureValue}>{fmt(features.rainfall7d)} mm</span>
            </div>
          </div>

          <div className={styles.featureItem}>
            <div className={styles.featureIcon}>
              <ArrowUpRight size={20} />
            </div>
            <div className={styles.featureInfo}>
              <span className={styles.featureLabel}>Slope Angle</span>
              <span className={styles.featureValue}>{fmt(features.slopeDegrees)}°</span>
            </div>
          </div>

          <div className={styles.featureItem}>
            <div className={styles.featureIcon}>
              <Mountain size={20} />
            </div>
            <div className={styles.featureInfo}>
              <span className={styles.featureLabel}>Elevation</span>
              <span className={styles.featureValue}>{fmt(features.elevationM, 0)} m</span>
            </div>
          </div>

          <div className={styles.featureItem}>
            <div className={styles.featureIcon}>
              <Compass size={20} />
            </div>
            <div className={styles.featureInfo}>
              <span className={styles.featureLabel}>Soil Moisture</span>
              <span className={styles.featureValue}>{fmt(soilMoisturePct, 1)}%</span>
            </div>
          </div>

          <div className={styles.featureItem}>
            <div className={styles.featureIcon}>
              <Activity size={20} />
            </div>
            <div className={styles.featureInfo}>
              <span className={styles.featureLabel}>Rainfall (3-day)</span>
              <span className={styles.featureValue}>{fmt(features.rainfall3d)} mm</span>
            </div>
          </div>
        </div>
      </div>

      {explanation && (
        <div className={styles.explanationSection}>
          <h4>Risk Assessment Summary</h4>
          <p>{explanation}</p>
        </div>
      )}
    </div>
  );
};

export default RiskCard;
