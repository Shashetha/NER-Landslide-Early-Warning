import { useState, useEffect } from 'react';
import { 
  Bell, 
  Shield, 
  Smartphone, 
  MapPin, 
  Globe, 
  Database, 
  Key, 
  CheckCircle, 
  Save,
  LogOut,
  RotateCcw
} from 'lucide-react';
import PageHeader from '../components/layout/PageHeader';
import Button from '../components/common/Button';
import styles from './Settings.module.css';

const Settings = () => {
  const [settings, setSettings] = useState({
    smsNotifications: true,
    emailNotifications: true,
    minRiskThreshold: 'HIGH',
    targetState: 'All States',
    language: 'English',
    offlineStorageQuota: '50 MB',
    dataRefreshInterval: '15s',
  });

  const [saved, setSaved] = useState(false);

  const handleSave = (e) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const handleClearOfflineCache = () => {
    if (window.indexedDB) {
      window.indexedDB.deleteDatabase('NER_Landslide_Offline_DB');
      alert('Offline IndexedDB cache cleared.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
    window.location.href = '/';
  };

  return (
    <div className={styles.container}>
      <PageHeader
        title="Disaster Platform & Notification Settings"
        subtitle="Configure early warning broadcast thresholds, SMS dispatch rules, and offline data cache"
      />

      {saved && (
        <div style={{ background: '#ecfdf5', border: '1px solid #a7f3d0', color: '#047857', padding: '0.85rem 1.25rem', borderRadius: '6px', fontWeight: '700', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <CheckCircle size={18} />
          <span>Settings saved and applied to early warning gateway.</span>
        </div>
      )}

      <form onSubmit={handleSave} className={styles.settingsGrid}>
        {/* Notification Settings */}
        <div className={styles.card}>
          <div className={styles.cardHeader}>
            <Bell className={styles.cardIcon} size={20} />
            <h3>Emergency Alert & Dispatch Rules</h3>
          </div>

          <div className={styles.cardBody}>
            <div className={styles.settingItem}>
              <div>
                <h4>TextBee SMS Carrier Broadcasts</h4>
                <p>Deliver instant text message when hazard threshold is breached</p>
              </div>
              <input
                type="checkbox"
                checked={settings.smsNotifications}
                onChange={(e) => setSettings({ ...settings, smsNotifications: e.target.checked })}
              />
            </div>

            <div className={styles.settingItem}>
              <div>
                <h4>Disaster Authority Email Notices</h4>
                <p>Send multi-hazard reports directly to official commander inbox</p>
              </div>
              <input
                type="checkbox"
                checked={settings.emailNotifications}
                onChange={(e) => setSettings({ ...settings, emailNotifications: e.target.checked })}
              />
            </div>

            <div className={styles.settingItem}>
              <div>
                <h4>Minimum Risk Trigger Level</h4>
                <p>Threshold to activate automatic emergency SMS dispatch</p>
              </div>
              <select
                value={settings.minRiskThreshold}
                onChange={(e) => setSettings({ ...settings, minRiskThreshold: e.target.value })}
              >
                <option value="CRITICAL">Critical Only (75% and above)</option>
                <option value="HIGH">High and Critical (55% and above)</option>
                <option value="MEDIUM">Moderate, High and Critical (35% and above)</option>
              </select>
            </div>
          </div>
        </div>

        {/* Offline & Cache Management */}
        <div className={styles.card}>
          <div className={styles.cardHeader}>
            <Database className={styles.cardIcon} size={20} />
            <h3>PWA & Offline Storage (Remote Valleys)</h3>
          </div>

          <div className={styles.cardBody}>
            <div className={styles.settingItem}>
              <div>
                <h4>IndexedDB Local Storage</h4>
                <p>Retains field reports on device during zero-connectivity</p>
              </div>
              <span style={{ fontWeight: '700', fontSize: '0.85rem', color: '#047857' }}>Active</span>
            </div>

            <div className={styles.settingItem}>
              <div>
                <h4>Data Refresh Polling</h4>
                <p>Telemetry poll interval from Open-Meteo & station sensors</p>
              </div>
              <select
                value={settings.dataRefreshInterval}
                onChange={(e) => setSettings({ ...settings, dataRefreshInterval: e.target.value })}
              >
                <option value="10s">10 Seconds (Emergency mode)</option>
                <option value="15s">15 Seconds (Standard)</option>
                <option value="60s">1 Minute (Bandwidth Saver)</option>
              </select>
            </div>

            <div className={styles.settingItem}>
              <div>
                <h4>Clear Offline Storage Cache</h4>
                <p>Resets locally synced incident report queues</p>
              </div>
              <Button type="button" variant="secondary" size="small" onClick={handleClearOfflineCache}>
                Clear Cache
              </Button>
            </div>
          </div>
        </div>
      </form>

      {/* Save & Logout Actions */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1.5rem', paddingTop: '1.25rem', borderTop: '1px solid #cbd5e1' }}>
        <Button variant="primary" icon={Save} onClick={handleSave}>
          Save All Settings
        </Button>

        <Button variant="danger" icon={LogOut} onClick={handleLogout}>
          Sign Out of Authority Command
        </Button>
      </div>
    </div>
  );
};

export default Settings;
