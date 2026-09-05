import { Droplets, Mountain, ArrowUpRight, Compass, Thermometer } from 'lucide-react';
import RiskBadge from './RiskBadge';
import RiskGauge from './RiskGauge';
import styles from './RiskCard.module.css';

const RiskCard = ({ prediction, loading }) => {
  if (loading) {
    return (
      <div className={styles.card}>
        <div className={styles.loadingContainer}>
          <div className={styles.spinner}></div>
          <p>Analyzing terrain & environmental factors...</p>
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

  const { riskLevel, probability, features, explanation, confidence } = prediction;

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
          <div className={styles.confidenceBadge}>
            <span>Confidence: {Math.round(confidence * 100)}%</span>
          </div>
        </div>

        <div className={styles.featuresGrid}>
          <div className={styles.featureItem}>
            <div className={styles.featureIcon}>
              <Droplets size={20} />
            </div>
            <div className={styles.featureInfo}>
              <span className={styles.featureLabel}>Rainfall</span>
              <span className={styles.featureValue}>{features.rainfall} mm</span>
            </div>
          </div>

          <div className={styles.featureItem}>
            <div className={styles.featureIcon}>
              <ArrowUpRight size={20} />
            </div>
            <div className={styles.featureInfo}>
              <span className={styles.featureLabel}>Slope Angle</span>
              <span className={styles.featureValue}>{features.slope}°</span>
            </div>
          </div>

          <div className={styles.featureItem}>
            <div className={styles.featureIcon}>
              <Mountain size={20} />
            </div>
            <div className={styles.featureInfo}>
              <span className={styles.featureLabel}>Elevation</span>
              <span className={styles.featureValue}>{features.elevation} m</span>
            </div>
          </div>

          <div className={styles.featureItem}>
            <div className={styles.featureIcon}>
              <Compass size={20} />
            </div>
            <div className={styles.featureInfo}>
              <span className={styles.featureLabel}>Soil Moisture</span>
              <span className={styles.featureValue}>{features.soilMoisture}%</span>
            </div>
          </div>

          <div className={styles.featureItem}>
            <div className={styles.featureIcon}>
              <Thermometer size={20} />
            </div>
            <div className={styles.featureInfo}>
              <span className={styles.featureLabel}>Temperature</span>
              <span className={styles.featureValue}>{features.temperature}°C</span>
            </div>
          </div>
        </div>
      </div>

      {explanation && (
        <div className={styles.explanationSection}>
          <h4>Why is this location at risk?</h4>
          <p>{explanation}</p>
        </div>
      )}
    </div>
  );
};

export default RiskCard;
