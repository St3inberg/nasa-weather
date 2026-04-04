import { LitElement, html, css } from 'https://cdn.jsdelivr.net/gh/lit/lit@3/index.js';

class MarsWeatherCard extends LitElement {
  static get properties() {
    return {
      hass: { type: Object },
      config: { type: Object },
      data: { type: Object }
    };
  }

  setConfig(config) {
    this.config = config;
  }

  connectedCallback() {
    super.connectedCallback();
    this.updateData();
    // Update every hour
    setInterval(() => this.updateData(), 3600000);
  }

  updateData() {
    if (!this.config || !this.config.entity) return;
    this.requestUpdate();
  }

  getWeatherData() {
    if (!this.hass || !this.config || !this.config.entity) return null;
    return this.hass.states[this.config.entity];
  }

  static get styles() {
    return css`
      :host {
        --mars-bg: linear-gradient(135deg, #c1440e 0%, #8b3a0c 50%, #4a1f05 100%);
        --mars-dark: #3d1a04;
        --mars-accent: #e67e22;
      }

      .card {
        background: var(--mars-bg);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        color: #fff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        position: relative;
        overflow: hidden;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }

      .card::before {
        content: '';
        position: absolute;
        top: 0;
        right: -20%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
      }

      @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
      }

      .content {
        position: relative;
        z-index: 2;
      }

      .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
        flex-wrap: wrap;
      }

      .title {
        font-size: 28px;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
      }

      .status {
        font-size: 12px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
        background: rgba(255, 255, 255, 0.2);
        padding: 4px 12px;
        border-radius: 20px;
      }

      .weather-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 16px;
        margin-bottom: 16px;
      }

      .weather-item {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        padding: 16px;
        backdrop-filter: blur(10px);
      }

      .weather-label {
        font-size: 12px;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
      }

      .weather-value {
        font-size: 24px;
        font-weight: bold;
        color: var(--mars-accent);
      }

      .weather-unit {
        font-size: 14px;
        opacity: 0.9;
        margin-left: 4px;
      }

      .footer {
        font-size: 11px;
        opacity: 0.7;
        margin-top: 16px;
        text-align: center;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding-top: 12px;
      }

      .error {
        background: rgba(220, 53, 69, 0.2);
        border: 1px solid rgba(220, 53, 69, 0.5);
        padding: 16px;
        border-radius: 8px;
        text-align: center;
      }

      .planet-icon {
        font-size: 48px;
        margin-right: 16px;
      }
    `;
  }

  render() {
    const state = this.getWeatherData();
    
    if (!state) {
      return html`
        <div class="card">
          <div class="content">
            <div class="error">
              Entity not found: ${this.config.entity}
            </div>
          </div>
        </div>
      `;
    }

    const temp = state.state || 'N/A';
    const attributes = state.attributes || {};
    const updated = attributes.updated_at || 'Unknown';

    return html`
      <div class="card">
        <div class="content">
          <div class="header">
            <div style="display: flex; align-items: center;">
              <span class="planet-icon">🔴</span>
              <h2 class="title">Mars Weather</h2>
            </div>
            <div class="status">Live Data</div>
          </div>

          <div class="weather-grid">
            <div class="weather-item">
              <div class="weather-label">Temperature</div>
              <div class="weather-value">
                ${temp}
                <span class="weather-unit">°C</span>
              </div>
            </div>
            <div class="weather-item">
              <div class="weather-label">Pressure</div>
              <div class="weather-value">
                ${attributes.pressure || 'N/A'}
                <span class="weather-unit">Pa</span>
              </div>
            </div>
            <div class="weather-item">
              <div class="weather-label">Wind Speed</div>
              <div class="weather-value">
                ${attributes.wind_speed || 'N/A'}
                <span class="weather-unit">m/s</span>
              </div>
            </div>
            <div class="weather-item">
              <div class="weather-label">Wind Direction</div>
              <div class="weather-value">
                ${attributes.wind_direction || 'N/A'}
              </div>
            </div>
          </div>

          <div class="footer">
            Last updated: ${updated} | Data from NASA InSight Mars Weather Service
          </div>
        </div>
      </div>
    `;
  }
}

customElements.define('mars-weather-card', MarsWeatherCard);
