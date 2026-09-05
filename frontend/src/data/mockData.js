export const mockDashboardData = {
  statistics: {
    monitoredLocations: 124,
    highRiskAreas: 18,
    activeAlerts: 7,
    reportsToday: 36
  },
  riskDistribution: {
    low: 58,
    medium: 24,
    high: 13,
    critical: 5
  },
  rainfallData: {
    last24Hours: [
      { time: '00:00', rainfall: 12 },
      { time: '03:00', rainfall: 18 },
      { time: '06:00', rainfall: 25 },
      { time: '09:00', rainfall: 32 },
      { time: '12:00', rainfall: 28 },
      { time: '15:00', rainfall: 35 },
      { time: '18:00', rainfall: 42 },
      { time: '21:00', rainfall: 38 }
    ],
    last7Days: [
      { day: 'Mon', rainfall: 45 },
      { day: 'Tue', rainfall: 52 },
      { day: 'Wed', rainfall: 38 },
      { day: 'Thu', rainfall: 65 },
      { day: 'Fri', rainfall: 78 },
      { day: 'Sat', rainfall: 85 },
      { day: 'Sun', rainfall: 92 }
    ],
    last30Days: [
      { week: 'Week 1', rainfall: 245 },
      { week: 'Week 2', rainfall: 312 },
      { week: 'Week 3', rainfall: 285 },
      { week: 'Week 4', rainfall: 398 }
    ]
  },
  recentAlerts: [
    {
      id: 1,
      location: 'Gangtok, Sikkim',
      riskLevel: 'HIGH',
      probability: 0.87,
      timestamp: new Date(Date.now() - 12 * 60 * 1000),
      latitude: 27.3389,
      longitude: 88.6065
    },
    {
      id: 2,
      location: 'Cherrapunji, Meghalaya',
      riskLevel: 'CRITICAL',
      probability: 0.94,
      timestamp: new Date(Date.now() - 28 * 60 * 1000),
      latitude: 25.2630,
      longitude: 91.7324
    },
    {
      id: 3,
      location: 'Itanagar, Arunachal Pradesh',
      riskLevel: 'HIGH',
      probability: 0.79,
      timestamp: new Date(Date.now() - 45 * 60 * 1000),
      latitude: 27.0844,
      longitude: 93.6053
    },
    {
      id: 4,
      location: 'Kohima, Nagaland',
      riskLevel: 'MEDIUM',
      probability: 0.65,
      timestamp: new Date(Date.now() - 65 * 60 * 1000),
      latitude: 25.6747,
      longitude: 94.1106
    },
    {
      id: 5,
      location: 'Shillong, Meghalaya',
      riskLevel: 'MEDIUM',
      probability: 0.58,
      timestamp: new Date(Date.now() - 92 * 60 * 1000),
      latitude: 25.5788,
      longitude: 91.8933
    }
  ]
};

export const mockRiskPrediction = (lat, lng) => {
  const probability = Math.random() * 0.6 + 0.3;
  let riskLevel = 'LOW';
  
  if (probability >= 0.85) riskLevel = 'CRITICAL';
  else if (probability >= 0.7) riskLevel = 'HIGH';
  else if (probability >= 0.5) riskLevel = 'MEDIUM';

  return {
    predictionId: Math.random().toString(36).substr(2, 9),
    latitude: lat,
    longitude: lng,
    riskLevel,
    probability,
    confidence: Math.random() * 0.2 + 0.8,
    features: {
      rainfall: Math.round(Math.random() * 200 + 50),
      slope: Math.round(Math.random() * 40 + 10),
      elevation: Math.round(Math.random() * 2000 + 500),
      soilMoisture: Math.round(Math.random() * 50 + 30),
      temperature: Math.round(Math.random() * 15 + 10)
    },
    explanation: generateRiskExplanation(riskLevel),
    timestamp: new Date()
  };
};

const generateRiskExplanation = (riskLevel) => {
  const explanations = {
    LOW: 'Current environmental conditions indicate stable terrain with minimal landslide risk. Continue regular monitoring.',
    MEDIUM: 'Moderate risk detected due to recent rainfall. Terrain stability should be monitored closely over the next 24-48 hours.',
    HIGH: 'High rainfall combined with steep terrain and elevated soil moisture is increasing the probability of landslide activity. Enhanced monitoring recommended.',
    CRITICAL: 'Critical risk levels detected. Immediate evacuation procedures should be considered. Multiple environmental factors indicate imminent landslide danger.'
  };
  return explanations[riskLevel];
};

