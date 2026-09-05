export const getRiskColor = (riskLevel) => {
  const colors = {
    LOW: '#10b981',
    MEDIUM: '#f59e0b',
    HIGH: '#ef4444',
    CRITICAL: '#dc2626'
  };
  return colors[riskLevel] || colors.LOW;
};

export const getRiskClass = (riskLevel) => {
  return riskLevel.toLowerCase();
};

export const getRiskIcon = (riskLevel) => {
  const icons = {
    LOW: '🟢',
    MEDIUM: '🟠',
    HIGH: '🔴',
    CRITICAL: '🔴'
  };
  return icons[riskLevel] || icons.LOW;
};

export const formatProbability = (probability) => {
  return `${Math.round(probability * 100)}%`;
};

export const formatTimeAgo = (date) => {
  const seconds = Math.floor((new Date() - new Date(date)) / 1000);
  
  const intervals = {
    year: 31536000,
    month: 2592000,
    week: 604800,
    day: 86400,
    hour: 3600,
    minute: 60
  };
  
  for (const [unit, secondsInUnit] of Object.entries(intervals)) {
    const interval = Math.floor(seconds / secondsInUnit);
    if (interval >= 1) {
      return `${interval} ${unit}${interval > 1 ? 's' : ''} ago`;
    }
  }
  
  return 'just now';
};

export const getRiskLevelText = (probability) => {
  if (probability >= 0.85) return 'CRITICAL';
  if (probability >= 0.7) return 'HIGH';
  if (probability >= 0.5) return 'MEDIUM';
  return 'LOW';
};
