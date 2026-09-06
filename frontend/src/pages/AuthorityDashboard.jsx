import { useState, useEffect } from 'react';
import { 
  ShieldAlert, 
  MapPin, 
  Send, 
  Radio, 
  CheckCircle2, 
  Clock, 
  AlertOctagon, 
  FileText, 
  BarChart3, 
  RotateCw,
  Eye,
  Filter,
  Bell,
  Mail,
  MessageSquare,
  Smartphone,
  AlertTriangle,
  Compass,
  Navigation,
  Trash2,
  CheckCircle,
  X
} from 'lucide-react';
import PageHeader from '../components/layout/PageHeader';
import Button from '../components/common/Button';
import Modal from '../components/common/Modal';
import { api } from '../services/api';
import alertStyles from './Alerts.module.css';
import authStyles from './AuthorityDashboard.module.css';

const STATE_AREAS = {
  'Sikkim': ['Gangtok', 'Namchi', 'Mangan (North Sikkim)', 'Gyalshing', 'Rangpo (NH10 Corridor)'],
  'Meghalaya': ['Shillong', 'Cherrapunji (Sohra)', 'Mawsynram', 'Tura (Garo Hills)', 'Nongstoin', 'Jowai (Jaintia Hills)'],
  'Arunachal Pradesh': ['Itanagar', 'Tawang', 'Bomdila', 'Pasighat', 'Ziro Valley', 'Bhalukpong (NH13 Highway)'],
  'Nagaland': ['Kohima', 'Mokokchung', 'Dimapur', 'Wokha', 'Phek'],
  'Manipur': ['Imphal (Valley Fringe)', 'Tamenglong', 'Ukhrul', 'Churachandpur', 'Noney (Railway Corridor)'],
  'Mizoram': ['Aizawl', 'Lunglei', 'Champhai', 'Kolasib (NH306 Highway)', 'Serchhip'],
  'Assam': ['Guwahati (Kamakhya/Kalapahar Hills)', 'Haflong (Dima Hasao Hills)', 'Diphu (Karbi Anglong)', 'Silchar (Barail Foothills)', 'Tezpur'],
  'Tripura': ['Agartala', 'Jampui Hills', 'Dharmanagar']
};

