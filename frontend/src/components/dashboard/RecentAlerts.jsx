import { Link } from 'react-router-dom';
import { ArrowRight, MapPin } from 'lucide-react';
import RiskBadge from '../risk/RiskBadge';
import { formatTimeAgo } from '../../utils/riskUtils';
import styles from './RecentAlerts.module.css';

const RecentAlerts = ({ alerts = [] }) => {
  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h3 className={styles.title}>Recent Risk Alerts</h3>
        <Link to="/alerts" className={styles.viewAll}>
          View All <ArrowRight size={14} />
        </Link>
      </div>

      <div className={styles.alertList}>
        {alerts.slice(0, 4).map((alert) => (
          <Link 
            key={alert.id} 
            to={`/location-analysis?lat=${alert.latitude}&lng=${alert.longitude}`}
            className={styles.alertItem}
          >
            <div className={styles.alertMain}>
              <div className={styles.locationRow}>
                <MapPin size={16} className={styles.pinIcon} />
                <span className={styles.locationName}>{alert.location}</span>
              </div>
              <span className={styles.timeAgo}>{formatTimeAgo(alert.timestamp)}</span>
            </div>
            <RiskBadge riskLevel={alert.riskLevel} size="small" />
          </Link>
        ))}
      </div>
    </div>
  );
};

export default RecentAlerts;
