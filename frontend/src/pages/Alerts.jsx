import { useState, useEffect } from 'react';
import { 
  Bell, 
  MapPin, 
  Search, 
  ExternalLink,
  Eye,
  SlidersHorizontal,
  CheckCircle2,
  Clock,
  ShieldAlert,
  AlertTriangle,
  RotateCw
} from 'lucide-react';
import PageHeader from '../components/layout/PageHeader';
import RiskBadge from '../components/risk/RiskBadge';
import Modal from '../components/common/Modal';
import Button from '../components/common/Button';
import RiskMap from '../components/map/RiskMap';
import { api } from '../services/api';
import { formatTimeAgo } from '../utils/riskUtils';
import styles from './Alerts.module.css';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [riskFilter, setRiskFilter] = useState('all');
  const [selectedAlert, setSelectedAlert] = useState(null);

  const fetchAlerts = async () => {
    setLoading(true);
    try {
      const data = await api.getAlerts();
      setAlerts(data || []);
    } catch (error) {
      console.error('Failed to fetch alerts:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, []);

  const filteredAlerts = alerts.filter((alert) => {
    const matchesSearch = alert.location.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          alert.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === 'all' || alert.status === statusFilter;
    const matchesRisk = riskFilter === 'all' || alert.riskLevel.toLowerCase() === riskFilter.toLowerCase();
    return matchesSearch && matchesStatus && matchesRisk;
  });

  const criticalCount = alerts.filter(a => a.riskLevel === 'CRITICAL').length;
  const highCount = alerts.filter(a => a.riskLevel === 'HIGH').length;

  return (
    <div className={styles.container}>
      <PageHeader
        title="Emergency Warnings & Active Incident Alerts"
        subtitle="Automated early warning feeds triggered across North Eastern Region monitoring stations"
        action={
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <Button
              variant="secondary"
              icon={RotateCw}
              onClick={fetchAlerts}
              loading={loading}
            >
              Refresh Alerts
            </Button>
          </div>
        }
      />

      {/* Filter Tabs & Search Bar */}
      <div className={styles.filterCard}>
        <div className={styles.search}>
          <Search size={18} className={styles.searchIcon} />
          <input
            type="text"
            placeholder="Search alerts by location or details..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <div className={styles.filterGroup}>
          <div className={styles.filterItem}>
            <label>Severity Filter:</label>
            <select
              value={riskFilter}
              onChange={(e) => setRiskFilter(e.target.value)}
            >
              <option value="all">All Levels</option>
              <option value="critical">Critical ({criticalCount})</option>
              <option value="high">High ({highCount})</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>

          <div className={styles.filterItem}>
            <label>Status:</label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="all">All Statuses</option>
              <option value="active">Active (Evacuate)</option>
              <option value="monitoring">Monitoring</option>
              <option value="resolved">Resolved</option>
            </select>
          </div>
        </div>
      </div>

      {/* Alerts Grid */}
      <div className={styles.alertsGrid}>
        {filteredAlerts.map((alert) => (
          <div 
            key={alert.id} 
            className={`${styles.alertCard} ${alert.status === 'resolved' ? styles.resolved : ''}`}
            onClick={() => setSelectedAlert(alert)}
            style={{ cursor: 'pointer' }}
          >
            <div className={styles.cardHeader}>
              <div className={styles.locationMeta}>
                <MapPin size={18} className={styles.pin} />
                <h3>{alert.location}</h3>
              </div>
              <RiskBadge riskLevel={alert.riskLevel} size="small" />
            </div>

            <p className={styles.description}>{alert.description}</p>

            <div className={styles.metadata}>
              <div className={styles.metaItem}>
                <Clock size={14} />
                <span>Updated: {formatTimeAgo(alert.updatedAt)}</span>
              </div>
              <div className={styles.metaItem}>
                <span>Exposed Population: <strong>{alert.affectedPopulation?.toLocaleString() || 'N/A'}</strong></span>
              </div>
            </div>

            <div className={styles.cardFooter}>
              <span className={`${styles.statusBadge} ${styles[alert.status]}`}>
                {alert.status}
              </span>
              <span className={styles.viewLink} style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                <Eye size={14} /> View Location Map
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Alert Details & Coordinates Modal */}
      {selectedAlert && (
        <Modal
          isOpen={Boolean(selectedAlert)}
          onClose={() => setSelectedAlert(null)}
          title={`Alert Details: ${selectedAlert.location}`}
        >
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: '#f8fafc', padding: '1rem 1.25rem', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
              <div>
                <span style={{ fontSize: '0.75rem', fontWeight: '700', color: '#64748b', textTransform: 'uppercase' }}>Hazard Warning</span>
                <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#0f172a', marginTop: '0.1rem' }}>
                  {selectedAlert.location}
                </div>
              </div>
              <RiskBadge riskLevel={selectedAlert.riskLevel} size="large" />
            </div>

            <div style={{ height: '260px', borderRadius: '8px', overflow: 'hidden', border: '1px solid #cbd5e1' }}>
              <RiskMap
                key={`modal_alert_map_${selectedAlert.id}_${selectedAlert.latitude}_${selectedAlert.longitude}`}
                riskZones={[
                  {
                    id: selectedAlert.id,
                    name: selectedAlert.location,
                    latitude: selectedAlert.latitude,
                    longitude: selectedAlert.longitude,
                    riskLevel: selectedAlert.riskLevel,
                    probability: selectedAlert.probability,
                    radius: selectedAlert.riskLevel === 'CRITICAL' ? 3500 : 2000
                  }
                ]}
                center={[selectedAlert.latitude, selectedAlert.longitude]}
                zoom={10}
                height="260px"
                interactive={false}
              />
            </div>

            <p style={{ fontSize: '0.875rem', color: '#334155', lineHeight: '1.5', margin: 0 }}>
              {selectedAlert.description}
            </p>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '0.75rem', fontSize: '0.85rem' }}>
              <div style={{ padding: '0.75rem', background: '#f8fafc', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
                <span style={{ color: '#64748b', fontSize: '0.75rem', fontWeight: '600' }}>Coordinates:</span>
                <div style={{ fontWeight: '700', color: '#0f172a', marginTop: '0.1rem' }}>
                  {selectedAlert.latitude?.toFixed(4)}° N, {selectedAlert.longitude?.toFixed(4)}° E
                </div>
              </div>

              <div style={{ padding: '0.75rem', background: '#f8fafc', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
                <span style={{ color: '#64748b', fontSize: '0.75rem', fontWeight: '600' }}>Probability:</span>
                <div style={{ fontWeight: '800', color: selectedAlert.riskLevel === 'CRITICAL' ? '#b91c1c' : '#1d4ed8', marginTop: '0.1rem' }}>
                  {Math.round(selectedAlert.probability * 100)}% Threat Level
                </div>
              </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '0.5rem', paddingTop: '1rem', borderTop: '1px solid #e2e8f0' }}>
              <Button
                variant="secondary"
                onClick={() => setSelectedAlert(null)}
              >
                Close
              </Button>
              <Button
                variant="primary"
                icon={ExternalLink}
                onClick={() => {
                  window.location.href = `/location-analysis?lat=${selectedAlert.latitude}&lng=${selectedAlert.longitude}`;
                }}
              >
                Full Multi-Hazard Analysis
              </Button>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
};

export default Alerts;
