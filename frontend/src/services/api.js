const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function fetchAPI(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    }
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `API error: ${response.status}`);
  }

  return response.json();
}

export const api = {
  async getRiskPrediction(latitude, longitude) {
    const data = await fetchAPI('/predictions', {
      method: 'POST',
      body: JSON.stringify({ latitude, longitude })
    });
    return {
      predictionId: data.prediction_id,
      latitude: data.latitude,
      longitude: data.longitude,
      riskLevel: data.risk_level,
      probability: data.probability,
      confidence: data.confidence,
      features: {
        rainfall: data.features.rainfall,
        slope: data.features.slope,
        elevation: data.features.elevation,
        soilMoisture: data.features.soil_moisture,
        temperature: data.features.temperature
      },
      explanation: data.explanation,
      timestamp: new Date(data.timestamp)
    };
  },

  async getDashboardData() {
    const alerts = await fetchAPI('/alerts');
    
    const activeAlerts = alerts.filter(a => a.status === 'active').length;
    const highRiskAreas = alerts.filter(a =>
      a.risk_level === 'HIGH' || a.risk_level === 'CRITICAL'
    ).length;

    return {
      statistics: {
        monitoredLocations: 124,
        highRiskAreas,
        activeAlerts,
        reportsToday: 36
      },
      riskDistribution: { low: 58, medium: 24, high: 13, critical: 5 },
      rainfallData: {
        last24Hours: [
          { time: '00:00', rainfall: 12 }, { time: '03:00', rainfall: 18 },
          { time: '06:00', rainfall: 25 }, { time: '09:00', rainfall: 32 },
          { time: '12:00', rainfall: 28 }, { time: '15:00', rainfall: 42 },
          { time: '18:00', rainfall: 55 }, { time: '21:00', rainfall: 38 }
        ],
        last7Days: [
          { day: 'Mon', rainfall: 45 }, { day: 'Tue', rainfall: 52 },
          { day: 'Wed', rainfall: 38 }, { day: 'Thu', rainfall: 65 },
          { day: 'Fri', rainfall: 78 }, { day: 'Sat', rainfall: 85 },
          { day: 'Sun', rainfall: 92 }
        ],
        last30Days: [
          { week: 'Week 1', rainfall: 245 }, { week: 'Week 2', rainfall: 312 },
          { week: 'Week 3', rainfall: 285 }, { week: 'Week 4', rainfall: 398 }
        ]
      },
      recentAlerts: alerts.map(a => ({
        id: a.id,
        location: a.location,
        riskLevel: a.risk_level,
        probability: a.probability,
        timestamp: new Date(a.updated_at),
        latitude: a.latitude,
        longitude: a.longitude
      }))
    };
  },

  async getRiskZones() {
    const alerts = await fetchAPI('/alerts');
    return alerts.map(a => ({
      id: a.id,
      name: a.location,
      latitude: a.latitude,
      longitude: a.longitude,
      riskLevel: a.risk_level,
      probability: a.probability,
      radius: a.risk_level === 'CRITICAL' ? 3000 : a.risk_level === 'HIGH' ? 2000 : 1500
    }));
  },

  async getAlerts(filters = {}) {
    let query = '';
    if (filters.status) query += `?status=${filters.status}`;
    if (filters.riskLevel) query += `${query ? '&' : '?'}risk_level=${filters.riskLevel}`;
    
    const alerts = await fetchAPI(`/alerts${query}`);
    return alerts.map(a => ({
      id: a.id,
      location: a.location,
      latitude: a.latitude,
      longitude: a.longitude,
      riskLevel: a.risk_level,
      probability: a.probability,
      status: a.status,
      createdAt: new Date(a.created_at),
      updatedAt: new Date(a.updated_at),
      affectedPopulation: a.affected_population,
      description: a.description
    }));
  },

  async getReports() {
    const data = await fetchAPI('/reports');
    return data.reports || [];
  },

  async submitHazardReport(reportData) {
    const data = await fetchAPI('/reports', {
      method: 'POST',
      body: JSON.stringify({
        location: reportData.location,
        latitude: parseFloat(reportData.latitude),
        longitude: parseFloat(reportData.longitude),
        hazard_type: reportData.hazardType || reportData.hazard_type,
        severity: reportData.severity,
        description: reportData.description,
        contact_info: reportData.contactInfo || reportData.contact_info || null
      })
    });
    return {
      success: data.success,
      reportId: data.report_id,
      message: data.message
    };
  }
};
