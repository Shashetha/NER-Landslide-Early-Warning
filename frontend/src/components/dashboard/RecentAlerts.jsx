import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, MapPin, Eye, ExternalLink } from 'lucide-react';
import RiskBadge from '../risk/RiskBadge';
import Modal from '../common/Modal';
import Button from '../common/Button';
import RiskMap from '../map/RiskMap';
import { formatTimeAgo } from '../../utils/riskUtils';
import styles from './RecentAlerts.module.css';

const RecentAlerts = ({ alerts = [] }) => {
  const [selectedAlert, setSelectedAlert] = useState(null);

  const handleOpenDetailModal = (e, alert) => {
    e.preventDefault();
    setSelectedAlert(alert);
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h3 className={styles.title}>Recent Risk Alerts</h3>
        <Link to="/alerts" className={styles.viewAll}>
          View All <ArrowRight size={14} />
        </Link>
      </div>

      <div className={styles.alertList}>
        {alerts.slice(0, 5).map((alert) => (
          <div 
            key={alert.id}
            className={styles.alertItem}
            onClick={(e) => handleOpenDetailModal(e, alert)}
            style={{ cursor: 'pointer' }}
          >
            <div className={styles.alertMain}>
              <div className={styles.locationRow}>
                <MapPin size={16} className={styles.pinIcon} />
                <span className={styles.locationName}>{alert.location}</span>
              </div>
              <span className={styles.timeAgo}>{formatTimeAgo(alert.timestamp)}</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
              <RiskBadge riskLevel={alert.riskLevel} size="small" />
              <Eye size={16} color="#64748b" />
            </div>
          </div>
        ))}
      </div>

      {/* Interactive Detail & Map Popup Modal */}
      {selectedAlert && (
        <Modal
          isOpen={Boolean(selectedAlert)}
          onClose={() => setSelectedAlert(null)}
          title={`Alert Details: ${selectedAlert.location}`}
        >
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            {/* Threat Badge & Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: '#f8fafc', padding: '1rem 1.25rem', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
              <div>
                <span style={{ fontSize: '0.75rem', fontWeight: '700', color: '#64748b', textTransform: 'uppercase' }}>Landslide Threat Level</span>
                <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#0f172a', marginTop: '0.1rem' }}>
                  {selectedAlert.location}
                </div>
              </div>
              <RiskBadge riskLevel={selectedAlert.riskLevel} size="large" />
            </div>

            {/* Centered Map on Exact Selected Coordinates */}
            <div style={{ height: '260px', borderRadius: '8px', overflow: 'hidden', border: '1px solid #cbd5e1' }}>
              <RiskMap
                key={`modal_map_${selectedAlert.id}_${selectedAlert.latitude}_${selectedAlert.longitude}`}
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

            {/* GPS & Probability Info Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '0.75rem', fontSize: '0.85rem' }}>
              <div style={{ padding: '0.75rem', background: '#f8fafc', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
                <span style={{ color: '#64748b', fontSize: '0.75rem', fontWeight: '600' }}>GPS Coordinates:</span>
                <div style={{ fontWeight: '700', color: '#0f172a', marginTop: '0.1rem' }}>
                  {selectedAlert.latitude?.toFixed(4)}° N, {selectedAlert.longitude?.toFixed(4)}° E
                </div>
              </div>

              <div style={{ padding: '0.75rem', background: '#f8fafc', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
                <span style={{ color: '#64748b', fontSize: '0.75rem', fontWeight: '600' }}>Model Probability:</span>
                <div style={{ fontWeight: '800', color: selectedAlert.riskLevel === 'CRITICAL' ? '#b91c1c' : '#1d4ed8', marginTop: '0.1rem' }}>
                  {Math.round(selectedAlert.probability * 100)}% Landslide Risk
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '0.5rem', paddingTop: '1rem', borderTop: '1px solid #e2e8f0' }}>
              <Button
                variant="secondary"
                onClick={() => setSelectedAlert(null)}
              >
                Close
              </Button>
              <Link to={`/location-analysis?lat=${selectedAlert.latitude}&lng=${selectedAlert.longitude}`}>
                <Button
                  variant="primary"
                  icon={ExternalLink}
                >
                  Open Full AI Telemetry & Multi-Hazard Forecast
                </Button>
              </Link>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
};

export default RecentAlerts;
