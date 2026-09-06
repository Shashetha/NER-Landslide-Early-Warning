import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  AlertTriangle, 
  MapPin, 
  Layers, 
  Activity, 
  RotateCw, 
  ExternalLink,
  Shield,
  Search,
  Filter,
  CheckCircle2,
  Clock,
  Radio,
  FileText
} from 'lucide-react';
import PageHeader from '../components/layout/PageHeader';
import StatCard from '../components/dashboard/StatCard';
import RiskMap from '../components/map/RiskMap';
import RainfallChart from '../components/dashboard/RainfallChart';
import RecentAlerts from '../components/dashboard/RecentAlerts';
import Button from '../components/common/Button';
import { api } from '../services/api';
import styles from './Overview.module.css';

const STATE_COORDINATES = {
  'ALL': { center: [26.2006, 92.9376], zoom: 7 },
  'Sikkim': { center: [27.5330, 88.5122], zoom: 9 },
  'Meghalaya': { center: [25.4670, 91.3662], zoom: 9 },
  'Arunachal Pradesh': { center: [28.2180, 94.7278], zoom: 8 },
  'Nagaland': { center: [26.1584, 94.5624], zoom: 9 },
  'Manipur': { center: [24.6637, 93.9063], zoom: 9 },
  'Mizoram': { center: [23.1645, 92.9376], zoom: 9 },
  'Assam': { center: [26.2006, 92.9376], zoom: 8 },
  'Tripura': { center: [23.9408, 91.9882], zoom: 9 }
};

