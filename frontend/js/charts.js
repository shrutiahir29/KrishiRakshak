/**
 * KRISHIRAKSHAK — Interactive Charting & Visualizations
 * Canvas and SVG-based visualizations with zero external bloat.
 */

export const ChartRenderer = {
  /**
   * Renders the 30-point historical sensor trends chart from KU Leuven dataset.
   */
  renderHistoricalTrends(canvasId, trends) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || !trends || trends.length === 0) return;

    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    
    // Set actual resolution
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);

    const width = rect.width;
    const height = rect.height;
    const pad = { top: 35, right: 30, bottom: 45, left: 50 };
    const chartW = width - pad.left - pad.right;
    const chartH = height - pad.top - pad.bottom;

    ctx.clearRect(0, 0, width, height);

    // Compute min/max
    const moistures = trends.map(t => t.soil_moisture);
    const temps = trends.map(t => t.temperature);
    const minMoist = 0;
    const maxMoist = Math.max(40, Math.ceil(Math.max(...moistures) / 10) * 10);

    // Background Grid
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
    ctx.lineWidth = 1;
    const gridRows = 4;
    for (let i = 0; i <= gridRows; i++) {
      const y = pad.top + (chartH / gridRows) * i;
      ctx.beginPath();
      ctx.moveTo(pad.left, y);
      ctx.lineTo(width - pad.right, y);
      ctx.stroke();

      // Axis label
      const val = Math.round(maxMoist - (maxMoist / gridRows) * i);
      ctx.fillStyle = 'rgba(251, 250, 246, 0.70)';
      ctx.font = '10px "JetBrains Mono", monospace';
      ctx.textAlign = 'right';
      ctx.fillText(`${val}%`, pad.left - 8, y + 3);
    }

    const n = trends.length;
    const getX = (idx) => pad.left + (chartW / (n - 1)) * idx;
    const getYMoist = (val) => pad.top + chartH - (val / maxMoist) * chartH;

    // Draw Rainfall Bars
    trends.forEach((t, i) => {
      if (t.rainfall > 0) {
        const x = getX(i) - 4;
        const barH = Math.min(chartH, t.rainfall * 8);
        const y = pad.top + chartH - barH;
        ctx.fillStyle = 'rgba(56, 189, 248, 0.35)';
        ctx.fillRect(x, y, 8, barH);
      }
    });

    // Draw Soil Moisture Line (Emerald)
    ctx.beginPath();
    ctx.strokeStyle = '#10b981';
    ctx.lineWidth = 2.5;
    ctx.shadowColor = 'rgba(16, 185, 129, 0.4)';
    ctx.shadowBlur = 8;
    trends.forEach((t, i) => {
      const x = getX(i);
      const y = getYMoist(t.soil_moisture);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();
    ctx.shadowBlur = 0; // reset

    // Draw Points
    trends.forEach((t, i) => {
      const x = getX(i);
      const y = getYMoist(t.soil_moisture);
      ctx.beginPath();
      ctx.arc(x, y, 3, 0, Math.PI * 2);
      ctx.fillStyle = '#34d399';
      ctx.fill();
    });

    // Draw Temperature Line (Amber)
    const maxTemp = 40;
    const getYTemp = (val) => pad.top + chartH - (val / maxTemp) * chartH;
    ctx.beginPath();
    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth = 1.8;
    ctx.setLineDash([4, 4]);
    trends.forEach((t, i) => {
      const x = getX(i);
      const y = getYTemp(t.temperature);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();
    ctx.setLineDash([]); // reset

    // Draw Legend at top
    ctx.font = '600 11px Outfit, sans-serif';
    ctx.textAlign = 'left';

    // Item 1: Soil Moisture
    ctx.fillStyle = '#4ade80';
    ctx.fillRect(pad.left, 12, 12, 4);
    ctx.fillStyle = '#fbfaf6';
    ctx.fillText('Soil Moisture (VWC %)', pad.left + 18, 17);

    // Item 2: Temperature
    ctx.fillStyle = '#f59e0b';
    ctx.fillRect(pad.left + 160, 12, 12, 2);
    ctx.fillStyle = '#fbfaf6';
    ctx.fillText('Temperature (°C)', pad.left + 178, 17);

    // Item 3: Rainfall
    ctx.fillStyle = '#38bdf8';
    ctx.fillRect(pad.left + 300, 10, 8, 8);
    ctx.fillStyle = '#fbfaf6';
    ctx.fillText('Precipitation (mm)', pad.left + 314, 17);

    // X-Axis Date markers
    ctx.fillStyle = 'rgba(251, 250, 246, 0.70)';
    ctx.font = '10px "JetBrains Mono", monospace';
    ctx.textAlign = 'center';
    const step = Math.ceil(n / 6);
    for (let i = 0; i < n; i += step) {
      const x = getX(i);
      const label = trends[i].timestamp.split(' ')[0] || `T-${i}`;
      ctx.fillText(label, x, height - 15);
    }
  },

  /**
   * Renders TreeSHAP additive feature attributions with biological reasoning.
   */
  renderShapBars(containerId, shapList) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!shapList || shapList.length === 0) {
      container.innerHTML = `<div style="color:var(--text-dim); padding: 12px;">No SHAP explanation data available.</div>`;
      return;
    }

    // Find max absolute value to normalize bar length (up to 50% max width each side)
    const maxVal = Math.max(...shapList.map(s => Math.abs(s.shap_value)), 0.1);

    const html = shapList.map(item => {
      const val = item.shap_value;
      const isPos = val >= 0;
      const pct = Math.min(50, Math.round((Math.abs(val) / maxVal) * 45));
      const sign = isPos ? '+' : '';
      const colorClass = isPos ? 'positive' : 'negative';
      const textColor = isPos ? '#f87171' : '#34d399';

      return `
        <div class="shap-row" title="${item.description}: ${item.reasoning}">
          <div class="shap-label">
            <span style="font-weight:600;">${item.label}</span>
            <span style="font-size:0.75rem; color:var(--text-dim); display:block;">${item.input_value}</span>
          </div>
          <div class="shap-bar-track">
            <div class="shap-zero-line"></div>
            <div class="shap-bar-fill ${colorClass}" style="width: ${pct}%;"></div>
          </div>
          <div class="shap-val" style="color:${textColor};">
            ${sign}${val.toFixed(3)}
          </div>
        </div>
      `;
    }).join('');

    container.innerHTML = `
      <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:var(--text-dim); text-transform:uppercase; margin-bottom:4px; padding:0 4px;">
        <span>◀ Reduces Pest Risk</span>
        <span>Increases Pest Risk ▶</span>
      </div>
      <div class="shap-container">
        ${html}
      </div>
      <div style="font-size:0.76rem; color:var(--text-dim); margin-top:8px; line-height:1.4;">
        * Generated via exact XGBoost TreeSHAP local additive attribution ($f(x) = E[f(x)] + \\sum \\phi_i$).
      </div>
    `;
  },

  /**
   * Renders SVG Soil Moisture Dial / Gauge
   */
  renderMoistureDial(containerId, moisturePct, fcPct, pwpPct) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const val = Math.min(100, Math.max(0, moisturePct || 0));
    const strokeDash = Math.round((val / 100) * 283); // 2 * PI * 45 = 282.7

    let statusText = 'Optimal Zone';
    let statusColor = '#10b981';
    if (val < (pwpPct || 8)) {
      statusText = 'Critical Deficit (Below PWP)';
      statusColor = '#ef4444';
    } else if (val < (fcPct * 0.65 || 18)) {
      statusText = 'Depleted (Irrigation Needed)';
      statusColor = '#f59e0b';
    } else if (val > (fcPct || 30)) {
      statusText = 'Near Saturation';
      statusColor = '#38bdf8';
    }

    container.innerHTML = `
      <div style="position:relative; width:160px; height:160px; margin:0 auto;">
        <svg viewBox="0 0 100 100" style="width:100%; height:100%; transform: rotate(-90deg);">
          <circle cx="50" cy="50" r="42" fill="none" stroke="rgba(255,255,255,0.14)" stroke-width="8" />
          <circle cx="50" cy="50" r="42" fill="none" stroke="${statusColor}" stroke-width="8"
            stroke-dasharray="264" stroke-dashoffset="${264 - (val / 100) * 264}"
            stroke-linecap="round" style="transition: stroke-dashoffset 0.8s ease;" />
        </svg>
        <div style="position:absolute; top:0; left:0; width:100%; height:100%; display:flex; flex-direction:column; align-items:center; justify-content:center;">
          <span style="font-family:'JetBrains Mono', monospace; font-size:1.8rem; font-weight:800; color:#ffffff;">${val.toFixed(1)}%</span>
          <span style="font-size:0.7rem; color:var(--text-dim); text-transform:uppercase; font-weight:600;">VWC Depth 15cm</span>
        </div>
      </div>
      <div style="text-align:center; margin-top:10px;">
        <span class="badge" style="background:${statusColor}22; color:${statusColor}; border:1px solid ${statusColor}55;">
          ${statusText}
        </span>
      </div>
    `;
  }
};
