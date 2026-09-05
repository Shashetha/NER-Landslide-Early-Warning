import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, MapPin, Layers, Crosshair } from 'lucide-react';
import PageHeader from '../components/layout/PageHeader';
import RiskMap from '../components/map/RiskMap';
import Button from '../components/common/Button';
import RiskBadge from '../components/risk/RiskBadge';
import { api } from '../services/api';
import styles from './RiskMapPage.module.css';

const RiskMapPage = () => {
  const navigate = useNavigate();
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [riskZones, setRiskZones] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const fetchZones = async () => {
      try {
        const zones = await api.getRiskZones();
        setRiskZones(zones);
      } catch (err) {
        console.error('Error fetching risk zones:', err);
      }
    };
    fetchZones();
  }, []);

  const handleLocationSelect = (lat, lng) => {
    setSelectedLocation({ lat, lng });
  };

  const handleAnalyzeClick = () => {
    if (selectedLocation) {
      navigate(`/location-analysis?lat=${selectedLocation.lat}&lng=${selectedLocation.lng}`);
    }
  };

  return (
    <div className={styles.container}>
      <PageHeader
        title="Interactive Geospatial Risk Map"
        subtitle="Explore regional hazard overlays, live precipitation alerts, and active landslide zones."
      />

      <div className={styles.mapCard}>
        <div className={styles.toolbar}>
          <div className={styles.searchBox}>
            <Search size={18} className={styles.searchIcon} />
            <input
              type="text"
              placeholder="Search location, valley or hills..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <div className={styles.legend}>
            <span className={styles.legendItem}><span className={`${styles.dot} ${styles.low}`}></span> Low Risk</span>
            <span className={styles.legendItem}><span className={`${styles.dot} ${styles.medium}`}></span> Medium</span>
            <span className={styles.legendItem}><span className={`${styles.dot} ${styles.high}`}></span> High Risk</span>
            <span className={styles.legendItem}><span className={`${styles.dot} ${styles.critical}`}></span> Critical</span>
          </div>
        </div>

        <div className={styles.mapContainer}>
          <RiskMap
            selectedLocation={selectedLocation}
            onLocationSelect={handleLocationSelect}
            riskZones={riskZones}
            height="600px"
          />

          {selectedLocation && (
            <div className={styles.locationOverlay}>
              <div className={styles.overlayHeader}>
                <MapPin size={18} className={styles.pinIcon} />
                <h4>Selected Coordinates</h4>
              </div>
              <div className={styles.coords}>
                <div><span>Lat:</span> {selectedLocation.lat.toFixed(6)}</div>
                <div><span>Lng:</span> {selectedLocation.lng.toFixed(6)}</div>
              </div>
              <Button
                variant="primary"
                fullWidth
                size="small"
                onClick={handleAnalyzeClick}
              >
                Perform AI Analysis
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default RiskMapPage;
