import { useState } from 'react';
import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer 
} from 'recharts';
import styles from './RainfallChart.module.css';

const RainfallChart = ({ data }) => {
  const [timeRange, setTimeRange] = useState('last24Hours');

  if (!data) return null;

  const currentData = data[timeRange] || [];
  const xKey = timeRange === 'last24Hours' ? 'time' : timeRange === 'last7Days' ? 'day' : 'week';

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h3 className={styles.title}>Rainfall Analytics</h3>
        <div className={styles.tabs}>
          <button 
            className={`${styles.tab} ${timeRange === 'last24Hours' ? styles.active : ''}`}
            onClick={() => setTimeRange('last24Hours')}
          >
            24h
          </button>
          <button 
            className={`${styles.tab} ${timeRange === 'last7Days' ? styles.active : ''}`}
            onClick={() => setTimeRange('last7Days')}
          >
            7d
          </button>
          <button 
            className={`${styles.tab} ${timeRange === 'last30Days' ? styles.active : ''}`}
            onClick={() => setTimeRange('last30Days')}
          >
            30d
          </button>
        </div>
      </div>

      <div className={styles.chartWrapper}>
        <ResponsiveContainer width="100%" height={260}>
          <AreaChart data={currentData}>
            <defs>
              <linearGradient id="rainfallGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
            <XAxis dataKey={xKey} stroke="#94a3b8" fontSize={12} tickLine={false} />
            <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} unit="mm" />
            <Tooltip 
              formatter={(value) => [`${value} mm`, 'Rainfall']}
              contentStyle={{ 
                borderRadius: '0.5rem', 
                border: '1px solid var(--border-color)',
                boxShadow: 'var(--shadow-md)'
              }}
            />
            <Area 
              type="monotone" 
              dataKey="rainfall" 
              stroke="#3b82f6" 
              strokeWidth={2}
              fillOpacity={1} 
              fill="url(#rainfallGradient)" 
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default RainfallChart;
