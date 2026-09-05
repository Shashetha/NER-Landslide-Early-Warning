import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Bell, Filter, Search, MapPin, Users, Calendar } from 'lucide-react';
import PageHeader from '../components/layout/PageHeader';
import RiskBadge from '../components/risk/RiskBadge';
import Loader from '../components/common/Loader';
import { api } from '../services/api';
import { formatTimeAgo } from '../utils/riskUtils';
import styles from './Alerts.module.css';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('all');
  const [severityFilter, setSeverityFilter] = useState('all');
  const [search, setSearch] = useState('');

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const data = await api.getAlerts();
        setAlerts(data);
      } catch (err) {
        console.error('Failed to load alerts:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchAlerts();
  }, []);

  const filteredAlerts = alerts.filter((alert) => {
    const matchesStatus = statusFilter === 'all' || alert.status === statusFilter;
    const matchesSeverity = severityFilter === 'all' || alert.riskLevel === severityFilter;
    const matchesSearch = alert.location.toLowerCase().includes(search.toLowerCase()) ||
                          alert.description.toLowerCase().includes(search.toLowerCase());
    return matchesStatus && matchesSeverity && matchesSearch;
  });

  return (
    <div className={styles.container}>
      <PageHeader
        title="Emergency Hazard Alerts"
        subtitle="Live automated notifications triggered by high-risk environmental thresholds"
      />

      <div className={styles.filterCard}>
        <div className={styles.search}>
          <Search size={18} className={styles.searchIcon} />
          <input
            type="text"
            placeholder="Search alerts by location or trigger..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <div className={styles.filterGroup}>
          <div className={styles.filterItem}>
            <label>Status:</label>
            <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
              <option value="all">All Statuses</option>
              <option value="active">Active</option>
              <option value="resolved">Resolved</option>
            </select>
          </div>

          <div className={styles.filterItem}>
            <label>Severity:</label>
            <select value={severityFilter} onChange={(e) => setSeverityFilter(e.target.value)}>
              <option value="all">All Levels</option>
              <option value="CRITICAL">Critical</option>
              <option value="HIGH">High</option>
              <option value="MEDIUM">Medium</option>
              <option value="LOW">Low</option>
            </select>
          </div>
        </div>
      </div>

      {loading ? (
        <Loader text="Fetching system alerts..." />
      ) : filteredAlerts.length === 0 ? (
        <div className={styles.empty}>
          <Bell size={48} className={styles.emptyIcon} />
          <h3>No Alerts Found</h3>
          <p>There are no active or recorded alerts matching your current filter criteria.</p>
        </div>
      ) : (
        <div className={styles.alertsGrid}>
          {filteredAlerts.map((alert) => (
            <div key={alert.id} className={`${styles.alertCard} ${alert.status === 'resolved' ? styles.resolved : ''}`}>
              <div className={styles.cardHeader}>
                <div className={styles.locationMeta}>
                  <MapPin size={18} className={styles.pin} />
                  <h3>{alert.location}</h3>
                </div>
                <RiskBadge riskLevel={alert.riskLevel} />
              </div>

              <p className={styles.description}>{alert.description}</p>

              <div className={styles.metadata}>
                <div className={styles.metaItem}>
                  <Users size={16} />
                  <span>Pop. at Risk: ~{alert.affectedPopulation.toLocaleString()}</span>
                </div>
                <div className={styles.metaItem}>
                  <Calendar size={16} />
                  <span>{formatTimeAgo(alert.updatedAt)}</span>
                </div>
              </div>

              <div className={styles.cardFooter}>
                <span className={`${styles.statusBadge} ${styles[alert.status]}`}>
                  ● {alert.status.toUpperCase()}
                </span>
                <Link
                  to={`/location-analysis?lat=${alert.latitude}&lng=${alert.longitude}`}
                  className={styles.viewLink}
                >
                  Analyze Zone &rarr;
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Alerts;
