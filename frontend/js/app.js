/**
 * KRISHIRAKSHAK — Main Application Controller
 * Handles application state, user interactions, module routing, and real-time UI updates.
 */

import { ApiService } from './api.js';
import { ChartRenderer } from './charts.js';

class KrishiRakshakApp {
  constructor() {
    this.currentView = 'home';
    this.systemState = null;
    this.init();
  }

  async init() {
    this.setGreeting();
    this.bindNavigation();
    this.bindForms();
    this.bindQuickActions();
    
    // Initial Load
    await this.loadInitialData();
  }

  setGreeting() {
    const h = new Date().getHours();
    const g = h < 12 ? 'Good Morning' : h < 17 ? 'Good Afternoon' : 'Good Evening';
    const el = document.getElementById('greetingText');
    if (el) el.textContent = `${g}, Farmer 🌾`;
  }

  // Toast Notification System
  showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast';
    let icon = 'ℹ️';
    if (type === 'success') icon = '✅';
    if (type === 'danger') icon = '⚠️';
    if (type === 'warning') icon = '🔔';

    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }

  // Navigation Controller
  bindNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        const targetPage = item.dataset.page;
        this.switchPage(targetPage);
      });
    });

    // Mobile sidebar toggle if exists
    const menuToggle = document.getElementById('menu-toggle');
    if (menuToggle) {
      menuToggle.addEventListener('click', () => {
        document.querySelector('.app-sidebar').classList.toggle('open');
      });
    }
  }

  switchPage(pageId) {
    if (!pageId) return;
    this.currentView = pageId;

    // Update nav states
    document.querySelectorAll('.nav-item').forEach(el => {
      el.classList.toggle('active', el.dataset.page === pageId);
    });

    // Update page views
    document.querySelectorAll('.page-view').forEach(view => {
      view.classList.toggle('active', view.id === `page-${pageId}`);
    });

    // Update Header title if present
    const headerTitle = document.getElementById('header-page-title');
    const titles = {
      'home': 'System Overview & Executive Dashboard',
      'pest': 'Pest Risk Forecasting & TreeSHAP Attribution',
      'irrigation': 'Smart Irrigation & Water Balance Advisory',
      'crops': 'Crop Agronomic Suitability & Ecological Scoring',
      'disease': 'Crop Leaf Disease Diagnostics (Integration)',
      'treatment': 'Integrated Pest Management (IPM) Guidance',
      'analytics': 'Historical Sensors & Microclimate Analytics',
      'settings': 'System Runtime & Configuration'
    };
    if (headerTitle) {
      headerTitle.textContent = titles[pageId] || 'KrishiRakshak';
    }

    // Trigger lazy loading per page
    if (pageId === 'analytics') {
      this.loadAnalyticsPage();
    } else if (pageId === 'irrigation') {
      this.loadIrrigationPage();
    } else if (pageId === 'treatment') {
      this.loadTreatmentPage();
    } else if (pageId === 'settings') {
      this.loadSettingsPage();
    }
  }

  // Initial Data Fetch
  async loadInitialData() {
    try {
      const latVal = document.getElementById('top-lat')?.value;
      const lonVal = document.getElementById('top-lon')?.value;
      const crop = document.getElementById('top-crop-select')?.value || 'rice';
      const lat = latVal !== undefined && latVal !== '' ? parseFloat(latVal) : 21.15;
      const lon = lonVal !== undefined && lonVal !== '' ? parseFloat(lonVal) : 79.09;

      const summary = await ApiService.getDashboardSummary({ lat, lon, crop });
      this.systemState = summary;
      this.renderDashboard(summary);
      this.updateModeBadges(summary.mode_badge);
      this.syncLiveWeatherToForms(summary.weather);
      this.loadPestHistory();
      this.loadIrrigationHistory();
    } catch (err) {
      console.error('Failed to load initial data:', err);
      this.showToast('Could not load dashboard data from backend', 'danger');
    }
  }

  updateModeBadges(badgeText) {
    const badges = document.querySelectorAll('.mode-badge-text');
    badges.forEach(b => {
      b.textContent = badgeText || 'LIVE WEATHER MODE';
    });
  }

  syncLiveWeatherToForms(w) {
    if (!w) return;
    // 1. Sync to Pest Forecast form sliders
    const pestTemp = document.getElementById('pest-temp');
    const pestHum = document.getElementById('pest-hum');
    const pestRain = document.getElementById('pest-rain');
    if (pestTemp && w.temperature !== undefined) {
      pestTemp.value = Math.round(w.temperature);
      const valEl = document.getElementById('pest-temp-val');
      if (valEl) valEl.textContent = Math.round(w.temperature);
    }
    if (pestHum && w.humidity !== undefined) {
      pestHum.value = Math.round(w.humidity);
      const valEl = document.getElementById('pest-hum-val');
      if (valEl) valEl.textContent = Math.round(w.humidity);
    }
    if (pestRain && w.rainfall !== undefined) {
      pestRain.value = Math.round(w.rainfall);
      const valEl = document.getElementById('pest-rain-val');
      if (valEl) valEl.textContent = Math.round(w.rainfall);
    }

    // 2. Sync to Crop Recommendation form sliders
    const cropTemp = document.getElementById('crop-temp');
    const cropHum = document.getElementById('crop-hum');
    const cropRain = document.getElementById('crop-rain');
    if (cropTemp && w.temperature !== undefined) {
      cropTemp.value = Math.round(w.temperature);
      const valEl = document.getElementById('crop-temp-val');
      if (valEl) valEl.textContent = Math.round(w.temperature);
    }
    if (cropHum && w.humidity !== undefined) {
      cropHum.value = Math.round(w.humidity);
      const valEl = document.getElementById('crop-hum-val');
      if (valEl) valEl.textContent = Math.round(w.humidity);
    }
    if (cropRain && w.rainfall !== undefined) {
      cropRain.value = Math.max(20, Math.round(w.rainfall > 0 ? w.rainfall * 10 : 120));
      const valEl = document.getElementById('crop-rain-val');
      if (valEl) valEl.textContent = cropRain.value;
    }
  }

  // Dashboard Rendering
  renderDashboard(data) {
    if (!data) return;

    // 1. Weather Cards
    const w = data.weather;
    if (w) {
      const tempEl = document.getElementById('dash-temp');
      if (tempEl) tempEl.textContent = `${w.temperature.toFixed(0)}°C`;
      
      const humEl = document.getElementById('dash-humidity');
      if (humEl) humEl.textContent = `💧 ${w.humidity.toFixed(0)}%`;
      
      const rainEl = document.getElementById('dash-rain');
      if (rainEl) rainEl.textContent = `🌧️ ${w.rainfall.toFixed(0)}mm`;

      const windEl = document.getElementById('dash-wind');
      if (windEl) windEl.textContent = `🍃 ${w.wind_speed.toFixed(1)} m/s`;
      
      const condEl = document.getElementById('dash-weather-condition');
      if (condEl) condEl.textContent = w.weather_condition;
      
      const locEl = document.getElementById('dash-location-name');
      if (locEl) locEl.textContent = w.location;

      const emojiEl = document.getElementById('dash-weather-emoji') || document.getElementById('weatherEmoji');
      if (emojiEl) {
        emojiEl.textContent = w.rainfall > 5 ? '🌧️' : w.rainfall > 0 ? '🌦️' : w.temperature > 28 ? '☀️' : '⛅';
      }

      // Render 5-Day Forecast Row with Live Daily Humidity & Temp
      const forecastRow = document.getElementById('dash-forecast-row');
      if (forecastRow) {
        if (data.forecast && data.forecast.length > 0) {
          forecastRow.innerHTML = data.forecast.map((f, i) => {
            const condEmoji = f.rainfall_mm > 4 ? '🌧️' : f.rainfall_mm > 0 ? '🌦️' : f.temperature > 28 ? '☀️' : '⛅';
            return `
              <div class="forecast-day ${i === 0 ? 'today' : ''}" title="${f.condition} • Humidity: ${f.humidity}% • Rain: ${f.rainfall_mm}mm">
                <div class="d">${i === 0 ? 'Today' : f.day_name}</div>
                <div class="e">${condEmoji}</div>
                <div class="t">${Math.round(f.temperature)}°C</div>
                <div style="font-size:0.75rem; color:#a7f3d0; margin-top:3px; font-weight:600;">💧 ${Math.round(f.humidity)}%</div>
              </div>
            `;
          }).join('');
        } else {
          const d = new Date();
          const dayNames = ['Today'];
          for (let i = 1; i < 5; i++) {
            const next = new Date();
            next.setDate(d.getDate() + i);
            dayNames.push(next.toLocaleDateString('en-US', { weekday: 'short' }));
          }
          const temps = [
            Math.round(w.temperature),
            Math.round(w.temperature + 2),
            Math.round(w.temperature - 1),
            Math.round(w.temperature + 1),
            Math.round(w.temperature)
          ];
          const emojis = ['⛅', '☀️', '🌧️', '⛈️', '🌤️'];
          forecastRow.innerHTML = dayNames.map((name, i) => `
            <div class="forecast-day ${i === 0 ? 'today' : ''}">
              <div class="d">${name}</div>
              <div class="e">${emojis[i]}</div>
              <div class="t">${temps[i]}°C</div>
              <div style="font-size:0.75rem; color:#a7f3d0; margin-top:3px; font-weight:600;">💧 ${Math.round(w.humidity)}%</div>
            </div>
          `).join('');
        }
      }
    }

    // 2. Soil Moisture & Irrigation
    const sm = data.soil_moisture;
    const ir = data.irrigation;
    if (sm) {
      const irrMoistInput = document.getElementById('irr-moist-override');
      if (irrMoistInput) {
        irrMoistInput.value = sm.soil_moisture_percent.toFixed(1);
      }
      const hint = document.getElementById('irr-sensor-hint');
      if (hint) {
        hint.textContent = `Auto-populated from Sensor ${sm.sensor_id} dataset (${sm.soil_moisture_percent.toFixed(1)}% VWC at 15cm depth)`;
      }
    }

    if (ir) {
      const irrBadge = document.getElementById('dash-irr-badge');
      const irrSummary = document.getElementById('dash-irr-summary');
      const isIrrigate = ir.decision === 'IRRIGATE';
      if (irrBadge) {
        irrBadge.textContent = isIrrigate ? 'Irrigate' : 'Optimal';
        irrBadge.className = `status-pill ${isIrrigate ? 'warn' : 'ok'}`;
      }
      if (irrSummary) {
        const moist = sm ? sm.soil_moisture_percent.toFixed(1) : '31.2';
        irrSummary.textContent = isIrrigate 
          ? `Moisture deficit detected (${moist}% VWC). Recommended dose: ${ir.water_amount_mm} mm.`
          : `Soil moisture is at optimal level (${moist}% VWC). No irrigation needed today.`;
      }
    }

    // 3. Pest Risk
    const pr = data.pest_risk;
    if (pr) {
      const pestBadge = document.getElementById('dash-pest-risk-badge');
      const pestSummary = document.getElementById('dash-pest-summary');
      const risk = pr.predicted_risk || 'LOW';
      if (pestBadge) {
        pestBadge.textContent = `${risk.charAt(0) + risk.slice(1).toLowerCase()} Risk`;
        pestBadge.className = `status-pill ${risk === 'HIGH' ? 'bad' : risk === 'MEDIUM' ? 'warn' : 'ok'}`;
      }
      if (pestSummary) {
        pestSummary.textContent = risk === 'HIGH'
          ? `High pest outbreak risk (${pr.probability_percent}%). Immediate field inspection recommended.`
          : risk === 'MEDIUM'
          ? `Moderate pest risk (${pr.probability_percent}%). Monitor microclimate drivers.`
          : `XGBoost 3–5 day risk projection indicates low insect pest pressure (${pr.probability_percent}%).`;
      }
    }

    // 4. Alert Card
    const alertTitle = document.getElementById('dash-alert-title');
    const alertMsg = document.getElementById('dash-alert-msg');
    if (alertTitle && alertMsg) {
      if (pr && pr.predicted_risk === 'HIGH') {
        alertTitle.textContent = 'Pest Risk Alert';
        alertMsg.textContent = `Elevated pest pressure (${pr.probability_percent}% probability) detected for current conditions.`;
      } else if (ir && ir.decision === 'IRRIGATE') {
        alertTitle.textContent = 'Irrigation Advisory';
        alertMsg.textContent = `Soil moisture below ideal threshold. Irrigation of ${ir.water_amount_mm} mm suggested.`;
      } else {
        alertTitle.textContent = 'No Critical Alerts';
        alertMsg.textContent = 'Your crops are looking healthy!';
      }
    }

    // 5. Crop Recommendation Hero
    const topCropName = document.getElementById('dash-top-crop-name');
    const topCropScore = document.getElementById('dash-top-crop-score');
    const cropSelect = document.getElementById('top-crop-select');
    const selectedCrop = cropSelect ? cropSelect.value : 'rice';
    const cropNames = {
      'rice': 'Paddy (Rice)',
      'cotton': 'Cotton',
      'soybean': 'Soybean',
      'wheat': 'Wheat'
    };
    if (topCropName) {
      topCropName.textContent = cropNames[selectedCrop] || 'Paddy (Rice)';
    }
    if (topCropScore) {
      topCropScore.textContent = 'High Suitability';
    }
  }

  // Forms Controller
  bindForms() {
    // 1. Pest Forecast Form
    const pestForm = document.getElementById('pest-form');
    if (pestForm) {
      pestForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handlePestInference();
      });

      // Quick Sync button: fetch live humidity & temperature from Weather API
      const pestSyncWeatherBtn = document.getElementById('btn-sync-pest-weather');
      if (pestSyncWeatherBtn) {
        pestSyncWeatherBtn.addEventListener('click', async () => {
          await this.syncCurrentWeatherToActiveForm('pest');
        });
      }

      // Synchronize slider numbers
      const syncInputs = ['pest-temp', 'pest-hum', 'pest-rain', 'pest-n', 'pest-p', 'pest-k', 'pest-ph'];
      syncInputs.forEach(id => {
        const slider = document.getElementById(id);
        const display = document.getElementById(`${id}-val`);
        if (slider && display) {
          slider.addEventListener('input', () => {
            display.textContent = slider.value;
          });
        }
      });
    }

    // 2. Irrigation Form
    const irrForm = document.getElementById('irrigation-form');
    if (irrForm) {
      irrForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleIrrigationCalculation();
      });

      // Quick Sync button: fetch and populate from sensor dataset
      const syncBtn = document.getElementById('btn-sync-sensor-moist');
      if (syncBtn) {
        syncBtn.addEventListener('click', async () => {
          await this.syncSensorMoisture();
        });
      }
    }

    // 3. Crop Recommendation Form
    const cropForm = document.getElementById('crop-form');
    if (cropForm) {
      cropForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleCropRecommendation();
      });

      // Quick Sync button: fetch live humidity & temperature from Weather API
      const cropSyncWeatherBtn = document.getElementById('btn-sync-crop-weather');
      if (cropSyncWeatherBtn) {
        cropSyncWeatherBtn.addEventListener('click', async () => {
          await this.syncCurrentWeatherToActiveForm('crop');
        });
      }

      const cropSliders = ['crop-n', 'crop-p', 'crop-k', 'crop-temp', 'crop-hum', 'crop-ph', 'crop-rain'];
      cropSliders.forEach(id => {
        const slider = document.getElementById(id);
        const display = document.getElementById(`${id}-val`);
        if (slider && display) {
          slider.addEventListener('input', () => {
            display.textContent = slider.value;
          });
        }
      });
    }

    // 4. Treatment Search
    const treatmentSearch = document.getElementById('treatment-search');
    const treatmentCropFilter = document.getElementById('treatment-crop-filter');
    if (treatmentSearch && treatmentCropFilter) {
      const runSearch = () => {
        this.loadTreatmentPage(treatmentCropFilter.value, treatmentSearch.value);
      };
      treatmentSearch.addEventListener('input', runSearch);
      treatmentCropFilter.addEventListener('change', runSearch);
    }

    // 5. Disease Upload Simulation
    const diseaseInput = document.getElementById('disease-file-input');
    const diseaseBox = document.getElementById('disease-drop-zone');
    if (diseaseInput && diseaseBox) {
      diseaseBox.addEventListener('click', () => diseaseInput.click());
      diseaseInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (file) await this.handleDiseaseImage(file);
      });
    }

    // 6. Settings Form
    const settingsForm = document.getElementById('settings-form');
    if (settingsForm) {
      settingsForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleSettingsSave();
      });
    }
  }

  bindQuickActions() {
    const refreshBtn = document.getElementById('quick-refresh-btn');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', async () => {
        this.showToast('Refreshing latest agricultural sensor state...', 'info');
        await this.loadInitialData();
        this.showToast('Data refreshed successfully', 'success');
      });
    }

    const updateBtn = document.getElementById('top-update-btn');
    if (updateBtn) {
      updateBtn.addEventListener('click', async () => {
        const crop = document.getElementById('top-crop-select')?.value || 'rice';
        this.showToast(`Updating recommendations for ${crop.toUpperCase()}...`, 'info');
        await this.loadInitialData();
        this.showToast(`Updated agricultural state for ${crop.toUpperCase()}`, 'success');
      });
    }
  }

  // Module Actions
  async handlePestInference() {
    const payload = {
      crop: document.getElementById('pest-crop').value,
      temperature: parseFloat(document.getElementById('pest-temp').value),
      humidity: parseFloat(document.getElementById('pest-hum').value),
      rainfall: parseFloat(document.getElementById('pest-rain').value),
      N: parseFloat(document.getElementById('pest-n').value),
      P: parseFloat(document.getElementById('pest-p').value),
      K: parseFloat(document.getElementById('pest-k').value),
      ph: parseFloat(document.getElementById('pest-ph').value)
    };

    try {
      this.showToast('Executing XGBoost inference & TreeSHAP attributions...', 'info');
      const res = await ApiService.predictPestRisk(payload);

      // Render Result
      const badge = document.getElementById('pest-result-risk');
      badge.textContent = res.predicted_risk;
      badge.className = `badge ${res.predicted_risk === 'HIGH' ? 'danger' : res.predicted_risk === 'MEDIUM' ? 'warning' : 'success'}`;
      
      document.getElementById('pest-result-prob').textContent = `${res.probability_percent}%`;
      document.getElementById('pest-result-action').textContent = res.action_summary;

      // Class breakdown
      const probs = res.class_probabilities || {};
      document.getElementById('pest-prob-high').textContent = `${probs.HIGH || 0}%`;
      document.getElementById('pest-prob-med').textContent = `${probs.MEDIUM || 0}%`;
      document.getElementById('pest-prob-low').textContent = `${probs.LOW || 0}%`;

      // Render TreeSHAP horizontal diverging bars
      ChartRenderer.renderShapBars('pest-shap-container', res.shap_explanations);

      this.showToast('Inference complete! TreeSHAP factors updated.', 'success');
      this.loadPestHistory();
    } catch (err) {
      this.showToast(err.message, 'danger');
    }
  }

  async loadPestHistory() {
    const container = document.getElementById('pest-history-tbody');
    if (!container) return;
    try {
      const records = await ApiService.getPestHistory(8);
      if (records.length === 0) {
        container.innerHTML = `<tr><td colspan="5" style="text-align:center;">No prediction records logged yet.</td></tr>`;
        return;
      }
      container.innerHTML = records.map(r => `
        <tr>
          <td>${r.timestamp || 'Recent'}</td>
          <td><strong style="color:var(--text-main);">${r.crop.toUpperCase()}</strong></td>
          <td><span class="badge ${r.predicted_risk === 'HIGH' ? 'danger' : r.predicted_risk === 'MEDIUM' ? 'warning' : 'success'}">${r.predicted_risk}</span></td>
          <td>${r.probability_percent}%</td>
          <td>${r.features ? `${r.features.temperature}°C, ${r.features.humidity}% RH` : '-'}</td>
        </tr>
      `).join('');
    } catch (err) {
      console.warn('Could not load pest history:', err);
    }
  }

  async handleIrrigationCalculation() {
    const payload = {
      crop: document.getElementById('irr-crop').value,
      growth_stage: document.getElementById('irr-stage').value,
      soil_type: document.getElementById('irr-soil').value,
      irrigation_method: document.getElementById('irr-method').value,
      forecast_rain_48h: parseFloat(document.getElementById('irr-rain-override').value || 0),
      manual_soil_moisture: document.getElementById('irr-moist-override').value 
        ? parseFloat(document.getElementById('irr-moist-override').value) / 100 
        : null
    };

    try {
      this.showToast('Calculating FAO-56 Penman-Monteith ETc & Water Balance...', 'info');
      const res = await ApiService.getIrrigationAdvisory(payload);

      // Render Results
      const decBadge = document.getElementById('irr-result-decision');
      decBadge.textContent = res.decision;
      decBadge.className = `badge ${res.decision === 'IRRIGATE' ? 'info' : 'success'}`;

      document.getElementById('irr-result-intensity').textContent = `${res.intensity} Intensity`;
      document.getElementById('irr-result-amount-mm').textContent = `${res.water_amount_mm} mm`;
      document.getElementById('irr-result-amount-l').textContent = `${res.water_liters_per_m2} L/m² (${res.water_liters_per_hectare.toLocaleString()} L/ha)`;

      document.getElementById('irr-result-etc').textContent = `${res.etc_mm_day} mm/day (Kc = ${res.kc})`;
      document.getElementById('irr-result-depletion').textContent = `${res.depletion_percentage}% Depletion`;

      // Render Dial
      ChartRenderer.renderMoistureDial(
        'irr-dial-container', 
        res.soil_moisture_percent, 
        res.field_capacity_percent, 
        res.wilting_point_percent
      );

      // Render Reasons
      const reasonsList = document.getElementById('irr-reasons-list');
      if (reasonsList && res.reasons) {
        reasonsList.innerHTML = res.reasons.map(r => `<li>${r}</li>`).join('');
      }

      this.showToast('Irrigation advisory generated!', 'success');
      this.loadIrrigationHistory();
    } catch (err) {
      this.showToast(err.message, 'danger');
    }
  }

  async loadIrrigationHistory() {
    const container = document.getElementById('irr-history-tbody');
    if (!container) return;
    try {
      const records = await ApiService.getIrrigationHistory(8);
      if (records.length === 0) {
        container.innerHTML = `<tr><td colspan="5" style="text-align:center;">No advisories logged yet.</td></tr>`;
        return;
      }
      container.innerHTML = records.map(r => `
        <tr>
          <td>${r.timestamp || 'Recent'}</td>
          <td><strong style="color:var(--text-main);">${r.crop.toUpperCase()}</strong></td>
          <td>${r.soil_moisture_percent}%</td>
          <td><span class="badge ${r.decision === 'IRRIGATE' ? 'info' : 'success'}">${r.decision}</span></td>
          <td>${r.water_amount_mm} mm</td>
        </tr>
      `).join('');
    } catch (err) {
      console.warn('Could not load irrigation history:', err);
    }
  }

  async syncSensorMoisture() {
    try {
      this.showToast('Fetching latest reading from TEROS 10 dataset...', 'info');
      const reading = await ApiService.getCurrentSoilMoisture();
      const input = document.getElementById('irr-moist-override');
      if (input) {
        input.value = reading.soil_moisture_percent.toFixed(1);
      }
      const hint = document.getElementById('irr-sensor-hint');
      if (hint) {
        hint.textContent = `Synced from Sensor ${reading.sensor_id} (${reading.soil_moisture_percent.toFixed(1)}% VWC at 15cm depth)`;
      }
      this.showToast(`Set to ${reading.soil_moisture_percent.toFixed(1)}% from Sensor ${reading.sensor_id} dataset!`, 'success');
      // Automatically recalculate water balance with the synced reading
      await this.handleIrrigationCalculation();
    } catch (err) {
      this.showToast('Could not sync sensor dataset reading', 'danger');
    }
  }

  async syncCurrentWeatherToActiveForm(target = 'both') {
    try {
      this.showToast('Fetching live atmospheric humidity & temperature from Weather API...', 'info');
      const latVal = document.getElementById('top-lat')?.value;
      const lonVal = document.getElementById('top-lon')?.value;
      const lat = latVal !== undefined && latVal !== '' ? parseFloat(latVal) : 21.15;
      const lon = lonVal !== undefined && lonVal !== '' ? parseFloat(lonVal) : 79.09;

      const w = await ApiService.getCurrentWeather({ lat, lon });
      this.syncLiveWeatherToForms(w);
      this.showToast(`Live Weather Synced: ${w.humidity}% Humidity, ${w.temperature}°C (${w.weather_condition})`, 'success');

      if (target === 'pest') {
        await this.handlePestInference();
      } else if (target === 'crop') {
        await this.handleCropRecommendation();
      }
    } catch (err) {
      console.error('Failed to sync live weather:', err);
      this.showToast('Could not fetch live weather from API', 'danger');
    }
  }

  async loadIrrigationPage() {
    const input = document.getElementById('irr-moist-override');
    if (input && (!input.value || input.value === '')) {
      if (this.systemState && this.systemState.soil_moisture) {
        input.value = this.systemState.soil_moisture.soil_moisture_percent.toFixed(1);
      } else {
        await this.syncSensorMoisture();
        return;
      }
    }
    await this.handleIrrigationCalculation();
  }

  async handleCropRecommendation() {
    const payload = {
      N: parseFloat(document.getElementById('crop-n').value),
      P: parseFloat(document.getElementById('crop-p').value),
      K: parseFloat(document.getElementById('crop-k').value),
      temperature: parseFloat(document.getElementById('crop-temp').value),
      humidity: parseFloat(document.getElementById('crop-hum').value),
      ph: parseFloat(document.getElementById('crop-ph').value),
      rainfall: parseFloat(document.getElementById('crop-rain').value),
      top_k: 6
    };

    try {
      this.showToast('Evaluating agronomic thresholds across 22 major crop species...', 'info');
      const res = await ApiService.recommendCrops(payload);
      const grid = document.getElementById('crop-results-grid');

      if (!grid) return;

      const cropIcons = {
        'rice': '🌾', 'maize': '🌽', 'chickpea': '🫘', 'kidneybeans': '🫘', 'pigeonpeas': '🌱',
        'mothbeans': '🌱', 'mungbean': '🌱', 'blackgram': '🌱', 'lentil': '🍲', 'pomegranate': '🍎',
        'banana': '🍌', 'mango': '🥭', 'grapes': '🍇', 'watermelon': '🍉', 'muskmelon': '🍈',
        'apple': '🍎', 'orange': '🍊', 'papaya': '🍈', 'coconut': '🥥', 'cotton': '🧶',
        'jute': '🧵', 'coffee': '☕'
      };

      grid.innerHTML = res.recommendations.map((rec, index) => {
        const icon = cropIcons[rec.crop_code] || '🌱';
        return `
          <div class="crop-rec-card">
            <div class="crop-rank-badge">#${index + 1}</div>
            <div class="crop-title-row">
              <span class="crop-icon-large">${icon}</span>
              <div>
                <h3>${rec.crop}</h3>
                <span style="font-size:0.76rem; color:var(--text-dim); text-transform:uppercase;">Crop Code: ${rec.crop_code}</span>
              </div>
            </div>

            <div class="crop-score-bar-wrapper">
              <div class="crop-score-header">
                <span>Suitability Match</span>
                <strong style="color:var(--emerald-400); font-family:'JetBrains Mono';">${rec.score}%</strong>
              </div>
              <div class="crop-score-track">
                <div class="crop-score-fill" style="width:${rec.score}%;"></div>
              </div>
            </div>

            <div style="font-size:0.78rem; display:flex; justify-content:space-between; color:var(--text-dim);">
              <span>NPK: ${rec.sub_scores.npk_score}%</span>
              <span>Climate: ${rec.sub_scores.climate_score}%</span>
              <span>pH: ${rec.sub_scores.ph_score}%</span>
            </div>

            <ul class="crop-reasons-list">
              ${rec.reasons.map(r => `<li>${r}</li>`).join('')}
            </ul>
          </div>
        `;
      }).join('');

      this.showToast('Top crop recommendations generated!', 'success');
    } catch (err) {
      this.showToast(err.message, 'danger');
    }
  }

  async loadTreatmentPage(cropFilter = '', conditionFilter = '') {
    const grid = document.getElementById('treatment-results-grid');
    if (!grid) return;

    try {
      const res = await ApiService.getTreatments(cropFilter, conditionFilter);
      if (!res.treatments || res.treatments.length === 0) {
        grid.innerHTML = `<div style="grid-column:1/-1; text-align:center; padding:32px; color:var(--text-dim);">No treatment guidelines match your search query.</div>`;
        return;
      }

      grid.innerHTML = res.treatments.map(t => `
        <div class="treatment-card">
          <div class="treatment-header">
            <span class="treatment-crop-tag">${t.crop}</span>
            <span class="badge ${t.severity === 'high' ? 'danger' : 'warning'}">${t.severity.toUpperCase()} RISK</span>
          </div>
          <h4>${t.condition}</h4>

          <div class="treatment-block">
            <span class="treatment-block-label">Recommended Treatment & Dosage</span>
            <div class="treatment-block-content">${t.treatment}</div>
          </div>

          <div class="treatment-block">
            <span class="treatment-block-label">Biological / Cultural Prevention</span>
            <div class="treatment-block-content" style="border-left-color:var(--cyan-400);">${t.preventive_measure}</div>
          </div>

          <div style="font-size:0.78rem; color:var(--text-dim); display:flex; flex-direction:column; gap:4px; margin-top:4px;">
            <span><strong>Timing:</strong> ${t.timing}</span>
            <span><strong>Precautions:</strong> ${t.precautions}</span>
          </div>
        </div>
      `).join('');
    } catch (err) {
      this.showToast(err.message, 'danger');
    }
  }

  async handleDiseaseImage(file) {
    const preview = document.getElementById('disease-preview-img');
    const resultBox = document.getElementById('disease-result-box');
    
    // Show image preview
    const reader = new FileReader();
    reader.onload = (e) => {
      preview.src = e.target.result;
      preview.style.display = 'block';
    };
    reader.readAsDataURL(file);

    try {
      this.showToast('Submitting leaf image to integration endpoint...', 'info');
      const res = await ApiService.testDiseaseUpload(file);
      
      resultBox.style.display = 'block';
      document.getElementById('disease-spec-box').textContent = JSON.stringify(res.future_spec, null, 2);
      this.showToast('Notice: Disease detection model is ON HOLD (Contract verified)', 'warning');
    } catch (err) {
      this.showToast(err.message, 'danger');
    }
  }

  async loadAnalyticsPage() {
    try {
      this.showToast('Fetching 65,000+ TEROS 10 dataset observations...', 'info');
      const data = await ApiService.getHistoricalTrends();
      ChartRenderer.renderHistoricalTrends('analytics-trends-canvas', data.trends);
      document.getElementById('trends-record-count').textContent = `${data.count} Multi-Sensor Time-Series Points`;
    } catch (err) {
      this.showToast('Failed to load sensor analytics data', 'danger');
    }
  }

  async loadSettingsPage() {
    try {
      const s = await ApiService.getSettings();
      document.getElementById('setting-data-mode').value = s.data_mode;
      document.getElementById('setting-city').value = s.weather_city;
      document.getElementById('setting-api-configured').textContent = s.weather_api_configured ? 'Configured ✅' : 'Not Set (Using Dataset)';
      document.getElementById('setting-database').textContent = s.database_backend;
      document.getElementById('setting-sensor-provider').textContent = s.hardware_abstraction.active_provider;
    } catch (err) {
      this.showToast('Failed to load settings', 'danger');
    }
  }

  async handleSettingsSave() {
    const payload = {
      data_mode: document.getElementById('setting-data-mode').value,
      weather_city: document.getElementById('setting-city').value,
      weather_api_key: document.getElementById('setting-api-key').value
    };

    try {
      const res = await ApiService.updateSettings(payload);
      this.showToast(res.message, 'success');
      this.updateModeBadges(res.active_mode_badge);
      await this.loadInitialData();
    } catch (err) {
      this.showToast(err.message, 'danger');
    }
  }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  window.krishiApp = new KrishiRakshakApp();
});
