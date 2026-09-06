import { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { Menu, Bell, AlertTriangle, CheckCircle2, ArrowRight } from 'lucide-react';
import styles from './Topbar.module.css';
import { api } from '../../services/api';

const Topbar = ({ onMenuClick, title = 'Landslide Early Warning Platform' }) => {
  const [showNotifications, setShowNotifications] = useState(false);
  const [alerts, setAlerts] = useState([]);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowNotifications(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    const loadAlerts = async () => {
      try {
        const data = await api.getAlerts();
        setAlerts(data || []);
      } catch (e) {
        console.warn('Could not fetch topbar alerts');
      }
    };
    loadAlerts();
    const interval = setInterval(loadAlerts, 10000);
    return () => clearInterval(interval);
  }, []);

  const activeAlerts = alerts.filter(a => a.status === 'active' || a.riskLevel === 'CRITICAL' || a.riskLevel === 'HIGH');

  return (
    <header className={styles.topbar}>
      <div className={styles.topbarLeft}>
        <button className={styles.menuButton} onClick={onMenuClick} aria-label="Toggle navigation menu">
          <Menu size={20} />
        </button>
        <h1 className={styles.topbarTitle}>{title}</h1>
      </div>

      <div className={styles.topbarRight} ref={dropdownRef}>
        <button 
          className={`${styles.topbarButton} ${showNotifications ? styles.active : ''}`} 
          aria-label="Notifications"
          onClick={() => setShowNotifications(!showNotifications)}
        >
          <Bell size={19} />
          {activeAlerts.length > 0 && (
            <span className={styles.notificationBadge}>{activeAlerts.length}</span>
          )}
        </button>

        {showNotifications && (
          <div className={styles.notificationDropdown}>
            <div className={styles.dropdownHeader}>
              <div>
                <h3>Emergency Notifications & Active Warnings</h3>
                <p>{activeAlerts.length} active high/critical threats across NER</p>
              </div>
            </div>

            <div className={styles.notificationList}>
              {activeAlerts.length === 0 ? (
                <div className={styles.emptyNotifications}>
                  <CheckCircle2 size={24} className={styles.emptyIcon} />
                  <p>All monitored NER stations are currently in stable status.</p>
                </div>
              ) : (
                activeAlerts.slice(0, 6).map((alert) => (
                  <Link 
                    key={alert.id}
                    to={`/location-analysis?lat=${alert.latitude}&lng=${alert.longitude}`}
                    className={`${styles.notificationItem} ${alert.riskLevel === 'CRITICAL' ? styles.unread : ''}`}
                    onClick={() => setShowNotifications(false)}
                  >
                    <div className={`${styles.alertIndicator} ${styles[alert.riskLevel.toLowerCase()] || styles.high}`}>
                      <AlertTriangle size={16} />
                    </div>
                    <div className={styles.notificationContent}>
                      <div className={styles.notificationTitleRow}>
                        <span className={styles.alertLocation}>{alert.location}</span>
                        <span style={{ fontSize: '0.7rem', color: '#64748b' }}>Live</span>
                      </div>
                      <p className={styles.alertDesc}>{alert.description}</p>
                      <span className={`${styles.riskTag} ${styles[alert.riskLevel.toLowerCase()] || styles.high}`}>
                        {alert.riskLevel} ({Math.round((alert.probability || 0.8) * 100)}%)
                      </span>
                    </div>
                  </Link>
                ))
              )}
            </div>

            <div className={styles.dropdownFooter}>
              <Link to="/alerts" onClick={() => setShowNotifications(false)}>
                View All Alert Warnings <ArrowRight size={14} />
              </Link>
            </div>
          </div>
        )}

        <div className={styles.userAvatar} title="Lead Disaster Response Commander">
          RC
        </div>
      </div>
    </header>
  );
};

export default Topbar;
