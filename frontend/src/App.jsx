import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useState } from 'react';
import Sidebar from './components/layout/Sidebar';
import Topbar from './components/layout/Topbar';
import Home from './pages/Home';
import Overview from './pages/Overview';
import RiskMapPage from './pages/RiskMapPage';
import LocationAnalysis from './pages/LocationAnalysis';
import Alerts from './pages/Alerts';
import Reports from './pages/Reports';
import AuthorityDashboard from './pages/AuthorityDashboard';
import Settings from './pages/Settings';
import './index.css';

const PAGE_TITLES = {
  '/dashboard': 'Disaster Monitoring Dashboard',
  '/map': 'GIS Landslide Risk & Threat Map',
  '/location-analysis': 'AI Multi-Hazard & Future Risk Prediction',
  '/risk-analysis': 'AI Multi-Hazard & Future Risk Prediction',
  '/alerts': 'Early Warnings & Active Alerts',
  '/reports': 'Field & Ground Hazard Reporting',
  '/authority': 'Authority Command & Disaster Management',
  '/settings': 'System Settings'
};

function AppContent() {
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const isLandingPage = location.pathname === '/';
  const currentTitle = PAGE_TITLES[location.pathname] || 'Landslide Early Warning Platform';

  if (isLandingPage) {
    return (
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    );
  }

  return (
    <div className="app-shell">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      
      {sidebarOpen && (
        <div 
          className="sidebar-backdrop" 
          onClick={() => setSidebarOpen(false)} 
        />
      )}

      <div className="app-main-wrapper">
        <Topbar 
          onMenuClick={() => setSidebarOpen(!sidebarOpen)} 
          title={currentTitle} 
        />
        <main className="app-content">
          <div className="content-inner">
            <Routes>
              <Route path="/dashboard" element={<Overview />} />
              <Route path="/map" element={<RiskMapPage />} />
              <Route path="/location-analysis" element={<LocationAnalysis />} />
              <Route path="/risk-analysis" element={<LocationAnalysis />} />
              <Route path="/alerts" element={<Alerts />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/authority" element={<AuthorityDashboard />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="*" element={<Navigate to="/dashboard" replace />} />
            </Routes>
          </div>
        </main>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
