# LandGuard AI — Landslide Risk Monitoring & Early Warning System

A modern, responsive, multi-page React geospatial dashboard application designed for disaster monitoring agencies, local administration, and community early warning.

## 🚀 Features

- **Geospatial Risk Mapping**: Interactive Leaflet map with OpenStreetMap/Satellite toggle, risk zone circles, and custom location markers.
- **AI-Driven Risk Scoring**: Point-based coordinate analysis simulating predictions with confidence metrics and environmental factor breakdowns.
- **Dynamic Analytics Dashboard**: Recharts-powered rainfall trends (24h/7d/30d), regional risk distributions, and key performance stats.
- **Incident Reporting**: Crowd-sourced hazard reporting modal for mudflows, cracks, and soil erosion with ground-truth logging.
- **Alert Dispatch Center**: Filterable, searchable emergency alerts based on population exposure and threat levels.
- **Extensible API Service Layer**: Centralized `api.js` abstraction ready to swap mock promises for FastAPI REST endpoints.

## 🛠️ Tech Stack

- **Framework**: React 18 + Vite
- **Routing**: React Router v6
- **Maps**: Leaflet + React-Leaflet + OpenStreetMap
- **Icons**: Lucide React
- **Charts**: Recharts
- **Styling**: CSS Modules + Global Variables

## 📦 Getting Started

```bash
cd landslide-monitoring
npm install
npm run dev
```

Navigate to `http://localhost:5173` in your browser.

## 🔌 Future Backend Integration

All API interactions are consolidated in `src/services/api.js`. To connect to a live FastAPI server, update `API_BASE_URL` and replace mock responses with `fetch()` calls against your `/api/v1/predictions` and `/api/v1/reports` endpoints.
