const API_BASE_URL = (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_URL) 
  ? import.meta.env.VITE_API_URL 
  : 'http://127.0.0.1:8000/api/v1';

async function fetchAPI(endpoint, options = {}) {
  const token = localStorage.getItem('auth_token');
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
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
  async login(username, password) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData.toString()
    });
    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      throw new Error(err.detail || 'Login failed');
    }
    const data = await response.json();
    if (data.access_token) {
      localStorage.setItem('auth_token', data.access_token);
      localStorage.setItem('auth_user', JSON.stringify(data.user));
    }
    return data;
  },

  async getRiskPrediction(latitude, longitude, environmentalData = {}) {
    const body = {
      latitude,
      longitude,
      ...(environmentalData.rainfall_1d != null && { rainfall_1d: environmentalData.rainfall_1d }),
      ...(environmentalData.rainfall_3d != null && { rainfall_3d: environmentalData.rainfall_3d }),
      ...(environmentalData.rainfall_7d != null && { rainfall_7d: environmentalData.rainfall_7d }),
      ...(environmentalData.elevation_m != null && { elevation_m: environmentalData.elevation_m }),
      ...(environmentalData.slope_degrees != null && { slope_degrees: environmentalData.slope_degrees }),
      ...(environmentalData.soil_moisture != null && { soil_moisture: environmentalData.soil_moisture }),
    };

    const data = await fetchAPI('/predictions', {
      method: 'POST',
      body: JSON.stringify(body)
    });

    return {
      predictionId: data.prediction_id,
      latitude: data.latitude,
      longitude: data.longitude,
      riskLevel: data.risk_level,
      probability: data.probability,
      confidence: data.confidence,
      features: {
        rainfall1d: data.features.rainfall_1d,
        rainfall3d: data.features.rainfall_3d,
        rainfall7d: data.features.rainfall_7d,
        elevationM: data.features.elevation_m,
        slopeDegrees: data.features.slope_degrees,
        soilMoisture: data.features.soil_moisture,
      },
      explanation: data.explanation,
      modelName: data.model_name,
      modelVersion: data.model_version,
      timestamp: new Date(data.timestamp)
    };
  },

  async getMultiHazardForecast(latitude, longitude) {
    return fetchAPI('/predictions/multi-hazard-forecast', {
      method: 'POST',
      body: JSON.stringify({ latitude, longitude })
    });
  },

  async getModelInfo() {
    return fetchAPI('/predictions/model-info');
  },

  async getDashboardData() {
    const summary = await fetchAPI('/dashboard/summary');
    return {
      statistics: summary.statistics,
      riskDistribution: summary.riskDistribution,
      rainfallData: {
        last7Days: summary.rainfallData?.last7Days || [],
        total7d: summary.rainfallData?.total7dRainfall || 0,
      },
      recentAlerts: (summary.recentAlerts || []).map(a => ({
        id: a.id,
        location: a.location,
        riskLevel: a.riskLevel,
        probability: a.probability,
        timestamp: new Date(a.timestamp),
        latitude: a.latitude,
        longitude: a.longitude,
        status: a.status,
      }))
    };
  },

  async getRiskZones() {
    const zones = await fetchAPI('/risk-zones');
    return zones.map(z => ({
      id: z.id,
      name: z.name,
      latitude: z.latitude,
      longitude: z.longitude,
      elevation_m: z.elevation_m,
      slope_degrees: z.slope_degrees,
      riskLevel: z.riskLevel,
      probability: z.probability,
      radius: z.radius,
    }));
  },

  async syncLiveAlerts() {
    return fetchAPI('/alerts/sync', { method: 'POST' });
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

  async getReports(filters = {}) {
    let query = '';
    if (filters.state) query += `?state=${encodeURIComponent(filters.state)}`;
    if (filters.status) query += `${query ? '&' : '?'}status=${filters.status}`;

    const data = await fetchAPI(`/reports${query}`);
    return data.reports || [];
  },

  async submitHazardReport(reportData) {
    const data = await fetchAPI('/reports', {
      method: 'POST',
      body: JSON.stringify({
        location: reportData.location,
        state: reportData.state || 'Meghalaya',
        district: reportData.district || null,
        latitude: parseFloat(reportData.latitude),
        longitude: parseFloat(reportData.longitude),
        hazard_type: reportData.hazardType || reportData.hazard_type || 'landslide',
        severity: reportData.severity || 'medium',
        description: reportData.description,
        visible_cracks: Boolean(reportData.visible_cracks),
        rockfall_observed: Boolean(reportData.rockfall_observed),
        road_blocked: Boolean(reportData.road_blocked),
        water_accumulation: Boolean(reportData.water_accumulation),
        soil_movement: Boolean(reportData.soil_movement),
        media_url: reportData.media_url || null,
        idempotency_key: reportData.idempotency_key || null,
        contact_info: reportData.contactInfo || reportData.contact_info || null
      })
    });
    return {
      success: data.success,
      reportId: data.report_id,
      message: data.message
    };
  },

  async deleteReport(reportId) {
    return fetchAPI(`/reports/${reportId}`, {
      method: 'DELETE'
    });
  },

  async updateReportStatus(reportId, newStatus, adminNotes = '') {
    return fetchAPI(`/reports/${reportId}/status`, {
      method: 'PATCH',
      body: JSON.stringify({
        status: newStatus,
        admin_notes: adminNotes
      })
    });
  }
};