const Overview = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [riskZones, setRiskZones] = useState([]);
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedRiskFilter, setSelectedRiskFilter] = useState('ALL');
  const [selectedState, setSelectedState] = useState('ALL');
  const [mapCenter, setMapCenter] = useState([26.2006, 92.9376]);
  const [mapZoom, setMapZoom] = useState(7);

  const loadData = async () => {
    setLoading(true);
    try {
      const [dash, zones, repList] = await Promise.all([
        api.getDashboardData(),
        api.getRiskZones(),
        api.getReports()
      ]);
      setDashboardData(dash);
      setRiskZones(zones);
      setReports(repList || []);
    } catch (error) {
      console.error('Failed to load operational dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 15000);
    return () => clearInterval(interval);
  }, []);

  const handleStateClick = (st) => {
    setSelectedState(st);
    if (STATE_COORDINATES[st]) {
      setMapCenter(STATE_COORDINATES[st].center);
      setMapZoom(STATE_COORDINATES[st].zoom);
    }
  };

  const criticalCount = riskZones.filter(z => z.riskLevel === 'CRITICAL').length;
  const highCount = riskZones.filter(z => z.riskLevel === 'HIGH').length;
  const mediumCount = riskZones.filter(z => z.riskLevel === 'MEDIUM').length;
  const lowCount = riskZones.filter(z => z.riskLevel === 'LOW').length;

  const filteredMapZones = riskZones.filter(z => {
    const matchRisk = selectedRiskFilter === 'ALL' || z.riskLevel.toUpperCase() === selectedRiskFilter;
    const matchState = selectedState === 'ALL' || (z.name && z.name.toLowerCase().includes(selectedState.toLowerCase()));
    return matchRisk && matchState;
  });

  const nerStates = ['ALL', 'Sikkim', 'Meghalaya', 'Arunachal Pradesh', 'Nagaland', 'Manipur', 'Mizoram', 'Assam', 'Tripura'];

  return (
    <div className={styles.container}>
      <PageHeader
        title="Operational Disaster Monitoring & Threat Dashboard"
        subtitle="Real-time multi-hazard telemetry, AI risk distribution, and emergency dispatch status for North East India"
        action={
          <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
            <Link to="/map">
              <Button variant="secondary" icon={Layers}>
                Full GIS Map View
              </Button>
            </Link>
            <Button
              variant="secondary"
              icon={RotateCw}
              onClick={loadData}
              loading={loading}
            >
              Refresh Telemetry
            </Button>
          </div>
        }
      />

      {/* State Quick-Filter Bar with Auto-Pan & Zoom */}
      <div style={{ background: '#ffffff', padding: '0.85rem 1.25rem', borderRadius: '8px', border: '1px solid #cbd5e1', display: 'flex', gap: '0.75rem', alignItems: 'center', flexWrap: 'wrap', boxShadow: 'var(--shadow-sm)' }}>
        <Filter size={18} color="#1d4ed8" />
        <span style={{ fontWeight: '800', fontSize: '0.85rem', color: '#0f172a' }}>Focus Region:</span>
        {nerStates.map(st => (
          <button
            key={st}
            onClick={() => handleStateClick(st)}
            style={{
              padding: '0.35rem 0.75rem',
              borderRadius: '4px',
              border: '1px solid',
              borderColor: selectedState === st ? '#1d4ed8' : '#cbd5e1',
              background: selectedState === st ? '#eff6ff' : '#ffffff',
              color: selectedState === st ? '#1d4ed8' : '#475569',
              fontWeight: '700',
              fontSize: '0.8rem',
              cursor: 'pointer',
              transition: 'all 0.15s ease'
            }}
          >
            {st === 'ALL' ? 'All 8 NER States' : `📍 ${st}`}
          </button>
        ))}
      </div>

      {/* Clickable Real-Time Risk Metric Cards */}
      <div className={styles.statsGrid}>
        <div 
          onClick={() => setSelectedRiskFilter(selectedRiskFilter === 'CRITICAL' ? 'ALL' : 'CRITICAL')}
          style={{ cursor: 'pointer', outline: selectedRiskFilter === 'CRITICAL' ? '3px solid #b91c1c' : 'none', borderRadius: '8px' }}
        >
          <StatCard
            title="Critical Risk Zones"
            value={criticalCount}
            icon={AlertTriangle}
            color="red"
            trend={selectedRiskFilter === 'CRITICAL' ? 'Filtered Active' : 'Immediate Evacuation'}
            trendType="negative"
          />
        </div>

        <div 
          onClick={() => setSelectedRiskFilter(selectedRiskFilter === 'HIGH' ? 'ALL' : 'HIGH')}
          style={{ cursor: 'pointer', outline: selectedRiskFilter === 'HIGH' ? '3px solid #ea580c' : 'none', borderRadius: '8px' }}
        >
          <StatCard
            title="High Hazard Zones"
            value={highCount}
            icon={Radio}
            color="amber"
            trend={selectedRiskFilter === 'HIGH' ? 'Filtered Active' : 'Dangerous Slopes'}
            trendType="negative"
          />
        </div>

        <div 
          onClick={() => setSelectedRiskFilter(selectedRiskFilter === 'MEDIUM' ? 'ALL' : 'MEDIUM')}
          style={{ cursor: 'pointer', outline: selectedRiskFilter === 'MEDIUM' ? '3px solid #d97706' : 'none', borderRadius: '8px' }}
        >
          <StatCard
            title="Moderate Watch Areas"
            value={mediumCount}
            icon={Activity}
            color="amber"
            trend={selectedRiskFilter === 'MEDIUM' ? 'Filtered Active' : 'Close Vigilance'}
            trendType="positive"
          />
        </div>

        <div 
          onClick={() => setSelectedRiskFilter(selectedRiskFilter === 'LOW' ? 'ALL' : 'LOW')}
          style={{ cursor: 'pointer', outline: selectedRiskFilter === 'LOW' ? '3px solid #047857' : 'none', borderRadius: '8px' }}
        >
          <StatCard
            title="Stable Low Risk Stations"
            value={lowCount}
            icon={CheckCircle2}
            color="green"
            trend={selectedRiskFilter === 'LOW' ? 'Filtered Active' : 'Normal Telemetry'}
            trendType="positive"
          />
        </div>
      </div>

      {/* Main Operational Area: Interactive GIS Map & Side Alerts Panel */}
      <div className={styles.chartsGrid}>
        <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid #cbd5e1', overflow: 'hidden', boxShadow: 'var(--shadow-sm)', display: 'flex', flexDirection: 'column' }}>
          <div style={{ padding: '1rem 1.25rem', background: '#f8fafc', borderBottom: '1px solid #cbd5e1', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Layers size={18} color="#1d4ed8" />
              <span style={{ fontWeight: '800', fontSize: '0.95rem', color: '#0f172a' }}>
                Operational Risk Map ({filteredMapZones.length} Active Hotspots)
              </span>
            </div>
            <span style={{ fontSize: '0.75rem', fontWeight: '700', color: '#64748b' }}>
              Focus: {selectedState}
            </span>
          </div>

          <div style={{ height: '420px', width: '100%' }}>
            <RiskMap
              riskZones={filteredMapZones}
              height="420px"
              center={mapCenter}
              zoom={mapZoom}
              interactive={true}
            />
          </div>
        </div>

        <div className={styles.sideChart}>
          <RecentAlerts alerts={dashboardData?.recentAlerts || []} />
        </div>
      </div>

      {/* Bottom Operational Intelligence */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '1.25rem' }}>
        <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid #cbd5e1', padding: '1.5rem', boxShadow: 'var(--shadow-sm)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', paddingBottom: '0.5rem', borderBottom: '1px solid #e2e8f0' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: '800', color: '#0f172a' }}>
              Regional Precipitation Telemetry (NASA IMERG)
            </h3>
            <span style={{ fontSize: '0.75rem', color: '#1d4ed8', fontWeight: '700' }}>7-Day History</span>
          </div>
          <RainfallChart data={dashboardData?.rainfallData} />
        </div>

        <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid #cbd5e1', padding: '1.5rem', boxShadow: 'var(--shadow-sm)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', paddingBottom: '0.5rem', borderBottom: '1px solid #e2e8f0' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: '800', color: '#0f172a' }}>
              Ground Incident Reports ({reports.length})
            </h3>
            <Link to="/reports" style={{ fontSize: '0.8rem', color: '#1d4ed8', fontWeight: '700' }}>
              View All Reports →
            </Link>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {reports.slice(0, 4).map(r => (
              <div key={r.id} style={{ padding: '0.85rem 1rem', background: '#f8fafc', borderRadius: '6px', border: '1px solid #e2e8f0', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ fontWeight: '700', fontSize: '0.9rem', color: '#0f172a' }}>{r.location}</div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.15rem' }}>{r.description?.slice(0, 55)}...</div>
                </div>
                <span style={{
                  fontSize: '0.7rem',
                  fontWeight: '800',
                  padding: '0.2rem 0.5rem',
                  borderRadius: '4px',
                  background: r.severity === 'high' || r.severity === 'critical' ? '#fee2e2' : '#fef3c7',
                  color: r.severity === 'high' || r.severity === 'critical' ? '#b91c1c' : '#b45309',
                  textTransform: 'uppercase'
                }}>
                  {r.severity}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Overview;
