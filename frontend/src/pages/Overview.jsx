import { useState, useEffect } from 'react';
import { 
  MapPin, 
  AlertTriangle, 
  Bell, 
  FileText, 
  RefreshCw,
  TrendingUp,
  ShieldAlert,
  CloudRain
} from 'lucide-react';
import PageHeader from '../components/layout/PageHeader';
import StatCard from '../components/dashboard/StatCard';
import RiskChart from '../components/dashboard/RiskChart';
import RainfallChart from '../components/dashboard/RainfallChart';
import RecentAlerts from '../components/dashboard/RecentAlerts';
import Button from '../components/common/Button';
import Loader from '../components/common/Loader';
import { api } from '../services/api';
import styles from './Overview.module.css';

const Overview = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchData = async () => {
    try {
      const result = await api.getDashboardData();
      setData(result);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleRefresh = () => {
    setRefreshing(true);
    fetchData();
  };

  if (loading) {
    return <Loader text="Loading monitoring data..." size="large" />;
  }

  const { statistics, riskDistribution, rainfallData, recentAlerts } = data;

  return (
    <div className={styles.container}>
      <PageHeader
        title="Landslide Monitoring Overview"
        subtitle="Real-time environmental data and AI-driven risk analytics for North East India"
        action={
          <Button
            variant="secondary"
            icon={RefreshCw}
            loading={refreshing}
            onClick={handleRefresh}
          >
            Refresh Data
          </Button>
        }
      />

      {/* Emergency Alert Banner */}
      <div className={styles.alertBanner}>
        <div className={styles.bannerIcon}>
          <ShieldAlert size={22} />
        </div>
        <div className={styles.bannerText}>
          <strong>Severe Weather Alert: Heavy Rainfall in North East India</strong>
          <span>High landslide hazard warnings issued across Sikkim, Meghalaya, and Arunachal Pradesh. Responders on standby.</span>
        </div>
      </div>

      <div className={styles.statsGrid}>
        <StatCard
          title="Monitored Locations"
          value={statistics.monitoredLocations}
          icon={MapPin}
          color="blue"
        />
        <StatCard
          title="High Risk Areas"
          value={statistics.highRiskAreas}
          icon={AlertTriangle}
          color="red"
          trend={12}
        />
        <StatCard
          title="Active Alerts"
          value={statistics.activeAlerts}
          icon={Bell}
          color="amber"
        />
        <StatCard
          title="Reports Today"
          value={statistics.reportsToday}
          icon={FileText}
          color="green"
        />
      </div>

      <div className={styles.chartsGrid}>
        <div className={styles.mainChart}>
          <RainfallChart data={rainfallData} />
        </div>
        <div className={styles.sideChart}>
          <RiskChart data={riskDistribution} />
        </div>
      </div>

      <div className={styles.bottomSection}>
        <RecentAlerts alerts={recentAlerts} />
      </div>
    </div>
  );
};

export default Overview;
