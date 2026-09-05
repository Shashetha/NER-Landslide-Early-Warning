import { useState, useEffect } from 'react';
import { FileText, Plus, MapPin, Calendar, CheckCircle } from 'lucide-react';
import PageHeader from '../components/layout/PageHeader';
import Button from '../components/common/Button';
import Modal from '../components/common/Modal';
import Toast from '../components/common/Toast';
import Loader from '../components/common/Loader';
import { api } from '../services/api';
import { formatTimeAgo } from '../utils/riskUtils';
import styles from './Reports.module.css';

const Reports = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [toastMessage, setToastMessage] = useState(null);

  const [formData, setFormData] = useState({
    location: '',
    latitude: '11.4064',
    longitude: '76.6932',
    hazardType: 'landslide',
    severity: 'medium',
    description: '',
    contactInfo: ''
  });

  const fetchReports = async () => {
    try {
      const data = await api.getReports();
      setReports(data);
    } catch (err) {
      console.error('Failed to load reports:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const res = await api.submitHazardReport(formData);
      setToastMessage('Hazard report recorded and dispatched to field teams successfully.');
      setIsModalOpen(false);
      setFormData({
        location: '',
        latitude: '11.4064',
        longitude: '76.6932',
        hazardType: 'landslide',
        severity: 'medium',
        description: '',
        contactInfo: ''
      });
      fetchReports();
    } catch (err) {
      console.error('Submission failed:', err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className={styles.container}>
      <PageHeader
        title="Field Incident Reports"
        subtitle="Citizen & field officer crowdsourced hazard alerts and ground-truth verifications"
        action={
          <Button
            variant="primary"
            icon={Plus}
            onClick={() => setIsModalOpen(true)}
          >
            Submit Incident Report
          </Button>
        }
      />

      {loading ? (
        <Loader text="Loading incident database..." />
      ) : (
        <div className={styles.reportsGrid}>
          {reports.map((report) => (
            <div key={report.id} className={styles.reportCard}>
              <div className={styles.cardHeader}>
                <div className={styles.locationMeta}>
                  <MapPin size={18} className={styles.pin} />
                  <h3>{report.location}</h3>
                </div>
                <span className={`${styles.severityBadge} ${styles[report.severity]}`}>
                  {report.severity.toUpperCase()}
                </span>
              </div>

              <div className={styles.hazardType}>
                <strong>Type:</strong> {report.hazardType.replace('-', ' ').toUpperCase()}
              </div>

              <p className={styles.description}>{report.description}</p>

              <div className={styles.footer}>
                <div className={styles.metaItem}>
                  <Calendar size={14} />
                  <span>{formatTimeAgo(report.createdAt)}</span>
                </div>
                <span className={`${styles.statusBadge} ${styles[report.status]}`}>
                  {report.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Submit Hazard Incident Report"
      >
        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.formGroup}>
            <label>Location Name</label>
            <input
              type="text"
              name="location"
              required
              placeholder="e.g. Coonoor Ghat Road KM 14"
              value={formData.location}
              onChange={handleChange}
            />
          </div>

          <div className={styles.formRow}>
            <div className={styles.formGroup}>
              <label>Latitude</label>
              <input
                type="text"
                name="latitude"
                required
                value={formData.latitude}
                onChange={handleChange}
              />
            </div>
            <div className={styles.formGroup}>
              <label>Longitude</label>
              <input
                type="text"
                name="longitude"
                required
                value={formData.longitude}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className={styles.formRow}>
            <div className={styles.formGroup}>
              <label>Hazard Type</label>
              <select name="hazardType" value={formData.hazardType} onChange={handleChange}>
                <option value="landslide">Landslide / Mudflow</option>
                <option value="soil-erosion">Severe Soil Erosion</option>
                <option value="ground-cracks">Ground Cracks / Subsidence</option>
                <option value="rock-fall">Rock Fall</option>
              </select>
            </div>
            <div className={styles.formGroup}>
              <label>Estimated Severity</label>
              <select name="severity" value={formData.severity} onChange={handleChange}>
                <option value="low">Low Impact</option>
                <option value="medium">Medium Danger</option>
                <option value="high">High Threat</option>
              </select>
            </div>
          </div>

          <div className={styles.formGroup}>
            <label>Detailed Observations</label>
            <textarea
              name="description"
              rows={4}
              required
              placeholder="Describe road blocks, structural damage, water build-up or land movement..."
              value={formData.description}
              onChange={handleChange}
            />
          </div>

          <div className={styles.formGroup}>
            <label>Contact Email / Phone (Optional)</label>
            <input
              type="text"
              name="contactInfo"
              placeholder="For follow-up verification"
              value={formData.contactInfo}
              onChange={handleChange}
            />
          </div>

          <div className={styles.modalActions}>
            <Button
              variant="secondary"
              onClick={() => setIsModalOpen(false)}
              disabled={submitting}
            >
              Cancel
            </Button>
            <Button
              variant="primary"
              type="submit"
              loading={submitting}
            >
              Submit Report
            </Button>
          </div>
        </form>
      </Modal>

      {toastMessage && (
        <Toast
          message={toastMessage}
          onClose={() => setToastMessage(null)}
        />
      )}
    </div>
  );
};

export default Reports;
