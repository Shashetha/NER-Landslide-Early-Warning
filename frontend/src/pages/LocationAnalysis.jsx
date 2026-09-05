import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Play, RotateCcw, AlertTriangle } from 'lucide-react';
import PageHeader from '../components/layout/PageHeader';
import RiskMap from '../components/map/RiskMap';
import RiskCard from '../components/risk/RiskCard';
import Button from '../components/common/Button';
import { useRiskPrediction } from '../hooks/useRiskPrediction';
import styles from './LocationAnalysis.module.css';

const LocationAnalysis = () => {
  const [searchParams] = useSearchParams();
  const [selectedLocation, setSelectedLocation] = useState(null);
  const { prediction, loading, error, analyzeLocation, clearPrediction } = useRiskPrediction();

  useEffect(() => {
    const lat = searchParams.get('lat');
    const lng = searchParams.get('lng');
    if (lat && lng) {
      const location = { lat: parseFloat(lat), lng: parseFloat(lng) };
      setSelectedLocation(location);
      analyzeLocation(location.lat, location.lng);
    }
  }, [searchParams]);

  const handleLocationSelect = (lat, lng) => {
    setSelectedLocation({ lat, lng });
  };

  const handleRunAnalysis = () => {
    if (selectedLocation) {
      analyzeLocation(selectedLocation.lat, selectedLocation.lng);
    }
  };

  const handleReset = () => {
    setSelectedLocation(null);
    clearPrediction();
  };

  return (
    <div className={styles.container}>
      <PageHeader
        title="Location Risk Analysis"
        subtitle="Point-based terrain evaluation and deep environmental hazard scoring"
        action={
          <div className={styles.actions}>
            {selectedLocation && (
              <Button
                variant="secondary"
                icon={RotateCcw}
                onClick={handleReset}
                disabled={loading}
              >
                Reset
              </Button>
            )}
            <Button
              variant="primary"
              icon={Play}
              onClick={handleRunAnalysis}
              disabled={!selectedLocation || loading}
              loading={loading}
            >
              Analyze Location
            </Button>
          </div>
        }
      />

      {error && (
        <div className={styles.errorBanner}>
          <AlertTriangle size={20} />
          <span>{error}</span>
        </div>
      )}

      <div className={styles.analysisGrid}>
        <div className={styles.mapSection}>
          <div className={styles.cardHeader}>
            <h3>Geospatial Picker</h3>
            <p>Click on the terrain to set coordinates</p>
          </div>
          <RiskMap
            selectedLocation={selectedLocation}
            onLocationSelect={handleLocationSelect}
            height="460px"
          />
        </div>

        <div className={styles.resultsSection}>
          <RiskCard prediction={prediction} loading={loading} />
        </div>
      </div>
    </div>
  );
};

export default LocationAnalysis;
