import { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Circle, CircleMarker, Popup, useMap } from 'react-leaflet';
import { Layers, Navigation, Loader2 } from 'lucide-react';
import { MapClickHandler } from './MapControls';
import { getRiskColor } from '../../utils/riskUtils';
import Button from '../common/Button';
import styles from './RiskMap.module.css';

// Smooth Map Pan/Zoom Updater
const MapCenterUpdater = ({ center, zoom }) => {
  const map = useMap();
  useEffect(() => {
    if (center && center[0] && center[1]) {
      map.setView(center, zoom || 7);
      setTimeout(() => map.invalidateSize(), 150);
    }
  }, [center, zoom, map]);
  return null;
};

// Smooth GPS FlyTo component
const GpsFlyTo = ({ trigger, coords }) => {
  const map = useMap();
  useEffect(() => {
    if (trigger && coords && coords.lat && coords.lng) {
      map.flyTo([coords.lat, coords.lng], 13, { animate: true, duration: 1.5 });
    }
  }, [trigger, coords, map]);
  return null;
};

const RiskMap = ({
  selectedLocation,
  onLocationSelect,
  riskZones = [],
  showZones = true,
  height = '500px',
  center = [26.2006, 92.9376],
  zoom = 7,
  interactive = true,
  onMapClick,
  onZoneClick
}) => {
  const [layers, setLayers] = useState({ zones: showZones, satellite: false });
  const [locating, setLocating] = useState(false);
  const [gpsCoords, setGpsCoords] = useState(null);
  const [gpsTrigger, setGpsTrigger] = useState(false);
  const [gpsError, setGpsError] = useState('');

  const mapCenter = (center && center[0] && center[1]) ? center : [26.2006, 92.9376];

  // GPS Location Finder Handler
  const handleFindMyLocation = () => {
    setGpsError('');
    if (!navigator.geolocation) {
      setGpsError('Geolocation is not supported by your browser.');
      return;
    }

    setLocating(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;
        setLocating(false);
        setGpsCoords({ lat, lng });
        setGpsTrigger(prev => !prev);

        if (onLocationSelect) onLocationSelect(lat, lng);
        if (onMapClick) onMapClick({ lat, lng });
      },
      (err) => {
        setLocating(false);
        setGpsError('Unable to retrieve GPS coordinates. Please grant location access in browser.');
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    );
  };

  return (
    <div className={styles.mapWrapper} style={{ height }}>
      <MapContainer
        center={mapCenter}
        zoom={zoom}
        style={{ height: '100%', width: '100%' }}
        className={styles.leafletContainer}
      >
        {/* OpenStreetMap Base Tiles */}
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url={
            layers.satellite
              ? 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
              : 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
          }
        />

        <MapCenterUpdater center={mapCenter} zoom={zoom} />
        <GpsFlyTo trigger={gpsTrigger} coords={gpsCoords} />

        {interactive && (
          <MapClickHandler onLocationSelect={(lat, lng) => {
            if (onLocationSelect) onLocationSelect(lat, lng);
            if (onMapClick) onMapClick({ lat, lng });
          }} />
        )}

        {/* Live GPS Location User Marker (Blue Pulse Dot) */}
        {gpsCoords && (
          <CircleMarker
            center={[gpsCoords.lat, gpsCoords.lng]}
            radius={9}
            pathOptions={{
              color: '#ffffff',
              weight: 2.5,
              fillColor: '#2563eb',
              fillOpacity: 1.0
            }}
          >
            <Popup>
              <div className={styles.popup}>
                <strong style={{ color: '#1d4ed8' }}>📍 Your Live GPS Location</strong>
                <p>Lat: {gpsCoords.lat.toFixed(5)}° N</p>
                <p>Lng: {gpsCoords.lng.toFixed(5)}° E</p>
                <p style={{ fontSize: '0.7rem', color: '#64748b' }}>Accuracy: High GPS Telemetry</p>
              </div>
            </Popup>
          </CircleMarker>
        )}

        {/* Selected Target Point (Red/Orange Dot) */}
        {selectedLocation && selectedLocation.lat && selectedLocation.lng && (
          <CircleMarker
            center={[selectedLocation.lat, selectedLocation.lng]}
            radius={8}
            pathOptions={{
              color: '#ffffff',
              weight: 2,
              fillColor: '#dc2626',
              fillOpacity: 1.0
            }}
          >
            <Popup>
              <div className={styles.popup}>
                <strong>Target Location</strong>
                <p>Lat: {selectedLocation.lat.toFixed(4)}° N</p>
                <p>Lng: {selectedLocation.lng.toFixed(4)}° E</p>
              </div>
            </Popup>
          </CircleMarker>
        )}

        {/* Risk Zones & Stations — Clean GIS Circles & Risk Dots */}
        {layers.zones && riskZones.map((zone) => {
          const zLat = zone.latitude || zone.lat;
          const zLng = zone.longitude || zone.lng;
          const level = zone.riskLevel || zone.risk_level || 'LOW';
          const prob = zone.probability || zone.risk_probability || 0.3;
          const color = getRiskColor(level);

          if (!zLat || !zLng) return null;

          return (
            <div key={zone.id || `${zLat}_${zLng}`}>
              <Circle
                center={[zLat, zLng]}
                radius={zone.radius || 2000}
                pathOptions={{
                  color: color,
                  fillColor: color,
                  fillOpacity: 0.25,
                  weight: 1.5
                }}
                eventHandlers={{
                  click: () => {
                    if (onZoneClick) onZoneClick(zone);
                  }
                }}
              >
                <Popup>
                  <div className={styles.popup}>
                    <strong>{zone.name}</strong>
                    <p>Risk: <span style={{ color: color, fontWeight: 'bold' }}>{level}</span></p>
                    <p>Probability: {Math.round(prob * 100)}%</p>
                  </div>
                </Popup>
              </Circle>

              <CircleMarker
                center={[zLat, zLng]}
                radius={5}
                pathOptions={{
                  color: '#ffffff',
                  weight: 1.5,
                  fillColor: color,
                  fillOpacity: 0.9
                }}
                eventHandlers={{
                  click: () => {
                    if (onZoneClick) onZoneClick(zone);
                  }
                }}
              >
                <Popup>
                  <div className={styles.popup}>
                    <strong>{zone.name}</strong>
                    <p>Coordinates: {zLat.toFixed(4)}°, {zLng.toFixed(4)}°</p>
                    <p>Risk: <span style={{ color: color, fontWeight: 'bold' }}>{level}</span> ({Math.round(prob * 100)}%)</p>
                    {zone.elevation_m && <p>Elevation: {zone.elevation_m} m</p>}
                    {zone.slope_degrees && <p>Slope: {zone.slope_degrees}°</p>}
                  </div>
                </Popup>
              </CircleMarker>
            </div>
          );
        })}
      </MapContainer>

      {/* Floating GIS & GPS Controls */}
      <div className={styles.mapControls}>
        <Button
          variant="primary"
          size="small"
          icon={locating ? Loader2 : Navigation}
          onClick={handleFindMyLocation}
          disabled={locating}
        >
          {locating ? 'Locating GPS...' : '📍 GPS Location Finder'}
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

      {gpsError && (
        <div className={styles.locationError}>
          <span>⚠ {gpsError}</span>
          <button onClick={() => setGpsError('')}>✕</button>
        </div>
      )}
    </div>
  );
};

export default RiskMap;