const AuthorityDashboard = () => {
  const [reports, setReports] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [logs, setLogs] = useState([]);
  const [selectedState, setSelectedState] = useState('');
  const [loading, setLoading] = useState(false);
  const [syncing, setSyncing] = useState(false);
  const [activeTab, setActiveTab] = useState('alerts');

  // Dispatch Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [dispatchState, setDispatchState] = useState('Sikkim');
  const [dispatchArea, setDispatchArea] = useState('Gangtok');
  const [riskLevel, setRiskLevel] = useState('CRITICAL');
  const [customMsg, setCustomMsg] = useState('');
  const [broadcasting, setBroadcasting] = useState(false);

  // In-Website Popup Toast Message State (Replaces native browser alert())
  const [statusPopup, setStatusPopup] = useState(null);

  const showInWebsitePopup = (type, title, message) => {
    setStatusPopup({ type, title, message });
    setTimeout(() => {
      setStatusPopup(null);
    }, 6000);
  };

  const loadData = async () => {
    setLoading(true);
    try {
      const [reportsData, alertsData, logsData] = await Promise.all([
        api.getReports(selectedState ? { state: selectedState } : {}),
        api.getAlerts(selectedState ? { state: selectedState } : {}),
        fetch('http://127.0.0.1:8000/api/v1/notifications/logs?limit=30').then(r => r.json()).catch(() => [])
      ]);
      setReports(reportsData || []);
      setAlerts(alertsData || []);
      setLogs(Array.isArray(logsData) ? logsData : []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, [selectedState]);

  const handleSyncML = async () => {
    setSyncing(true);
    try {
      await api.syncLiveAlerts();
      await loadData();
      showInWebsitePopup('success', 'ML Telemetry Synchronized', 'Real-time satellite & slope models updated across all 40 regional stations.');
    } catch (e) {
      showInWebsitePopup('error', 'Synchronization Error', e.message);
    } finally {
      setSyncing(false);
    }
  };

  const handleStateSelectChange = (e) => {
    const newState = e.target.value;
    setDispatchState(newState);
    setDispatchArea(STATE_AREAS[newState] ? STATE_AREAS[newState][0] : '');
  };

  const handleTargetedDispatch = async (e) => {
    e.preventDefault();
    setBroadcasting(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/notifications/targeted-dispatch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          state: dispatchState,
          area: dispatchArea,
          risk_level: riskLevel,
          probability: riskLevel === 'CRITICAL' ? 0.96 : (riskLevel === 'HIGH' ? 0.82 : 0.60),
          custom_message: customMsg || undefined
        })
      });
      const data = await res.json();

      setIsModalOpen(false);
      await loadData();
      showInWebsitePopup(
        'success',
        `🚨 Early Warning Broadcast Dispatched (${dispatchArea}, ${dispatchState})`,
        `Targeted emergency warning sent to ${data.recipients_targeted} registered citizens & field responders via TextBee SMS. Live alert is active.`
      );
    } catch (err) {
      showInWebsitePopup('error', 'Dispatch Notice', err.message);
    } finally {
      setBroadcasting(false);
    }
  };

  const handleStatusChange = async (reportId, newStatus) => {
    try {
      await api.updateReportStatus(reportId, newStatus, 'Status updated via Authority Command Center');
      await loadData();
      showInWebsitePopup('success', 'Report Status Updated', `Report ID ${reportId} marked as ${newStatus}.`);
    } catch (e) {
      showInWebsitePopup('error', 'Update Failed', e.message);
    }
  };

  const handleDeleteReport = async (reportId) => {
    try {
      await api.deleteReport(reportId);
      await loadData();
      showInWebsitePopup('success', 'Report Deleted', `Report ID ${reportId} removed from database.`);
    } catch (err) {
      showInWebsitePopup('error', 'Delete Failed', err.message);
    }
  };

  const nerStates = [
    'All States', 'Arunachal Pradesh', 'Assam', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Sikkim', 'Tripura'
  ];

  return (
    <div className={alertStyles.container}>
      {/* In-Website Toast Popup (No native browser alerts) */}
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
        title="Authority Command & Disaster Management Center"
        subtitle="Real-time multi-state monitoring, targeted emergency dispatch, and field response workflows"
        action={
          <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
            <Button
              variant="danger"
              icon={Send}
              onClick={() => setIsModalOpen(true)}
            >
              Dispatch Targeted Emergency Alert
            </Button>
            <Button
              variant="secondary"
              icon={RotateCw}
              onClick={handleSyncML}
              loading={syncing}
            >
              Trigger Live ML Evaluation
            </Button>
          </div>
        }
      />

      {/* State Filter Bar */}
      <div style={{ background: '#ffffff', padding: '1rem 1.5rem', borderRadius: '8px', border: '1px solid #cbd5e1', display: 'flex', gap: '0.75rem', alignItems: 'center', flexWrap: 'wrap', boxShadow: 'var(--shadow-sm)' }}>
        <Filter size={18} color="#1d4ed8" />
        <span style={{ fontWeight: '700', fontSize: '0.85rem', color: '#0f172a' }}>State Jurisdiction:</span>
        {nerStates.map(st => (
          <button
            key={st}
            onClick={() => setSelectedState(st === 'All States' ? '' : st)}
            style={{
              padding: '0.4rem 0.85rem',
              borderRadius: '6px',
              border: '1px solid',
              borderColor: (selectedState === st || (st === 'All States' && !selectedState)) ? '#1d4ed8' : '#cbd5e1',
              background: (selectedState === st || (st === 'All States' && !selectedState)) ? '#eff6ff' : '#ffffff',
              color: (selectedState === st || (st === 'All States' && !selectedState)) ? '#1d4ed8' : '#475569',
              fontWeight: '700',
              fontSize: '0.8rem',
              cursor: 'pointer',
              transition: 'all 0.15s ease'
            }}
          >
            {st}
          </button>
        ))}
      </div>

      {/* Metrics Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.25rem' }}>
        <div style={{ background: '#ffffff', padding: '1.5rem', borderRadius: '8px', borderLeft: '4px solid #b91c1c', border: '1px solid #cbd5e1', boxShadow: 'var(--shadow-sm)' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: '800', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Critical Threat Zones</div>
          <div style={{ fontSize: '2.25rem', fontWeight: '800', color: '#0f172a', marginTop: '0.25rem', lineHeight: 1 }}>
            {alerts.filter(a => a.riskLevel === 'CRITICAL').length}
          </div>
        </div>

        <div style={{ background: '#ffffff', padding: '1.5rem', borderRadius: '8px', borderLeft: '4px solid #ea580c', border: '1px solid #cbd5e1', boxShadow: 'var(--shadow-sm)' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: '800', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.05em' }}>High Risk Zones</div>
          <div style={{ fontSize: '2.25rem', fontWeight: '800', color: '#0f172a', marginTop: '0.25rem', lineHeight: 1 }}>
            {alerts.filter(a => a.riskLevel === 'HIGH').length}
          </div>
        </div>

        <div style={{ background: '#ffffff', padding: '1.5rem', borderRadius: '8px', borderLeft: '4px solid #1d4ed8', border: '1px solid #cbd5e1', boxShadow: 'var(--shadow-sm)' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: '800', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Pending Field Reports</div>
          <div style={{ fontSize: '2.25rem', fontWeight: '800', color: '#0f172a', marginTop: '0.25rem', lineHeight: 1 }}>
            {reports.filter(r => r.status === 'NEW' || r.status === 'UNDER_REVIEW').length}
          </div>
        </div>

        <div style={{ background: '#ffffff', padding: '1.5rem', borderRadius: '8px', borderLeft: '4px solid #047857', border: '1px solid #cbd5e1', boxShadow: 'var(--shadow-sm)' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: '800', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Verified & Actioned</div>
          <div style={{ fontSize: '2.25rem', fontWeight: '800', color: '#0f172a', marginTop: '0.25rem', lineHeight: 1 }}>
            {reports.filter(r => r.status === 'ACTION_REQUIRED' || r.status === 'RESOLVED').length}
          </div>
        </div>
      </div>

      {/* Main Authority Table */}
      <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid #cbd5e1', overflow: 'hidden', boxShadow: 'var(--shadow-sm)' }}>
        <div style={{ display: 'flex', borderBottom: '1px solid #cbd5e1', background: '#f8fafc' }}>
          <button
            onClick={() => setActiveTab('alerts')}
            style={{
              padding: '1rem 1.75rem',
              fontWeight: '700',
              fontSize: '0.9rem',
              border: 'none',
              background: activeTab === 'alerts' ? '#ffffff' : 'transparent',
              borderBottom: activeTab === 'alerts' ? '3px solid #1d4ed8' : 'none',
              color: activeTab === 'alerts' ? '#1d4ed8' : '#64748b',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}
          >
            <Radio size={16} /> Regional Risk Stations ({alerts.length})
          </button>
          <button
            onClick={() => setActiveTab('reports')}
            style={{
              padding: '1rem 1.75rem',
              fontWeight: '700',
              fontSize: '0.9rem',
              border: 'none',
              background: activeTab === 'reports' ? '#ffffff' : 'transparent',
              borderBottom: activeTab === 'reports' ? '3px solid #1d4ed8' : 'none',
              color: activeTab === 'reports' ? '#1d4ed8' : '#64748b',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}
          >
            <FileText size={16} /> Field Incident Reports ({reports.length})
          </button>
          <button
            onClick={() => setActiveTab('logs')}
            style={{
              padding: '1rem 1.75rem',
              fontWeight: '700',
              fontSize: '0.9rem',
              border: 'none',
              background: activeTab === 'logs' ? '#ffffff' : 'transparent',
              borderBottom: activeTab === 'logs' ? '3px solid #1d4ed8' : 'none',
              color: activeTab === 'logs' ? '#1d4ed8' : '#64748b',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}
          >
            <Bell size={16} /> Notification Dispatch Logs ({logs.length})
          </button>
        </div>

        <div style={{ padding: '1.5rem' }}>
          {activeTab === 'alerts' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              {alerts.map(a => (
                <div key={a.id} style={{ padding: '1.25rem 1.5rem', border: '1px solid #e2e8f0', borderRadius: '6px', background: '#f8fafc', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      <span style={{ fontWeight: '800', fontSize: '1.05rem', color: '#0f172a' }}>{a.location}</span>
                      <span style={{ fontSize: '0.75rem', fontWeight: '800', padding: '0.2rem 0.6rem', borderRadius: '4px', background: a.riskLevel === 'CRITICAL' ? '#fee2e2' : a.riskLevel === 'HIGH' ? '#ffedd5' : '#ecfdf5', color: a.riskLevel === 'CRITICAL' ? '#b91c1c' : a.riskLevel === 'HIGH' ? '#ea580c' : '#047857' }}>
                        {a.riskLevel} ({Math.round(a.probability * 100)}%)
                      </span>
                    </div>
                    <p style={{ fontSize: '0.85rem', color: '#475569', marginTop: '0.35rem', lineHeight: '1.5' }}>{a.description}</p>
                  </div>
                  <div style={{ fontSize: '0.85rem', color: '#334155', fontWeight: '700' }}>
                    Pop. Exposed: {a.affectedPopulation?.toLocaleString() || 'N/A'}
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'reports' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {reports.length === 0 ? (
                <div style={{ textAlign: 'center', padding: '3rem', color: '#64748b' }}>No field reports matching current filter criteria.</div>
              ) : (
                reports.map(r => (
                  <div key={r.id} style={{ padding: '1.25rem 1.5rem', border: '1px solid #e2e8f0', borderRadius: '6px', background: '#f8fafc', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
                    <div style={{ flex: 1, minWidth: '280px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                        <span style={{ fontWeight: '800', fontSize: '1.05rem', color: '#0f172a' }}>{r.location}</span>
                        <span style={{ fontSize: '0.75rem', fontWeight: '800', padding: '0.2rem 0.6rem', borderRadius: '4px', background: r.severity === 'high' || r.severity === 'critical' ? '#fee2e2' : '#fef3c7', color: r.severity === 'high' || r.severity === 'critical' ? '#b91c1c' : '#b45309', textTransform: 'uppercase' }}>
                          {r.severity}
                        </span>
                        <span style={{ fontSize: '0.75rem', fontWeight: '800', padding: '0.2rem 0.6rem', borderRadius: '4px', background: '#eff6ff', color: '#1d4ed8' }}>
                          {r.status}
                        </span>
                      </div>
                      <p style={{ fontSize: '0.875rem', color: '#475569', marginTop: '0.35rem', lineHeight: '1.5' }}>{r.description}</p>
                    </div>
                    
                    <div style={{ display: 'flex', gap: '0.65rem', alignItems: 'center' }}>
                      <span style={{ fontSize: '0.8rem', fontWeight: '700', color: '#334155' }}>Action:</span>
                      <select
                        value={r.status}
                        onChange={(e) => handleStatusChange(r.id, e.target.value)}
                        style={{ padding: '0.45rem 0.75rem', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '0.85rem', fontWeight: '700', color: '#0f172a', background: '#ffffff', cursor: 'pointer' }}
                      >
                        <option value="NEW">NEW</option>
                        <option value="UNDER_REVIEW">UNDER REVIEW</option>
                        <option value="VERIFIED">VERIFIED</option>
                        <option value="ACTION_REQUIRED">ACTION REQUIRED (DISPATCH)</option>
                        <option value="RESOLVED">RESOLVED</option>
                        <option value="REJECTED">REJECTED</option>
                      </select>

                      <button
                        onClick={() => handleDeleteReport(r.id)}
                        title="Delete this report"
                        style={{
                          background: 'none',
                          border: 'none',
                          color: '#94a3b8',
                          cursor: 'pointer',
                          padding: '0.4rem',
                          display: 'flex',
                          alignItems: 'center',
                          borderRadius: '6px',
                          transition: 'all 0.15s ease'
                        }}
                        onMouseEnter={(e) => { e.currentTarget.style.color = '#dc2626'; e.currentTarget.style.background = '#fee2e2'; }}
                        onMouseLeave={(e) => { e.currentTarget.style.color = '#94a3b8'; e.currentTarget.style.background = 'none'; }}
                      >
                        <Trash2 size={18} />
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}

          {activeTab === 'logs' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {logs.map(l => (
                <div key={l.id} style={{ padding: '1.1rem 1.25rem', border: '1px solid #e2e8f0', borderRadius: '6px', background: '#f8fafc', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flex: 1, minWidth: '280px' }}>
                    <div style={{ 
                      width: '40px', 
                      height: '40px', 
                      borderRadius: '6px', 
                      display: 'flex', 
                      alignItems: 'center', 
                      justifyContent: 'center',
                      background: l.channel === 'SMS' ? '#eff6ff' : '#fef3c7',
                      color: l.channel === 'SMS' ? '#1d4ed8' : '#b45309'
                    }}>
                      {l.channel === 'SMS' ? <MessageSquare size={20} /> : <Mail size={20} />}
                    </div>
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span style={{ fontWeight: '800', fontSize: '0.9rem', color: '#0f172a' }}>{l.recipient}</span>
                        <span style={{ fontSize: '0.7rem', fontWeight: '800', padding: '0.15rem 0.5rem', borderRadius: '4px', background: '#e2e8f0', color: '#334155' }}>
                          {l.recipient_role || 'CITIZEN'}
                        </span>
                        <span style={{ fontSize: '0.7rem', fontWeight: '800', padding: '0.15rem 0.5rem', borderRadius: '4px', background: '#ecfdf5', color: '#047857' }}>
                          {l.status}
                        </span>
                      </div>
                      <p style={{ fontSize: '0.825rem', color: '#475569', marginTop: '0.25rem', lineHeight: '1.4' }}>{l.message}</p>
                    </div>
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', display: 'flex', alignItems: 'center', gap: '0.3rem', fontWeight: '600' }}>
                    <Clock size={14} />
                    <span>{new Date(l.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Authority Targeted Emergency Dispatch Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Dispatch Targeted Emergency Alert"
      >
        <form onSubmit={handleTargetedDispatch} className={authStyles.dispatchModalForm}>
          <div className={authStyles.warningNotice}>
            <AlertTriangle size={20} color="#dc2626" style={{ flexShrink: 0, marginTop: '2px' }} />
            <div>
              <strong>Targeted Early Warning Broadcast:</strong> Emergency alerts will be dispatched via <strong>TextBee SMS</strong> and in-app feeds strictly to registered citizens and disaster response units in the selected area.
            </div>
          </div>

          <div className={authStyles.formSection}>
            <div className={authStyles.inputRow}>
              <div className={authStyles.inputField}>
                <label className={authStyles.inputLabel}>
                  <MapPin size={14} color="#1d4ed8" /> Target State Jurisdiction *
                </label>
                <select 
                  className={authStyles.selectControl} 
                  value={dispatchState} 
                  onChange={handleStateSelectChange}
                >
                  {Object.keys(STATE_AREAS).map(st => (
                    <option key={st} value={st}>{st}</option>
                  ))}
                </select>
              </div>

              <div className={authStyles.inputField}>
                <label className={authStyles.inputLabel}>
                  <Compass size={14} color="#1d4ed8" /> Target Location / Corridor *
                </label>
                <select 
                  className={authStyles.selectControl} 
                  value={dispatchArea} 
                  onChange={(e) => setDispatchArea(e.target.value)}
                >
                  {(STATE_AREAS[dispatchState] || []).map(area => (
                    <option key={area} value={area}>{area}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className={authStyles.inputField}>
              <label className={authStyles.inputLabel}>
                <ShieldAlert size={14} color="#dc2626" /> Landslide Hazard Threat Level *
              </label>
              <select 
                className={authStyles.selectControl} 
                value={riskLevel} 
                onChange={(e) => setRiskLevel(e.target.value)}
              >
                <option value="CRITICAL">CRITICAL (Immediate Evacuation Advisory - 96% Model Probability)</option>
                <option value="HIGH">HIGH (Severe Slope Failure Hazard - 82% Model Probability)</option>
                <option value="MEDIUM">MEDIUM (Moderate Precautionary Watch - 60% Model Probability)</option>
              </select>
            </div>

            <div className={authStyles.inputField}>
              <label className={authStyles.inputLabel}>
                <FileText size={14} color="#1d4ed8" /> Emergency Alert Message (SMS Text)
              </label>
              <textarea
                className={authStyles.textControl}
                rows={3}
                placeholder={`GOVT DISASTER ALERT: [${riskLevel} RISK] Landslide hazard detected at ${dispatchArea}, ${dispatchState}. Evacuate steep slope cuts immediately.`}
                value={customMsg}
                onChange={(e) => setCustomMsg(e.target.value)}
              />
              <span style={{ fontSize: '0.72rem', color: '#64748b', marginTop: '0.2rem' }}>
                Leave blank to automatically send standardized NDMA emergency broadcast text.
              </span>
            </div>
          </div>

          <div className={authStyles.modalFooterActions}>
            <Button
              type="button"
              variant="secondary"
              onClick={() => setIsModalOpen(false)}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="danger"
              icon={Send}
              loading={broadcasting}
            >
              Broadcast Alert to {dispatchArea}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default AuthorityDashboard;
