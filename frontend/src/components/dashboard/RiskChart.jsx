import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import styles from './RiskChart.module.css';

const RiskChart = ({ data }) => {
  if (!data) return null;

  const chartData = [
    { name: 'Low Risk', value: data.low, color: '#10b981' },
    { name: 'Medium Risk', value: data.medium, color: '#f59e0b' },
    { name: 'High Risk', value: data.high, color: '#ef4444' },
    { name: 'Critical', value: data.critical, color: '#dc2626' }
  ];

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>Risk Distribution</h3>
      <div className={styles.chartWrapper}>
        <ResponsiveContainer width="100%" height={260}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={90}
              paddingAngle={4}
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip 
              formatter={(value) => [`${value}%`, 'Locations']}
              contentStyle={{ 
                borderRadius: '0.5rem', 
                border: '1px solid var(--border-color)',
                boxShadow: 'var(--shadow-md)'
              }}
            />
            <Legend verticalAlign="bottom" height={36} />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default RiskChart;
