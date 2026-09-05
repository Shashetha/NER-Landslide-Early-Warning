import { Link } from 'react-router-dom';
import { 
  MapPin, 
  Cpu, 
  CloudRain, 
  Bell, 
  ArrowRight, 
  ShieldCheck, 
  BarChart3,
  Layers
} from 'lucide-react';
import Button from '../components/common/Button';
import styles from './Home.module.css';

const Home = () => {
  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <div className={styles.logo}>
          <ShieldCheck size={32} className={styles.logoIcon} />
          <span>LandGuard AI</span>
        </div>
        <div className={styles.headerActions}>
          <Link to="/dashboard">
            <Button variant="primary">Launch Platform</Button>
          </Link>
        </div>
      </header>

      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <span className={styles.badge}>Next-Gen Disaster Risk Reduction</span>
          <h1 className={styles.title}>
            Predict Landslide Risk <br />
            <span>Before It Becomes a Disaster</span>
          </h1>
          <p className={styles.subtitle}>
            AI-powered environmental monitoring, geospatial modeling, and real-time early warning system designed for vulnerable communities and disaster managers.
          </p>
          <div className={styles.heroButtons}>
            <Link to="/map">
              <Button size="large" icon={MapPin}>Explore Risk Map</Button>
            </Link>
            <Link to="/location-analysis">
              <Button size="large" variant="secondary">Analyze a Location</Button>
            </Link>
          </div>
        </div>
      </section>

      <section className={styles.features}>
        <div className={styles.sectionHeader}>
          <h2>Key Capabilities</h2>
          <p>Comprehensive risk intelligence backed by multi-source data fusion</p>
        </div>
        <div className={styles.featuresGrid}>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}><MapPin size={24} /></div>
            <h3>Real-Time Risk Mapping</h3>
            <p>Interactive spatial view of regional hazards with live overlay of risk zones and rainfall data.</p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}><Cpu size={24} /></div>
            <h3>AI Risk Prediction</h3>
            <p>Advanced machine learning models predicting slide probabilities from terrain and weather inputs.</p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}><CloudRain size={24} /></div>
            <h3>Environmental Monitoring</h3>
            <p>Live tracking of soil saturation, cumulative precipitation, slope angles, and elevation dynamics.</p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}><Bell size={24} /></div>
            <h3>Early Warning Alerts</h3>
            <p>Automated threshold monitoring dispatching instant alerts to responders and stakeholders.</p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}><Layers size={24} /></div>
            <h3>Location Analysis</h3>
            <p>Deep dive into specific coordinates with confidence-scored risk metrics and actionable insights.</p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}><BarChart3 size={24} /></div>
            <h3>Historical Analytics</h3>
            <p>Analyze precipitation trends and seasonal risk shifts to bolster disaster readiness strategies.</p>
          </div>
        </div>
      </section>

      <section className={styles.howItWorks}>
        <div className={styles.sectionHeader}>
          <h2>How It Works</h2>
          <p>A continuous 4-step intelligence pipeline</p>
        </div>
        <div className={styles.stepsGrid}>
          <div className={styles.stepCard}>
            <span className={styles.stepNumber}>01</span>
            <h3>Select Location</h3>
            <p>Pick coordinates via interactive map or device GPS.</p>
          </div>
          <div className={styles.stepCard}>
            <span className={styles.stepNumber}>02</span>
            <h3>Collect Data</h3>
            <p>Pull live rainfall, soil moisture, and slope topography.</p>
          </div>
          <div className={styles.stepCard}>
            <span className={styles.stepNumber}>03</span>
            <h3>AI Predicts Risk</h3>
            <p>ML models estimate probability and identify key triggers.</p>
          </div>
          <div className={styles.stepCard}>
            <span className={styles.stepNumber}>04</span>
            <h3>Early Warning</h3>
            <p>Issue targeted warnings to safeguard human lives.</p>
          </div>
        </div>
      </section>

      <footer className={styles.footer}>
        <p>&copy; 2026 LandGuard AI Early Warning System. Built for Hackathons & Disaster Reduction.</p>
      </footer>
    </div>
  );
};

export default Home;
