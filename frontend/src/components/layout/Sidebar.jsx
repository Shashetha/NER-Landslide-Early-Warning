import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Map, 
  MapPin, 
  Bell, 
  FileText, 
  Settings,
  Mountain,
  Activity
} from 'lucide-react';
import styles from './Sidebar.module.css';

const Sidebar = ({ isOpen, onClose }) => {
  const location = useLocation();

  const navItems = [
    { path: '/dashboard', icon: LayoutDashboard, label: 'Overview' },
    { path: '/map', icon: Map, label: 'Risk Map' },
    { path: '/location-analysis', icon: MapPin, label: 'Location Analysis' },
    { path: '/alerts', icon: Bell, label: 'Alerts' },
    { path: '/reports', icon: FileText, label: 'Reports' },
    { path: '/settings', icon: Settings, label: 'Settings' }
  ];

  return (
    <aside className={`${styles.sidebar} ${isOpen ? styles.open : ''}`}>
      <div className={styles.sidebarHeader}>
        <div className={styles.sidebarLogo}>
          <Mountain className={styles.sidebarLogoIcon} />
          <span>LandGuard</span>
        </div>
      </div>

      <nav className={styles.sidebarNav}>
        {navItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`${styles.sidebarNavItem} ${
              location.pathname === item.path ? styles.active : ''
            }`}
            onClick={onClose}
          >
            <item.icon className={styles.sidebarNavIcon} />
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>

      <div className={styles.sidebarFooter}>
        <div className={styles.sidebarStatus}>
          <span className={styles.statusIndicator}></span>
          <span>System Active</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Activity size={14} />
          <span>124 locations monitored</span>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
