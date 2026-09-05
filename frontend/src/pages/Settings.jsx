import { useState } from 'react';
import { Bell, Map, Moon, Shield, Save } from 'lucide-react';
import PageHeader from '../components/layout/PageHeader';
import Button from '../components/common/Button';
import Toast from '../components/common/Toast';
import styles from './Settings.module.css';

const Settings = () => {
  const [toastMessage, setToastMessage] = useState(null);
  const [settings, setSettings] = useState({
    emailAlerts: true,
    pushNotifications: true,
    criticalOnly: false,
    defaultLayer: 'osm',
    autoLocation: true,
    theme: 'light',
    riskThreshold: '75'
  });

  const handleToggle = (key) => {
    setSettings(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const handleChange = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const handleSave = () => {
    setToastMessage('System and notification preferences saved successfully.');
  };

  return (
    <div className={styles.container}>
      <PageHeader
        title="System Settings & Preferences"
        subtitle="Configure early warning thresholds, telemetry streams, and notifications"
        action={
          <Button variant="primary" icon={Save} onClick={handleSave}>
            Save Changes
          </Button>
        }
      />

      <div className={styles.settingsGrid}>
        <div className={styles.card}>
          <div className={styles.cardHeader}>
            <Bell size={20} className={styles.cardIcon} />
            <h3>Notification Subscriptions</h3>
          </div>
          <div className={styles.cardBody}>
            <div className={styles.settingItem}>
              <div>
                <h4>Email Alerts</h4>
                <p>Receive high-risk warnings via configured responder emails</p>
              </div>
              <input
                type="checkbox"
                checked={settings.emailAlerts}
                onChange={() => handleToggle('emailAlerts')}
              />
            </div>
            <div className={styles.settingItem}>
              <div>
                <h4>Push Notifications</h4>
                <p>Real-time browser notifications on urgent threshold breaches</p>
              </div>
              <input
                type="checkbox"
                checked={settings.pushNotifications}
                onChange={() => handleToggle('pushNotifications')}
              />
            </div>
            <div className={styles.settingItem}>
              <div>
                <h4>Critical Alerts Only</h4>
                <p>Suppress notifications for medium risk levels</p>
              </div>
              <input
                type="checkbox"
                checked={settings.criticalOnly}
                onChange={() => handleToggle('criticalOnly')}
              />
            </div>
          </div>
        </div>

        <div className={styles.card}>
          <div className={styles.cardHeader}>
            <Map size={20} className={styles.cardIcon} />
            <h3>Map & Geospatial Options</h3>
          </div>
          <div className={styles.cardBody}>
            <div className={styles.settingItem}>
              <div>
                <h4>Default Base Layer</h4>
                <p>Choose initial basemap tile provider</p>
              </div>
              <select
                value={settings.defaultLayer}
                onChange={(e) => handleChange('defaultLayer', e.target.value)}
              >
                <option value="osm">OpenStreetMap</option>
                <option value="satellite">ESRI World Imagery</option>
                <option value="terrain">Topographic Map</option>
              </select>
            </div>
            <div className={styles.settingItem}>
              <div>
                <h4>Auto Center on Location</h4>
                <p>Request GPS automatically on initial page load</p>
              </div>
              <input
                type="checkbox"
                checked={settings.autoLocation}
                onChange={() => handleToggle('autoLocation')}
              />
            </div>
          </div>
        </div>

        <div className={styles.card}>
          <div className={styles.cardHeader}>
            <Shield size={20} className={styles.cardIcon} />
            <h3>Risk Threshold Tuning</h3>
          </div>
          <div className={styles.cardBody}>
            <div className={styles.settingItem}>
              <div>
                <h4>Critical Hazard Trigger (%)</h4>
                <p>Probability threshold required to dispatch field responders</p>
              </div>
              <input
                type="number"
                min="50"
                max="95"
                value={settings.riskThreshold}
                onChange={(e) => handleChange('riskThreshold', e.target.value)}
                style={{ width: '80px', padding: '0.375rem', borderRadius: '4px', border: '1px solid #ccc' }}
              />
            </div>
          </div>
        </div>
      </div>

      {toastMessage && (
        <Toast
          message={toastMessage}
          onClose={() => setToastMessage(null)}
        />
      )}
    </div>
  );
};

export default Settings;
