/**
 * KRISHIRAKSHAK — API Client Service
 * Encapsulates all REST calls to the FastAPI backend.
 */

const API_BASE = '/api';

export const ApiService = {
  // 1. Dashboard & Analytics
  async getDashboardSummary(opts = {}) {
    const params = new URLSearchParams();
    if (opts.lat !== undefined && opts.lat !== null && opts.lat !== '') params.append('lat', opts.lat);
    if (opts.lon !== undefined && opts.lon !== null && opts.lon !== '') params.append('lon', opts.lon);
    if (opts.city) params.append('city', opts.city);
    if (opts.crop) params.append('crop', opts.crop);
    const qs = params.toString() ? `?${params.toString()}` : '';
    const res = await fetch(`${API_BASE}/analytics/dashboard${qs}`);
    if (!res.ok) throw new Error(`Dashboard error: ${res.statusText}`);
    return await res.json();
  },

  async getHistoricalTrends() {
    const res = await fetch(`${API_BASE}/analytics/trends`);
    if (!res.ok) throw new Error(`Trends error: ${res.statusText}`);
    return await res.json();
  },

  // 2. Weather
  async getCurrentWeather(opts = {}) {
    const params = new URLSearchParams();
    if (typeof opts === 'string') {
      if (opts) params.append('city', opts);
    } else {
      if (opts.city) params.append('city', opts.city);
      if (opts.lat !== undefined && opts.lat !== null && opts.lat !== '') params.append('lat', opts.lat);
      if (opts.lon !== undefined && opts.lon !== null && opts.lon !== '') params.append('lon', opts.lon);
    }
    const qs = params.toString() ? `?${params.toString()}` : '';
    const res = await fetch(`${API_BASE}/weather/current${qs}`);
    if (!res.ok) throw new Error(`Weather error: ${res.statusText}`);
    return await res.json();
  },

  async getWeatherForecast(opts = {}) {
    const params = new URLSearchParams();
    if (typeof opts === 'string') {
      if (opts) params.append('city', opts);
    } else {
      if (opts.city) params.append('city', opts.city);
      if (opts.lat !== undefined && opts.lat !== null && opts.lat !== '') params.append('lat', opts.lat);
      if (opts.lon !== undefined && opts.lon !== null && opts.lon !== '') params.append('lon', opts.lon);
    }
    const qs = params.toString() ? `?${params.toString()}` : '';
    const res = await fetch(`${API_BASE}/weather/forecast${qs}`);
    if (!res.ok) throw new Error(`Forecast error: ${res.statusText}`);
    return await res.json();
  },

  // 3. Pest Risk Forecasting (XGBoost + SHAP)
  async predictPestRisk(payload) {
    const res = await fetch(`${API_BASE}/pest/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `Pest inference failed (${res.status})`);
    }
    return await res.json();
  },

  async getPestMetrics() {
    const res = await fetch(`${API_BASE}/pest/metrics`);
    if (!res.ok) throw new Error(`Metrics error: ${res.statusText}`);
    return await res.json();
  },

  async getPestHistory(limit = 10) {
    const res = await fetch(`${API_BASE}/pest/history?limit=${limit}`);
    if (!res.ok) return [];
    return await res.json();
  },

  // 4. Smart Irrigation
  async getCurrentSoilMoisture() {
    const res = await fetch(`${API_BASE}/irrigation/current`);
    if (!res.ok) throw new Error(`Soil moisture error: ${res.statusText}`);
    return await res.json();
  },

  async getIrrigationAdvisory(payload) {
    const res = await fetch(`${API_BASE}/irrigation/advisory`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `Irrigation calculation failed (${res.status})`);
    }
    return await res.json();
  },

  async getIrrigationHistory(limit = 10) {
    const res = await fetch(`${API_BASE}/irrigation/history?limit=${limit}`);
    if (!res.ok) return [];
    return await res.json();
  },

  // 5. Crop Recommendation
  async recommendCrops(payload) {
    const res = await fetch(`${API_BASE}/crops/recommend`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `Crop recommendation failed (${res.status})`);
    }
    return await res.json();
  },

  // 6. Treatment Guidance & IPM Knowledge Base
  async getTreatments(crop = '', condition = '') {
    const params = new URLSearchParams();
    if (crop) params.append('crop', crop);
    if (condition) params.append('condition', condition);
    const qs = params.toString() ? `?${params.toString()}` : '';
    const res = await fetch(`${API_BASE}/treatment/${qs}`);
    if (!res.ok) throw new Error(`Treatment error: ${res.statusText}`);
    return await res.json();
  },

  // 7. Disease Detection Placeholder
  async getDiseaseStatus() {
    const res = await fetch(`${API_BASE}/disease/status`);
    if (!res.ok) throw new Error(`Disease status error: ${res.statusText}`);
    return await res.json();
  },

  async testDiseaseUpload(file, crop = '') {
    const formData = new FormData();
    if (file) formData.append('image', file);
    if (crop) formData.append('crop', crop);
    const res = await fetch(`${API_BASE}/disease/predict`, {
      method: 'POST',
      body: formData
    });
    return await res.json();
  },

  // 8. Settings
  async getSettings() {
    const res = await fetch(`${API_BASE}/settings/`);
    if (!res.ok) throw new Error(`Settings error: ${res.statusText}`);
    return await res.json();
  },

  async updateSettings(payload) {
    const res = await fetch(`${API_BASE}/settings/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error(`Failed to update settings (${res.status})`);
    return await res.json();
  }
};
