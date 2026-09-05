import { getRiskColor, getRiskClass } from '../../utils/riskUtils';
import styles from './RiskBadge.module.css';

const RiskBadge = ({ riskLevel, size = 'medium', showIcon = true }) => {
  const getIcon = () => {
    switch (riskLevel) {
      case 'LOW': return '●';
      case 'MEDIUM': return '▲';
      case 'HIGH': return '■';
      case 'CRITICAL': return '★';
      default: return '●';
    }
  };

  return (
    <span className={`${styles.badge} ${styles[riskLevel?.toLowerCase()]} ${styles[size]}`}>
      {showIcon && <span className={styles.icon}>{getIcon()}</span>}
      <span>{riskLevel} RISK</span>
    </span>
  );
};

export default RiskBadge;
