import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { 
  Search, 
  MapPin, 
  AlertCircle, 
  CloudRain, 
  Waves, 
  Sparkles
} from 'lucide-react';
import PageHeader from '../components/layout/PageHeader';
import RiskCard from '../components/risk/RiskCard';
import RiskMap from '../components/map/RiskMap';
import Button from '../components/common/Button';
import { api } from '../services/api';
import styles from './LocationAnalysis.module.css';

const LocationAnalysis = () => {
  const [searchParams] = useSearchParams();
  
  const latParam = searchParams.get('lat');
  const lngParam = searchParams.get('lng');
  const initialLat = (latParam && !isNaN(parseFloat(latParam))) ? parseFloat(latParam) : 27.3389;
  const initialLng = (lngParam && !isNaN(parseFloat(lngParam))) ? parseFloat(lngParam) : 88.6065;

  const [selectedLocation, setSelectedLocation] = useState({ lat: initialLat, lng: initialLng });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [forecastData, setForecastData] = useState(null);
  const [forecastLoading, setForecastLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('current');

  useEffect(() => {
    if (latParam && lngParam) {
      const pLat = parseFloat(latParam);
      const pLng = parseFloat(lngParam);
      if (!isNaN(pLat) && !isNaN(pLng)) {
        setSelectedLocation({ lat: pLat, lng: pLng });
      }
    }
  }, [latParam, lngParam]);

  const runPrediction = async (lat, lng) => {
    setLoading(true);
    setError(null);
    setForecastLoading(true);

    try {
      // Direct call to api service to guarantee state update
      const pred = await api.getRiskPrediction(lat, lng);
      setPrediction(pred);
    } catch (err) {
      setError(err.message || 'Failed to predict landslide risk');
    } finally {
      setLoading(false);
    }

    try {
      const fc = await api.getMultiHazardForecast(lat, lng);
      setForecastData(fc);
    } catch (err) {
      console.error('Multi-hazard forecast error:', err);
    } finally {
      setForecastLoading(false);
    }
  };

  useEffect(() => {
    runPrediction(selectedLocation.lat, selectedLocation.lng);
  }, [selectedLocation.lat, selectedLocation.lng]);

  const handleMapClick = (latlng) => {
    setSelectedLocation({ lat: latlng.lat, lng: latlng.lng });
  };

  const handleGetLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setSelectedLocation({ lat: pos.coords.latitude, lng: pos.coords.longitude });
        },
        (err) => alert('Unable to get GPS location: ' + err.message)
      );
    }
  };

  return (
    <div className={styles.container}>
      <PageHeader
        title="AI Multi-Hazard & Future Risk Prediction"
        subtitle="Predict upcoming landslide triggers, 7-day future rainfall surges, and flash flood susceptibility"
        action={
          <div className={styles.actions}>
            <Button
              variant="secondary"
              icon={MapPin}
              onClick={handleGetLocation}
            >
              Use My Location
            </Button>
            <Button
              variant="primary"
              icon={Search}
              onClick={() => runPrediction(selectedLocation.lat, selectedLocation.lng)}
              loading={loading || forecastLoading}
            >
              Predict Multi-Hazard Risk
            </Button>
          </div>
        }
      />

      {error && (
        <div className={styles.errorBanner}>
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      <div className={styles.analysisGrid}>
        {/* Interactive Map Picker */}
        <div className={styles.mapSection}>
          <div className={styles.cardHeader}>
            <h3>Location Map Coordinates</h3>
            <p>Target: {selectedLocation.lat.toFixed(4)}° N, {selectedLocation.lng.toFixed(4)}° E</p>
          </div>
          <RiskMap
            key={`analysis_map_${selectedLocation.lat}_${selectedLocation.lng}`}
            riskZones={[
              {
                id: 'selected_marker',
                name: `Selected (${selectedLocation.lat.toFixed(4)}, ${selectedLocation.lng.toFixed(4)})`,
                latitude: selectedLocation.lat,
                longitude: selectedLocation.lng,
                riskLevel: prediction?.riskLevel || 'HIGH',
                probability: prediction?.probability || 0.85,
                radius: 2500
              }
            ]}
            onMapClick={handleMapClick}
            center={[selectedLocation.lat, selectedLocation.lng]}
            zoom={9}
            interactive={true}
          />
        </div>

        {/* Current Assessment Card */}
        <div className={styles.resultsSection}>
          <RiskCard prediction={prediction} loading={loading} />
        </div>
      </div>

      {/* ------------------------------------------------------------- */}
      {/* FUTURE RISK & MULTI-HAZARD FORECAST ENGINE (24h/48h/72h/7-Day) */}
      {/* ------------------------------------------------------------- */}
      <div style={{ background: '#ffffff', borderRadius: '8px', border: '1px solid #cbd5e1', padding: '1.75rem', marginTop: '1.5rem', boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.25rem', paddingBottom: '1rem', borderBottom: '1px solid #e2e8f0' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#1d4ed8', fontWeight: '800', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              <Sparkles size={16} />
              <span>AI Multi-Hazard Forecasting Engine</span>
            </div>
            <h2 style={{ fontSize: '1.35rem', fontWeight: '800', color: '#0f172a', marginTop: '0.2rem' }}>
              Future Landslide, Rain Surge & Flash Flood Timeline
            </h2>
          </div>

          <div style={{ display: 'flex', background: '#f1f5f9', padding: '0.25rem', borderRadius: '6px', border: '1px solid #cbd5e1' }}>
            {['current', '24h', '48h', '72h', '7d'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                style={{
                  padding: '0.4rem 0.85rem',
                  fontSize: '0.8rem',
                  fontWeight: '700',
                  borderRadius: '4px',
                  border: 'none',
                  background: activeTab === tab ? '#ffffff' : 'transparent',
                  color: activeTab === tab ? '#1d4ed8' : '#64748b',
                  boxShadow: activeTab === tab ? '0 1px 2px rgba(0,0,0,0.08)' : 'none',
                  cursor: 'pointer',
                  textTransform: 'uppercase'
                }}
              >
                {tab === 'current' ? 'Now' : (tab === '7d' ? '7-Day Trend' : `+${tab}`)}
              </button>
            ))}
          </div>
        </div>

        {forecastLoading ? (
          <div style={{ textAlign: 'center', padding: '3rem', color: '#64748b', fontWeight: '600' }}>
            Evaluating rolling precipitation models and flood susceptibility...
          </div>
        ) : forecastData ? (
          <div>
            <div style={{ background: '#f8fafc', padding: '1rem 1.25rem', borderRadius: '6px', border: '1px solid #cbd5e1', borderLeft: '4px solid #1d4ed8', marginBottom: '1.5rem', fontSize: '0.875rem', color: '#334155', lineHeight: '1.5' }}>
              <strong>AI Regional Advisory:</strong> {forecastData.summary_advisory}
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
              {(forecastData.timeline_7d || []).map((win, idx) => {
                const isPeak = win.date_label === forecastData.peak_hazard_day;
                const landRisk = win.landslide_risk_level;
                const floodRisk = win.flash_flood_risk;

                return (
                  <div
                    key={idx}
                    style={{
                      background: isPeak ? '#fef2f2' : '#ffffff',
                      border: '1px solid',
                      borderColor: isPeak ? '#fca5a5' : '#e2e8f0',
                      borderTop: `4px solid ${landRisk === 'CRITICAL' ? '#b91c1c' : landRisk === 'HIGH' ? '#ea580c' : landRisk === 'MEDIUM' ? '#d97706' : '#047857'}`,
                      borderRadius: '8px',
                      padding: '1.1rem',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '0.65rem',
                      boxShadow: '0 1px 2px rgba(0,0,0,0.05)'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontWeight: '800', fontSize: '0.85rem', color: '#0f172a' }}>{win.horizon}</span>
                      <span style={{ fontSize: '0.7rem', color: '#64748b', fontWeight: '600' }}>{win.date_label}</span>
                    </div>

                    <div style={{ background: '#f8fafc', padding: '0.5rem', borderRadius: '4px', border: '1px solid #e2e8f0' }}>
                      <div style={{ fontSize: '0.7rem', color: '#64748b', fontWeight: '700', textTransform: 'uppercase' }}>Landslide Risk</div>
                      <div style={{ fontSize: '1rem', fontWeight: '800', color: landRisk === 'CRITICAL' ? '#b91c1c' : landRisk === 'HIGH' ? '#ea580c' : '#047857' }}>
                        {landRisk} ({Math.round(win.landslide_probability * 100)}%)
                      </div>
                    </div>

                    <div style={{ background: '#f8fafc', padding: '0.5rem', borderRadius: '4px', border: '1px solid #e2e8f0' }}>
                      <div style={{ fontSize: '0.7rem', color: '#64748b', fontWeight: '700', textTransform: 'uppercase' }}>Flash Flood</div>
                      <div style={{ fontSize: '0.9rem', fontWeight: '800', color: floodRisk === 'CRITICAL' || floodRisk === 'HIGH' ? '#b91c1c' : '#0284c7' }}>
                        {floodRisk} Risk
                      </div>
                    </div>

                    <div style={{ fontSize: '0.75rem', color: '#475569', display: 'flex', flexDirection: 'column', gap: '0.2rem', marginTop: '0.25rem' }}>
                      <span style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                        <CloudRain size={13} color="#2563eb" /> Rain Surge: <strong>{win.rainfall_surge_mm} mm</strong>
                      </span>
                      <span style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                        <Waves size={13} color="#0891b2" /> 3d Rain Sum: <strong>{win.cumulative_3d_rain_mm} mm</strong>
                      </span>
                      <span>Soil Saturation: <strong>{win.soil_moisture_pct}%</strong></span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: '2rem', color: '#94a3b8' }}>
            Click "Predict Multi-Hazard Risk" above to calculate 7-day predictive models for this coordinate.
          </div>
        )}
      </div>
    </div>
  );
};

export default LocationAnalysis;
