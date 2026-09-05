import { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { Menu, Bell, X, AlertTriangle, Info, CheckCircle2, ArrowRight } from 'lucide-react';
import styles from './Topbar.module.css';
import { mockAlerts } from '../../data/mockData';
import { formatTimeAgo } from '../../utils/riskUtils';

const Topbar = ({ onMenuClick, title = 'Landslide Early Warning System' }) => {
  const [showNotifications, setShowNotifications] = useState(false);
  const [notifications, setNotifications] = useState(mockAlerts);
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

  const unreadCount = notifications.filter(n => n.status === 'active').length;

  const markAllAsRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, status: 'read' })));
  };

  return (
    <header className={styles.topbar}>
      <div className={styles.topbarLeft}>
        <button className={styles.menuButton} onClick={onMenuClick} aria-label="Toggle menu">
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
          <Bell size={20} />
          {unreadCount > 0 && <span className={styles.notificationBadge}>{unreadCount}</span>}
        </button>

        {showNotifications && (
          <div className={styles.notificationDropdown}>
            <div className={styles.dropdownHeader}>
              <div>
                <h3>Notifications & Alerts</h3>
                <p>{unreadCount} active warnings</p>
              </div>
              {unreadCount > 0 && (
                <button className={styles.markReadBtn} onClick={markAllAsRead}>
                  Mark all read
                </button>
              )}
            </div>

            <div className={styles.notificationList}>
              {notifications.length === 0 ? (
                <div className={styles.emptyNotifications}>
                  <CheckCircle2 size={24} className={styles.emptyIcon} />
                  <p>All clear! No active alerts right now.</p>
                </div>
              ) : (
                notifications.map((alert) => (
                  <Link 
                    key={alert.id}
                    to={`/location-analysis?lat=${alert.latitude}&lng=${alert.longitude}`}
                    className={`${styles.notificationItem} ${alert.status === 'active' ? styles.unread : ''}`}
                    onClick={() => setShowNotifications(false)}
                  >
                    <div className={`${styles.alertIndicator} ${styles[alert.riskLevel.toLowerCase()]}`}>
                      <AlertTriangle size={16} />
                    </div>
                    <div className={styles.notificationContent}>
                      <div className={styles.notificationTitleRow}>
                        <span className={styles.alertLocation}>{alert.location}</span>
                        <span className={styles.alertTime}>{formatTimeAgo(alert.updatedAt)}</span>
                      </div>
                      <p className={styles.alertDesc}>{alert.description}</p>
                      <span className={`${styles.riskTag} ${styles[alert.riskLevel.toLowerCase()]}`}>
                        {alert.riskLevel} RISK ({Math.round(alert.probability * 100)}%)
                      </span>
                    </div>
                  </Link>
                ))
              )}
            </div>

            <div className={styles.dropdownFooter}>
              <Link to="/alerts" onClick={() => setShowNotifications(false)}>
                View All Alert History <ArrowRight size={14} />
              </Link>
            </div>
          </div>
        )}

        <div className={styles.userAvatar} title="Disaster Monitoring Officer">
          DO
        </div>
      </div>
    </header>
  );
};

export default Topbar;
