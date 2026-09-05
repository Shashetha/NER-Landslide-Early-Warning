import { useState, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle, useMap } from 'react-leaflet';
import { Navigation, Layers, Loader2 } from 'lucide-react';
import { MapClickHandler } from './MapControls';
import { getRiskColor } from '../../utils/riskUtils';
import Button from '../common/Button';
import styles from './RiskMap.module.css';

// Inner component — runs inside MapContainer so useMap() works
const LocationFlyTo = ({ trigger, coords }) => {
  const map = useMap();
  if (trigger && coords) {
    map.flyTo([coords.lat, coords.lng], 14, { animate: true, duration: 1.2 });
  }
  return null;
};

const RiskMap = ({
  selectedLocation,
  onLocationSelect,
  riskZones = [],
  showZones = true,
  height = '500px',
  center = [26.2006, 92.9376],
  zoom = 7
}) => {
  const [layers, setLayers] = useState({ zones: showZones, satellite: false });
  const [locating, setLocating] = useState(false);
  const [locError, setLocError] = useState('');
  const [flyTarget, setFlyTarget] = useState(null);
  const [flyTrigger, setFlyTrigger] = useState(false);

  const handleUseMyLocation = () => {
    setLocError('');

    if (!navigator.geolocation) {
      setLocError('Geolocation is not supported by this browser.');
      return;
    }

    setLocating(true);

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;

        // Pass to parent for marker + analysis
        onLocationSelect(lat, lng);

        // Fly map to user location
        setFlyTarget({ lat, lng });
        setFlyTrigger(prev => !prev);

        setLocating(false);
      },
      (error) => {
        setLocating(false);
        switch (error.code) {
          case error.PERMISSION_DENIED:
            setLocError('Location permission denied. Please allow location access in your browser and try again.');
            break;
          case error.POSITION_UNAVAILABLE:
            setLocError('Location unavailable. Please select a point on the map manually.');
            break;
          case error.TIMEOUT:
            setLocError('Location request timed out. Please try again.');
            break;
          default:
            setLocError('Unable to get your location. Please select a point on the map manually.');
        }
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0
      }
    );
  };

  return (
    <div className={styles.mapWrapper} style={{ height }}>
      <MapContainer
        center={center}
        zoom={zoom}
        style={{ height: '100%', width: '100%' }}
        className={styles.leafletContainer}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url={
            layers.satellite
              ? 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
              : 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
          }
        />

        <MapClickHandler onLocationSelect={onLocationSelect} />

        {/* Fly to user location when triggered */}
        <LocationFlyTo trigger={flyTrigger} coords={flyTarget} />

        {selectedLocation && (
          <Marker position={[selectedLocation.lat, selectedLocation.lng]}>
            <Popup>
              <div className={styles.popup}>
                <strong>Selected Location</strong>
                <p>Lat: {selectedLocation.lat.toFixed(6)}</p>
                <p>Lng: {selectedLocation.lng.toFixed(6)}</p>
              </div>
            </Popup>
          </Marker>
        )}

        {layers.zones && riskZones.map((zone) => (
          <Circle
            key={zone.id}
            center={[zone.latitude, zone.longitude]}
            radius={zone.radius}
            pathOptions={{
              color: getRiskColor(zone.riskLevel),
              fillColor: getRiskColor(zone.riskLevel),
              fillOpacity: 0.3
            }}
          >
            <Popup>
              <div className={styles.popup}>
                <strong>{zone.name}</strong>
                <p>Risk: <span style={{ color: getRiskColor(zone.riskLevel), fontWeight: 'bold' }}>{zone.riskLevel}</span></p>
                <p>Probability: {Math.round(zone.probability * 100)}%</p>
              </div>
            </Popup>
          </Circle>
        ))}
      </MapContainer>

      <div className={styles.mapControls}>
        <Button
          variant="secondary"
          size="small"
          icon={locating ? Loader2 : Navigation}
          onClick={handleUseMyLocation}
          disabled={locating}
        >
          {locating ? 'Locating...' : 'My Location'}
        </Button>
        <Button
          variant="secondary"
          size="small"
          icon={Layers}
          onClick={() => setLayers(prev => ({ ...prev, satellite: !prev.satellite }))}
        >
          {layers.satellite ? 'Map View' : 'Satellite'}
        </Button>
      </div>

      {locError && (
        <div className={styles.locationError}>
          <span>⚠ {locError}</span>
          <button onClick={() => setLocError('')}>✕</button>
        </div>
      )}
    </div>
  );
};

export default RiskMap;
