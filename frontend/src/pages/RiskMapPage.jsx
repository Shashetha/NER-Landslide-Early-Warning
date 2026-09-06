import { useState, useEffect } from 'react';
import { 
  Layers, 
  Filter, 
  MapPin, 
  AlertTriangle, 
  Search, 
  SlidersHorizontal,
  Flame,
  Activity,
  History,
  RotateCw,
  ExternalLink
} from 'lucide-react';
import PageHeader from '../components/layout/PageHeader';
import RiskMap from '../components/map/RiskMap';
import Button from '../components/common/Button';
import { api } from '../services/api';
import styles from './RiskMapPage.module.css';

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

const RiskMapPage = () => {
  const [riskPoints, setRiskPoints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedPoint, setSelectedPoint] = useState(null);
  const [filterLevel, setFilterLevel] = useState('ALL');
  const [filterState, setFilterState] = useState('ALL');
  const [mapCenter, setMapCenter] = useState([26.2006, 92.9376]);
  const [mapZoom, setMapZoom] = useState(7);

  const loadRiskMapData = async () => {
    setLoading(true);
    try {
      const res = await api.getRiskZones();
      setRiskPoints(res || []);
    } catch (error) {
      console.error('Failed to load risk map data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRiskMapData();
  }, []);

  const handleStateChange = (newState) => {
    setFilterState(newState);
    if (STATE_COORDINATES[newState]) {
      setMapCenter(STATE_COORDINATES[newState].center);
      setMapZoom(STATE_COORDINATES[newState].zoom);
    }
  };

  const filteredPoints = riskPoints.filter((point) => {
    const matchesSearch = (point.name && point.name.toLowerCase().includes(searchQuery.toLowerCase())) ||
                          (point.state && point.state.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesLevel = filterLevel === 'ALL' || (point.riskLevel || point.risk_level || '').toUpperCase() === filterLevel;
    const matchesState = filterState === 'ALL' || (point.state && point.state.toLowerCase() === filterState.toLowerCase());

    return matchesSearch && matchesLevel && matchesState;
  });

  const nerStates = ['ALL', 'Sikkim', 'Meghalaya', 'Arunachal Pradesh', 'Nagaland', 'Manipur', 'Mizoram', 'Assam', 'Tripura'];

  return (
    <div className={styles.container}>
      <PageHeader
        title="Interactive GIS Landslide Risk & Threat Map"
        subtitle="Real-time multi-hazard risk map with automatic regional zooming across 8 North-Eastern states"
        action={
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <Button
              variant="secondary"
              size="small"
              icon={RotateCw}
              onClick={loadRiskMapData}
              loading={loading}
            >
              Refresh Telemetry
            </Button>
          </div>
        }
      />

      <div className={styles.mapCard}>
        {/* Top Operational Filter Bar */}
        <div className={styles.toolbar}>
          <div className={styles.searchBox}>
            <Search size={18} className={styles.searchIcon} />
            <input
              type="text"
              placeholder="Search station, corridor, state..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center', flexWrap: 'wrap' }}>
            {/* Automatic State Focus Selector */}
            <select
              value={filterState}
              onChange={(e) => handleStateChange(e.target.value)}
              style={{ padding: '0.4rem 0.75rem', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '0.85rem', fontWeight: '700', color: '#0f172a', background: '#ffffff', cursor: 'pointer' }}
            >
              {nerStates.map(st => (
                <option key={st} value={st}>{st === 'ALL' ? '🗺️ Focus: All 8 NER States' : `📍 Focus: ${st}`}</option>
              ))}
            </select>

            {/* Risk Level Filter */}
            <select
              value={filterLevel}
              onChange={(e) => setFilterLevel(e.target.value)}
              style={{ padding: '0.4rem 0.75rem', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '0.85rem', fontWeight: '700', color: '#0f172a', background: '#ffffff' }}
            >
              <option value="ALL">All Risk Levels</option>
              <option value="CRITICAL">Critical (80–100%)</option>
              <option value="HIGH">High (60–80%)</option>
              <option value="MEDIUM">Moderate (30–60%)</option>
              <option value="LOW">Low / Safe (0–30%)</option>
            </select>
          </div>
        </div>

        {/* Map View */}
        <div className={styles.mapContainer}>
          <RiskMap
            riskZones={filteredPoints}
            onZoneClick={(pt) => setSelectedPoint(pt)}
            center={mapCenter}
            zoom={mapZoom}
            height="620px"
          />

          {/* Selected Point Inspector Modal Overlay */}
          {selectedPoint && (
            <div className={styles.locationOverlay}>
              <div className={styles.overlayHeader}>
                <MapPin size={18} className={styles.pinIcon} />
                <h4>{selectedPoint.name || 'Hazard Point'}</h4>
              </div>
              
              <div style={{ 
                fontSize: '0.75rem', 
                fontWeight: '800', 
                padding: '0.2rem 0.5rem', 
                borderRadius: '4px', 
                background: (selectedPoint.probability || 0.8) >= 0.75 ? '#fee2e2' : (selectedPoint.probability || 0.8) >= 0.55 ? '#ffedd5' : (selectedPoint.probability || 0.8) >= 0.35 ? '#fef3c7' : '#ecfdf5', 
                color: (selectedPoint.probability || 0.8) >= 0.75 ? '#b91c1c' : (selectedPoint.probability || 0.8) >= 0.55 ? '#ea580c' : (selectedPoint.probability || 0.8) >= 0.35 ? '#b45309' : '#047857', 
                display: 'inline-block', 
                marginBottom: '0.6rem' 
              }}>
                {selectedPoint.riskLevel || selectedPoint.risk_level || 'HIGH'} ({Math.round((selectedPoint.probability || selectedPoint.risk_probability || 0.8) * 100)}% Probability)
              </div>

              <div className={styles.coords}>
                <div><span>Latitude:</span> {selectedPoint.latitude?.toFixed(4)}° N</div>
                <div><span>Longitude:</span> {selectedPoint.longitude?.toFixed(4)}° E</div>
                {selectedPoint.elevation_m && <div><span>Elevation:</span> {selectedPoint.elevation_m} m</div>}
                {selectedPoint.slope_degrees && <div><span>Slope Angle:</span> {selectedPoint.slope_degrees}°</div>}
                {selectedPoint.rainfall_7d && <div><span>7-Day Rain:</span> {selectedPoint.rainfall_7d} mm</div>}
                {selectedPoint.soil_moisture && <div><span>Soil Moisture:</span> {Math.round(selectedPoint.soil_moisture * 100)}% Saturation</div>}
                <div><span>Last Updated:</span> Live Telemetry</div>
              </div>

              <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem' }}>
                <Button
                  variant="primary"
                  size="small"
                  fullWidth
                  icon={ExternalLink}
                  onClick={() => {
                    window.location.href = `/location-analysis?lat=${selectedPoint.latitude}&lng=${selectedPoint.longitude}`;
                  }}
                >
                  Analyze 7-Day Forecast
                </Button>
                <Button
                  variant="secondary"
                  size="small"
                  onClick={() => setSelectedPoint(null)}
                >
                  Close
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default RiskMapPage;
