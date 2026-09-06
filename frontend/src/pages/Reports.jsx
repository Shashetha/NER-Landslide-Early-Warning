import { useState, useEffect } from 'react';
import { 
  FileText, 
  Plus, 
  MapPin, 
  Calendar, 
  AlertCircle, 
  Wifi, 
  WifiOff, 
  RefreshCw, 
  Camera, 
  UploadCloud,
  CheckCircle2,
  Clock,
  Trash2,
  CheckCircle,
  X,
  AlertTriangle
} from 'lucide-react';
import PageHeader from '../components/layout/PageHeader';
import Button from '../components/common/Button';
import Modal from '../components/common/Modal';
import { api } from '../services/api';
import { offlineStorage } from '../services/offlineStorage';
import styles from './Reports.module.css';

const Reports = () => {
  const [reports, setReports] = useState([]);
  const [pendingSync, setPendingSync] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [syncingOffline, setSyncingOffline] = useState(false);
  const [selectedPhoto, setSelectedPhoto] = useState(null);

  const [currentUser, setCurrentUser] = useState(null);
  
  // In-Website Toast Popup
  const [statusPopup, setStatusPopup] = useState(null);

  const showInWebsitePopup = (type, title, message) => {
    setStatusPopup({ type, title, message });
    setTimeout(() => {
      setStatusPopup(null);
    }, 5000);
  };

  const [formData, setFormData] = useState({
    location: '',
    state: 'Sikkim',
    district: '',
    latitude: '',
    longitude: '',
    hazardType: 'landslide',
    severity: 'high',
    description: '',
    visible_cracks: false,
    rockfall_observed: false,
    road_blocked: false,
    water_accumulation: false,
    soil_movement: false,
    contactInfo: '',
  });

  useEffect(() => {
    const cachedUser = localStorage.getItem('auth_user');
    if (cachedUser) {
      try {
        const u = JSON.parse(cachedUser);
        setCurrentUser(u);
        setFormData(prev => ({
          ...prev,
          state: u.state || 'Sikkim',
          district: u.district || '',
          contactInfo: u.phone_number || u.email || ''
        }));
      } catch (e) {}
    }
  }, []);

  const loadReports = async () => {
    setLoading(true);
    try {
      const data = await api.getReports();
      setReports(data || []);
    } catch (e) {
      console.warn('Network offline or error fetching live reports');
    } finally {
      setLoading(false);
    }
  };

  const loadPendingOffline = async () => {
    try {
      const offlineList = await offlineStorage.getPendingReports();
      setPendingSync(offlineList);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadReports();
    loadPendingOffline();

    const handleOnline = () => {
      setIsOnline(true);
      syncPendingReports();
    };
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    const interval = setInterval(loadReports, 8000);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
      clearInterval(interval);
    };
  }, []);

  const syncPendingReports = async () => {
    setSyncingOffline(true);
    try {
      const offlineList = await offlineStorage.getPendingReports();
      let syncedCount = 0;
      for (const item of offlineList) {
        try {
          await api.submitHazardReport(item);
          await offlineStorage.removeReport(item.idempotency_key);
          syncedCount++;
        } catch (err) {
          console.error('Failed to sync item:', item, err);
        }
      }
      await loadPendingOffline();
      await loadReports();
      if (syncedCount > 0) {
        showInWebsitePopup('success', 'Offline Reports Synchronized', `${syncedCount} report(s) pushed to emergency response database.`);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setSyncingOffline(false);
    }
  };

  const handleDeleteReport = async (reportId) => {
    try {
      await api.deleteReport(reportId);
      await loadReports();
      showInWebsitePopup('success', 'Report Removed', `Field report record ${reportId} deleted.`);
    } catch (err) {
      showInWebsitePopup('error', 'Delete Error', err.message);
    }
  };

  const handleGetCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setFormData(prev => ({
            ...prev,
            latitude: pos.coords.latitude.toFixed(6),
            longitude: pos.coords.longitude.toFixed(6),
          }));
          showInWebsitePopup('success', 'GPS Location Acquired', `${pos.coords.latitude.toFixed(4)}° N, ${pos.coords.longitude.toFixed(4)}° E`);
        },
        (err) => showInWebsitePopup('error', 'GPS Error', 'Please grant location permission in your browser.')
      );
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const reportPayload = {
        ...formData,
        reporter_name: currentUser?.full_name || 'Ground Observer',
        contactInfo: formData.contactInfo || currentUser?.phone_number || '',
        latitude: parseFloat(formData.latitude),
        longitude: parseFloat(formData.longitude),
        idempotency_key: `report_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`,
      };

      if (!navigator.onLine) {
        await offlineStorage.saveReport(reportPayload);
        await loadPendingOffline();
        setIsModalOpen(false);
        showInWebsitePopup('success', 'Offline Report Saved', 'Ground report saved safely to device storage. It will auto-sync upon reconnection.');
      } else {
        await api.submitHazardReport(reportPayload);
        setIsModalOpen(false);
        await loadReports();
        showInWebsitePopup('success', 'Ground Report Registered', 'Hazard report submitted and dispatched to regional disaster management team.');
      }

      setFormData({
        location: '',
        state: currentUser?.state || 'Sikkim',
        district: currentUser?.district || '',
        latitude: '',
        longitude: '',
        hazardType: 'landslide',
        severity: 'high',
        description: '',
        visible_cracks: false,
        rockfall_observed: false,
        road_blocked: false,
        water_accumulation: false,
        soil_movement: false,
        contactInfo: currentUser?.phone_number || '',
      });
      setSelectedPhoto(null);
    } catch (err) {
      await offlineStorage.saveReport(formData);
      await loadPendingOffline();
      setIsModalOpen(false);
      showInWebsitePopup('success', 'Cached to Device', 'Report stored safely in local offline cache.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className={styles.container}>
      {/* In-Website Toast Popup */}
      {statusPopup && (
        <div style={{
          position: 'fixed',
          top: '5rem',
          right: '2rem',
          zIndex: 9999,
          background: statusPopup.type === 'error' ? '#7f1d1d' : '#064e3b',
          color: '#ffffff',
          borderRadius: '8px',
          padding: '1.25rem 1.5rem',
          maxWidth: '440px',
          boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.3)',
          border: `2px solid ${statusPopup.type === 'error' ? '#dc2626' : '#10b981'}`,
          display: 'flex',
          flexDirection: 'column',
          gap: '0.4rem',
          animation: 'slideIn 0.25s cubic-bezier(0.16, 1, 0.3, 1)'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: '800', fontSize: '0.9rem' }}>
              {statusPopup.type === 'error' ? <AlertTriangle size={18} color="#fca5a5" /> : <CheckCircle size={18} color="#6ee7b7" />}
              <span>{statusPopup.title}</span>
            </div>
            <button 
              onClick={() => setStatusPopup(null)} 
              style={{ background: 'none', border: 'none', color: '#ffffff', cursor: 'pointer', padding: '0.2rem' }}
            >
              <X size={16} />
            </button>
          </div>
          <p style={{ fontSize: '0.825rem', color: statusPopup.type === 'error' ? '#fecaca' : '#d1fae5', margin: 0, lineHeight: '1.45' }}>
            {statusPopup.message}
          </p>
        </div>
      )}

      <PageHeader
        title="Field & Ground Hazard Reporting"
        subtitle="Submit ground observations, slope movements, and infrastructure road blocks for emergency dispatch"
        action={
          <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center', flexWrap: 'wrap' }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.45rem',
              padding: '0.45rem 0.85rem',
              borderRadius: '6px',
              fontSize: '0.8rem',
              fontWeight: '800',
              background: isOnline ? '#ecfdf5' : '#fffbeb',
              color: isOnline ? '#047857' : '#b45309',
              border: '1px solid',
              borderColor: isOnline ? '#a7f3d0' : '#fde68a'
            }}>
              {isOnline ? <Wifi size={15} /> : <WifiOff size={15} />}
              <span>{isOnline ? '🟢 Live Connected' : `🟠 Offline (${pendingSync.length} Pending Sync)`}</span>
            </div>

            {pendingSync.length > 0 && (
              <Button
                variant="secondary"
                icon={RefreshCw}
                onClick={syncPendingReports}
                loading={syncingOffline}
              >
                Sync Offline ({pendingSync.length})
              </Button>
            )}

            <Button
              variant="primary"
              icon={Plus}
              onClick={() => setIsModalOpen(true)}
            >
              Submit Hazard Report
            </Button>
          </div>
        }
      />

      {/* Pending Offline Banner */}
      {pendingSync.length > 0 && (
        <div style={{ padding: '1rem 1.25rem', background: '#fffbeb', border: '1px solid #fde68a', borderRadius: '8px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', color: '#92400e', fontSize: '0.85rem', fontWeight: '700' }}>
            <AlertCircle size={20} color="#b45309" />
            <span>{pendingSync.length} report(s) safely stored on device storage (IndexedDB). They will automatically push to the emergency command server upon connection.</span>
          </div>
          <Button variant="secondary" size="small" onClick={syncPendingReports} loading={syncingOffline}>
            Sync Now
          </Button>
        </div>
      )}

      {/* Reports Grid */}
      <div className={styles.reportsGrid}>
        {reports.length === 0 ? (
          <div style={{ gridColumn: '1 / -1', background: '#ffffff', border: '1px solid #cbd5e1', borderRadius: '8px', padding: '3.5rem 1.5rem', textAlign: 'center', color: '#64748b' }}>
            <FileText size={36} color="#94a3b8" style={{ marginBottom: '0.75rem' }} />
            <h3 style={{ fontSize: '1.1rem', color: '#0f172a', fontWeight: '800' }}>No Ground Reports Filed Yet</h3>
            <p style={{ fontSize: '0.875rem', marginTop: '0.25rem' }}>Submit a field incident or road blockage report using the button above.</p>
          </div>
        ) : (
          reports.map((report) => (
            <div key={report.id} className={styles.reportCard}>
              <div className={styles.cardHeader}>
                <div className={styles.locationMeta}>
                  <MapPin size={18} className={styles.pin} />
                  <h3>{report.location}</h3>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span className={`${styles.severityBadge} ${styles[report.severity]}`}>
                    {report.severity}
                  </span>
                  <button
                    onClick={() => handleDeleteReport(report.id)}
                    title="Delete this report"
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#94a3b8',
                      cursor: 'pointer',
                      padding: '0.25rem',
                      display: 'flex',
                      alignItems: 'center',
                      borderRadius: '4px',
                      transition: 'color 0.15s, background 0.15s'
                    }}
                    onMouseEnter={(e) => { e.currentTarget.style.color = '#dc2626'; e.currentTarget.style.background = '#fee2e2'; }}
                    onMouseLeave={(e) => { e.currentTarget.style.color = '#94a3b8'; e.currentTarget.style.background = 'none'; }}
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', marginTop: '0.2rem' }}>
                <span className={styles.hazardType} style={{ fontWeight: '800' }}>
                  Type: {report.hazard_type}
                </span>
                <span style={{ fontSize: '0.75rem', padding: '0.15rem 0.5rem', borderRadius: '4px', background: '#eff6ff', color: '#1d4ed8', fontWeight: '800' }}>
                  {report.status}
                </span>
              </div>

              <p className={styles.description}>{report.description}</p>

              <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', fontSize: '0.75rem', color: '#475569' }}>
                {report.visible_cracks && <span>⚠️ Cracks</span>}
                {report.rockfall_observed && <span>🪨 Rockfall</span>}
                {report.road_blocked && <span>🚫 Road Blocked</span>}
                {report.water_accumulation && <span>💧 Saturated</span>}
              </div>

              <div className={styles.footer}>
                <div className={styles.metaItem}>
                  <Calendar size={14} />
                  <span>{new Date(report.created_at).toLocaleDateString()}</span>
                </div>
                <span className={styles.statusBadge}>
                  {report.reporter_name || 'Ground Observer'}
                </span>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Modal Form */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Submit Ground Hazard & Incident Report"
      >
        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.formGroup}>
            <label>Location / Landmark Landmark *</label>
            <input
              type="text"
              required
              placeholder="e.g. NH-10 Highway Mile 24, Gangtok Corridor"
              value={formData.location}
              onChange={(e) => setFormData({ ...formData, location: e.target.value })}
            />
          </div>

          <div className={styles.formRow}>
            <div className={styles.formGroup}>
              <label>State Jurisdiction *</label>
              <select
                value={formData.state}
                onChange={(e) => setFormData({ ...formData, state: e.target.value })}
              >
                <option value="Sikkim">Sikkim</option>
                <option value="Meghalaya">Meghalaya</option>
                <option value="Arunachal Pradesh">Arunachal Pradesh</option>
                <option value="Nagaland">Nagaland</option>
                <option value="Manipur">Manipur</option>
                <option value="Mizoram">Mizoram</option>
                <option value="Assam">Assam</option>
                <option value="Tripura">Tripura</option>
              </select>
            </div>

            <div className={styles.formGroup}>
              <label>District / Valley</label>
              <input
                type="text"
                placeholder="e.g. East Sikkim"
                value={formData.district}
                onChange={(e) => setFormData({ ...formData, district: e.target.value })}
              />
            </div>
          </div>

          <div className={styles.formRow}>
            <div className={styles.formGroup}>
              <label>Latitude *</label>
              <input
                type="number"
                step="any"
                required
                placeholder="27.3389"
                value={formData.latitude}
                onChange={(e) => setFormData({ ...formData, latitude: e.target.value })}
              />
            </div>

            <div className={styles.formGroup}>
              <label>Longitude *</label>
              <input
                type="number"
                step="any"
                required
                placeholder="88.6065"
                value={formData.longitude}
                onChange={(e) => setFormData({ ...formData, longitude: e.target.value })}
              />
            </div>
          </div>

          <Button type="button" variant="secondary" size="small" onClick={handleGetCurrentLocation}>
            📍 Get GPS Coordinates
          </Button>

          <div className={styles.formRow}>
            <div className={styles.formGroup}>
              <label>Hazard Category *</label>
              <select
                value={formData.hazardType}
                onChange={(e) => setFormData({ ...formData, hazardType: e.target.value })}
              >
                <option value="landslide">Active Landslide</option>
                <option value="mudflow">Debris / Mudflow</option>
                <option value="soil-erosion">Severe Soil Erosion</option>
                <option value="rock-fall">Rock Fall</option>
                <option value="ground-cracks">Ground Cracks / Subsidence</option>
              </select>
            </div>

            <div className={styles.formGroup}>
              <label>Severity Level *</label>
              <select
                value={formData.severity}
                onChange={(e) => setFormData({ ...formData, severity: e.target.value })}
              >
                <option value="low">Low (Minor Warning)</option>
                <option value="medium">Medium (Moderate Hazard)</option>
                <option value="high">High (Dangerous Slope)</option>
                <option value="critical">Critical (Immediate Evacuation)</option>
              </select>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem', padding: '0.85rem', background: '#f8fafc', borderRadius: '6px', border: '1px solid #cbd5e1' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: '800', color: '#0f172a' }}>Observable Field Indicators:</span>
            <label style={{ fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={formData.visible_cracks}
                onChange={(e) => setFormData({ ...formData, visible_cracks: e.target.checked })}
              />
              Visible ground / road tension cracks
            </label>
            <label style={{ fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={formData.rockfall_observed}
                onChange={(e) => setFormData({ ...formData, rockfall_observed: e.target.checked })}
              />
              Active rockfall or dislodged boulders
            </label>
            <label style={{ fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={formData.road_blocked}
                onChange={(e) => setFormData({ ...formData, road_blocked: e.target.checked })}
              />
              Highway / local road blocked
            </label>
            <label style={{ fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={formData.water_accumulation}
                onChange={(e) => setFormData({ ...formData, water_accumulation: e.target.checked })}
              />
              Abnormal seepage or water ponding
            </label>
          </div>

          <div className={styles.formGroup}>
            <label>Field Observations & Summary *</label>
            <textarea
              required
              rows={3}
              placeholder="Describe slope condition, affected settlements, and ongoing movement..."
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
          </div>

          <div className={styles.modalActions}>
            <Button
              type="button"
              variant="secondary"
              onClick={() => setIsModalOpen(false)}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              loading={submitting}
            >
              Submit Report
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default Reports;
