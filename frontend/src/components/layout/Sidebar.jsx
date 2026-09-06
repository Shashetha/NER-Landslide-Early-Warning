import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Map, 
  Search, 
  Bell, 
  FileText, 
  ShieldAlert, 
  Settings as SettingsIcon, 
  Activity 
} from 'lucide-react';
import styles from './Sidebar.module.css';

const Sidebar = ({ isOpen, onClose }) => {
  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/map', label: 'GIS Risk Map', icon: Map },
    { path: '/location-analysis', label: 'Risk Analysis', icon: Search },
    { path: '/alerts', label: 'Early Warnings', icon: Bell },
    { path: '/reports', label: 'Field Reports', icon: FileText },
    { path: '/authority', label: 'Authority Command', icon: ShieldAlert },
    { path: '/settings', label: 'System Settings', icon: SettingsIcon },
  ];

  return (
    <aside className={`${styles.sidebar} ${isOpen ? styles.open : ''}`}>
      <div className={styles.sidebarHeader}>
        <div className={styles.sidebarLogo}>
          <Activity className={styles.sidebarLogoIcon} />
          <span>NER Early Warning</span>
        </div>
      </div>

      <nav className={styles.sidebarNav}>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              onClick={onClose}
              className={({ isActive }) =>
                `${styles.sidebarNavItem} ${isActive ? styles.active : ''}`
              }
            >
              <Icon className={styles.sidebarNavIcon} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className={styles.sidebarFooter}>
        <div className={styles.sidebarStatus}>
          <div className={styles.statusIndicator} />
          <span>AI Telemetry: Live</span>
        </div>
        <span>North East Region Platform</span>
      </div>
    </aside>
  );
};

export default Sidebar;
