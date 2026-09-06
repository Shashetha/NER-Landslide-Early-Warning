import { Link } from 'react-router-dom';
import { 
  Shield, 
  Map, 
  FileText, 
  Activity, 
  Radio, 
  WifiOff, 
  Layers, 
  CheckCircle2, 
  ArrowRight,
  TrendingUp,
  CloudRain,
  Mountain,
  Compass,
  Building,
  Satellite,
  Bell,
  Cpu,
  Database,
  ExternalLink,
  ChevronRight,
  ShieldCheck,
  AlertTriangle
} from 'lucide-react';
import Button from '../components/common/Button';
import styles from './Home.module.css';

const Home = () => {
  const nerStates = [
    { name: 'Arunachal Pradesh', capital: 'Itanagar', risk: 'High', terrain: 'Steep Eastern Himalayas', elevation: '3,048 m' },
    { name: 'Assam', capital: 'Dispur / Guwahati', risk: 'Moderate', terrain: 'Brahmaputra Valley & Hills', elevation: '680 m' },
    { name: 'Manipur', capital: 'Imphal', risk: 'High', terrain: 'Surrounding Hill Ranges', elevation: '1,662 m' },
    { name: 'Meghalaya', capital: 'Shillong', risk: 'Critical', terrain: 'Khasi & Jaintia Plateaus', elevation: '1,525 m' },
    { name: 'Mizoram', capital: 'Aizawl', risk: 'Critical', terrain: 'Lushai Fault Ridges', elevation: '1,334 m' },
    { name: 'Nagaland', capital: 'Kohima', risk: 'High', terrain: 'Naga Hills Corridor', elevation: '1,444 m' },
    { name: 'Sikkim', capital: 'Gangtok', risk: 'Critical', terrain: 'High Himalayan Slopes', elevation: '1,820 m' },
    { name: 'Tripura', capital: 'Agartala', risk: 'Moderate', terrain: 'Jampui Hill Ranges', elevation: '880 m' },
  ];

  return (
    <div className={styles.container}>
      {/* Official Government Top Header Banner */}
      <header className={styles.header}>
        <div className={styles.logo}>
          <div style={{
            width: '40px',
            height: '40px',
            background: 'linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%)',
            borderRadius: '8px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 2px 6px rgba(29, 78, 216, 0.4)'
          }}>
            <Activity color="#ffffff" size={22} />
          </div>
          <div>
            <div style={{ fontSize: '1.05rem', fontWeight: '900', letterSpacing: '-0.02em', color: '#ffffff' }}>
              NER-LEWS <span style={{ color: '#60a5fa', fontWeight: '600', fontSize: '0.85rem' }}>| Govt of India</span>
            </div>
            <div style={{ fontSize: '0.7rem', color: '#94a3b8', fontWeight: '600', letterSpacing: '0.02em' }}>
              North Eastern Region Landslide Early Warning & Disaster Management System
            </div>
          </div>
        </div>

        <nav className={styles.navLinks}>
          <Link to="/dashboard" className={styles.navLink}>Dashboard</Link>
          <Link to="/map" className={styles.navLink}>GIS Map</Link>
          <Link to="/risk-analysis" className={styles.navLink}>AI Telemetry</Link>
          <Link to="/reports" className={styles.navLink}>Field Reports</Link>
          <Link to="/dashboard">
            <Button variant="primary" size="small" icon={ChevronRight}>
              Command Portal
            </Button>
          </Link>
        </nav>
      </header>

      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <div className={styles.badge}>
            <ShieldCheck size={14} color="#60a5fa" />
            <span>National Disaster Management Platform • 8 NER States</span>
          </div>

          <h1 className={styles.title}>
            Next-Generation AI Landslide Monitoring & <span>Multi-Hazard Early Warning</span>
          </h1>

          <p className={styles.subtitle}>
            <strong>Safer Communities • Stronger Resilience.</strong> Powered by real NASA GPM satellite precipitation, SRTM terrain slope telemetry, and Random Forest machine learning to provide automated early warnings across 8 North-Eastern states.
          </p>

          <div className={styles.heroButtons}>
            <Link to="/dashboard">
              <Button variant="primary" size="large" icon={Activity}>
                Operational Dashboard
              </Button>
            </Link>
            <Link to="/map">
              <Button variant="secondary" size="large" icon={Map}>
                Interactive GIS Risk Map
              </Button>
            </Link>
            <Link to="/reports">
              <Button variant="secondary" size="large" icon={FileText}>
                Submit Ground Hazard Report
              </Button>
            </Link>
          </div>

          {/* Quick Metrics Bar */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
            gap: '1.25rem',
            width: '100%',
            maxWidth: '960px',
            marginTop: '3.5rem',
            padding: '1.25rem 1.75rem',
            background: 'rgba(255, 255, 255, 0.04)',
            borderRadius: '12px',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            backdropFilter: 'blur(10px)'
          }}>
            <div>
              <div style={{ fontSize: '1.75rem', fontWeight: '900', color: '#ffffff', lineHeight: 1 }}>40+</div>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: '600', marginTop: '0.2rem' }}>Monitored Corridors</div>
            </div>
            <div>
              <div style={{ fontSize: '1.75rem', fontWeight: '900', color: '#60a5fa', lineHeight: 1 }}>90.07%</div>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: '600', marginTop: '0.2rem' }}>ML Model Accuracy</div>
            </div>
            <div>
              <div style={{ fontSize: '1.75rem', fontWeight: '900', color: '#34d399', lineHeight: 1 }}>351</div>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: '600', marginTop: '0.2rem' }}>NASA Historical Events</div>
            </div>
            <div>
              <div style={{ fontSize: '1.75rem', fontWeight: '900', color: '#fbbf24', lineHeight: 1 }}>7-Day</div>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: '600', marginTop: '0.2rem' }}>Future Rain & Flood Forecast</div>
            </div>
          </div>
        </div>
      </section>

      {/* 8 North Eastern States Interactive Grid */}
      <section style={{ padding: '4.5rem 2rem 3rem', maxWidth: '1360px', margin: '0 auto', width: '100%' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', flexWrap: 'wrap', gap: '1rem', marginBottom: '2.5rem' }}>
          <div>
            <span style={{ fontSize: '0.78rem', fontWeight: '800', color: '#1d4ed8', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
              Regional Jurisdiction & Surveillance
            </span>
            <h2 style={{ fontSize: '1.85rem', fontWeight: '900', color: '#0f172a', marginTop: '0.25rem', letterSpacing: '-0.02em' }}>
              Active Disaster Monitoring Across 8 North-Eastern States
            </h2>
          </div>
          <Link to="/map" style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', fontWeight: '700', fontSize: '0.875rem', color: '#1d4ed8' }}>
            View Full Regional GIS Layers <ArrowRight size={16} />
          </Link>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.25rem' }}>
          {nerStates.map((st) => (
            <Link
              key={st.name}
              to={`/map?state=${encodeURIComponent(st.name)}`}
              className={styles.stateCard}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <div style={{ fontWeight: '800', fontSize: '1.05rem', color: '#0f172a' }}>{st.name}</div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.15rem', fontWeight: '600' }}>HQ: {st.capital}</div>
                </div>
                <span style={{
                  fontSize: '0.7rem',
                  fontWeight: '800',
                  padding: '0.2rem 0.6rem',
                  borderRadius: '4px',
                  background: st.risk === 'Critical' ? '#fee2e2' : (st.risk === 'High' ? '#fff7ed' : '#ecfdf5'),
                  color: st.risk === 'Critical' ? '#b91c1c' : (st.risk === 'High' ? '#ea580c' : '#047857'),
                  textTransform: 'uppercase',
                  letterSpacing: '0.04em'
                }}>
                  {st.risk}
                </span>
              </div>

              <div style={{ fontSize: '0.78rem', color: '#475569', marginTop: '0.85rem', paddingTop: '0.75rem', borderTop: '1px solid #f1f5f9', display: 'flex', justifyContent: 'space-between' }}>
                <span>Terrain: <strong>{st.terrain}</strong></span>
                <span>Max: <strong>{st.elevation}</strong></span>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Core Architectural Pillars */}
      <section className={styles.features}>
        <div className={styles.sectionHeader}>
          <span style={{ fontSize: '0.78rem', fontWeight: '800', color: '#1d4ed8', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
            System Architecture
          </span>
          <h2>Integrated Disaster Management Pillars</h2>
          <p>Engineered for government agencies, emergency response teams, and vulnerable communities.</p>
        </div>

        <div className={styles.featuresGrid}>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>
              <Cpu size={24} />
            </div>
            <h3>Calibrated Machine Learning</h3>
            <p>
              Trained on 702 real verified dataset records with 90.07% accuracy, evaluating dynamic satellite rainfall surges, SRTM elevation, slope angles, and soil moisture saturation.
            </p>
          </div>

          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>
              <Satellite size={24} />
            </div>
            <h3>Interactive GIS Threat Maps</h3>
            <p>
              Interactive geospatial mapping rendering 351 confirmed historical landslide events alongside live regional sensor stations and multi-hazard pulse circles.
            </p>
          </div>

          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>
              <Radio size={24} />
            </div>
            <h3>Targeted Emergency SMS Dispatch</h3>
            <p>
              State-specific broadcast engine dispatching high-priority TextBee carrier SMS and in-app feeds strictly to registered residents and disaster units within affected corridors.
            </p>
          </div>

          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>
              <WifiOff size={24} />
            </div>
            <h3>Resilient Offline Field PWA</h3>
            <p>
              IndexedDB local storage queue allowing field responders in remote Himalayan valleys to record ground fissures and road blocks without internet, auto-syncing upon reconnection.
            </p>
          </div>

          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>
              <CloudRain size={24} />
            </div>
            <h3>Future Multi-Hazard Forecasting</h3>
            <p>
              Predicts upcoming landslide probability spikes, 7-day future rainfall surges (mm), and flash flood susceptibility scores based on river discharge telemetry.
            </p>
          </div>

          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>
              <Shield size={24} />
            </div>
            <h3>Authority Response Command</h3>
            <p>
              Dedicated governance interface with state-wise jurisdiction filters, field incident verification, dispatch logging, and emergency escalation workflows.
            </p>
          </div>
        </div>
      </section>

      {/* Official Government Footer */}
      <footer className={styles.footer}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ fontWeight: '800', color: '#ffffff', fontSize: '0.95rem' }}>
              North Eastern Region Landslide Early Warning System (NER-LEWS)
            </div>
            <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '0.2rem' }}>
              Ministry of Disaster Management & Climate Resilience • Government of India
            </div>
          </div>
          <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
            NASA GLC • GPM IMERG • SRTM DEM • ESA-CCI • TextBee Gateway
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;