export const mockAlerts = [
  {
    id: 1,
    location: 'Gangtok, Sikkim',
    latitude: 27.3389,
    longitude: 88.6065,
    riskLevel: 'HIGH',
    probability: 0.87,
    status: 'active',
    createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000),
    updatedAt: new Date(Date.now() - 12 * 60 * 1000),
    affectedPopulation: 2500,
    description: 'Heavy rainfall detected in the area with steep slope conditions.'
  },
  {
    id: 2,
    location: 'Cherrapunji, Meghalaya',
    latitude: 25.2630,
    longitude: 91.7324,
    riskLevel: 'CRITICAL',
    probability: 0.94,
    status: 'active',
    createdAt: new Date(Date.now() - 4 * 60 * 60 * 1000),
    updatedAt: new Date(Date.now() - 30 * 60 * 1000),
    affectedPopulation: 5200,
    description: 'Critical conditions detected. Multiple risk factors present in wettest place on Earth.'
  },
  {
    id: 3,
    location: 'Itanagar, Arunachal Pradesh',
    latitude: 27.0844,
    longitude: 93.6053,
    riskLevel: 'HIGH',
    probability: 0.79,
    status: 'active',
    createdAt: new Date(Date.now() - 6 * 60 * 60 * 1000),
    updatedAt: new Date(Date.now() - 45 * 60 * 1000),
    affectedPopulation: 1800,
    description: 'Elevated soil moisture levels detected in hilly terrain.'
  },
  {
    id: 4,
    location: 'Shillong, Meghalaya',
    latitude: 25.5788,
    longitude: 91.8933,
    riskLevel: 'MEDIUM',
    probability: 0.62,
    status: 'resolved',
    createdAt: new Date(Date.now() - 48 * 60 * 60 * 1000),
    updatedAt: new Date(Date.now() - 12 * 60 * 60 * 1000),
    affectedPopulation: 3100,
    description: 'Risk levels have decreased. Situation stabilized.'
  }
];

export const mockReports = [
  {
    id: 1,
    location: 'Gangtok-Nathula Road',
    latitude: 27.3389,
    longitude: 88.6065,
    hazardType: 'landslide',
    severity: 'high',
    description: 'Small landslide observed on hillside. Road partially blocked.',
    reportedBy: 'Local Resident',
    contactInfo: 'anonymous',
    status: 'verified',
    createdAt: new Date(Date.now() - 3 * 60 * 60 * 1000),
    imageUrl: null
  },
  {
    id: 2,
    location: 'Cherrapunji Hills',
    latitude: 25.2630,
    longitude: 91.7324,
    hazardType: 'ground-cracks',
    severity: 'medium',
    description: 'Visible ground cracks appearing near residential area after monsoon.',
    reportedBy: 'Field Officer',
    contactInfo: 'officer@example.com',
    status: 'investigating',
    createdAt: new Date(Date.now() - 8 * 60 * 60 * 1000),
    imageUrl: null
  },
  {
    id: 3,
    location: 'Dawki, Meghalaya',
    latitude: 25.1833,
    longitude: 92.0167,
    hazardType: 'soil-erosion',
    severity: 'low',
    description: 'Soil erosion observed after recent rainfall near Bangladesh border.',
    reportedBy: 'Anonymous',
    contactInfo: 'anonymous',
    status: 'resolved',
    createdAt: new Date(Date.now() - 24 * 60 * 60 * 1000),
    imageUrl: null
  }
];

export const mockRiskZones = [
  {
    id: 1,
    name: 'Gangtok, Sikkim',
    latitude: 27.3389,
    longitude: 88.6065,
    riskLevel: 'HIGH',
    probability: 0.87,
    radius: 2000
  },
  {
    id: 2,
    name: 'Cherrapunji, Meghalaya',
    latitude: 25.2630,
    longitude: 91.7324,
    riskLevel: 'CRITICAL',
    probability: 0.94,
    radius: 3000
  },
  {
    id: 3,
    name: 'Itanagar, Arunachal',
    latitude: 27.0844,
    longitude: 93.6053,
    riskLevel: 'HIGH',
    probability: 0.79,
    radius: 2500
  },
  {
    id: 4,
    name: 'Shillong, Meghalaya',
    latitude: 25.5788,
    longitude: 91.8933,
    riskLevel: 'MEDIUM',
    probability: 0.62,
    radius: 1500
  },
  {
    id: 5,
    name: 'Kohima, Nagaland',
    latitude: 25.6747,
    longitude: 94.1106,
    riskLevel: 'MEDIUM',
    probability: 0.58,
    radius: 2200
  }
];
