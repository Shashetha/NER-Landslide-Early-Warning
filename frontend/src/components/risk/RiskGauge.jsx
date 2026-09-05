import { getRiskColor } from '../../utils/riskUtils';
import styles from './RiskGauge.module.css';

const RiskGauge = ({ probability, riskLevel, size = 180 }) => {
  const percentage = Math.round(probability * 100);
  const color = getRiskColor(riskLevel);
  const strokeWidth = 12;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  return (
    <div className={styles.gaugeContainer} style={{ width: size, height: size }}>
      <svg className={styles.svg} width={size} height={size}>
        {/* Background circle */}
        <circle
          className={styles.backgroundCircle}
          stroke="#e2e8f0"
          strokeWidth={strokeWidth}
          fill="transparent"
          r={radius}
          cx={size / 2}
          cy={size / 2}
        />
        {/* Progress circle */}
        <circle
          className={styles.progressCircle}
          stroke={color}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          fill="transparent"
          r={radius}
          cx={size / 2}
          cy={size / 2}
        />
      </svg>
      <div className={styles.gaugeContent}>
        <span className={styles.percentage} style={{ color }}>{percentage}%</span>
        <span className={styles.label}>Probability</span>
      </div>
    </div>
  );
};

export default RiskGauge;
