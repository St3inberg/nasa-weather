import { LitElement, html, css } from 'https://cdn.jsdelivr.net/gh/lit/lit@3/index.js';

// Public domain NASA Mars surface photo (Curiosity rover, Gale Crater)
const MARS_BG_IMAGE = 'https://mars.nasa.gov/system/resources/detail_files/25761_PIA25015-800.jpg';

class MarsWeatherCard extends LitElement {
  static get properties() {
    return {
      hass: { type: Object },
      config: { type: Object },
    };
  }

  setConfig(config) {
    if (!config.entity) throw new Error('You must define an entity');
    this.config = config;
  }

  _state(entityId) {
    return this.hass?.states?.[entityId];
  }

  _val(entityId) {
    return this._state(entityId)?.state ?? 'N/A';
  }

  static get styles() {
    return css`
      :host { display: block; }

      .card {
        border-radius: 12px;
        overflow: hidden;
        position: relative;
        min-height: 320px;
        color: #fff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
      }

      .bg {
        position: absolute;
        inset: 0;
        background-image: var(--mars-bg-image, linear-gradient(135deg, #c1440e 0%, #4a1f05 100%));
        background-size: cover;
        background-position: center;
        filter: brightness(0.75);
      }

      .overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(to top, rgba(0,0,0,0.75) 0%, transparent 60%);
      }

      .content {
        position: relative;
        z-index: 2;
        padding: 20px;
      }

      .header {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-bottom: 16px;
      }

      .title {
        font-size: 22px;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 6px rgba(0,0,0,0.6);
      }

      .sol {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.8;
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.25);
        padding: 3px 10px;
        border-radius: 20px;
        backdrop-filter: blur(4px);
      }

      .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 10px;
      }

      .tile {
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 8px;
        padding: 12px;
        backdrop-filter: blur(8px);
      }

      .tile-label {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        opacity: 0.75;
        margin-bottom: 6px;
      }

      .tile-value {
        font-size: 20px;
        font-weight: 700;
        color: #f5a623;
      }

      .tile-unit {
        font-size: 12px;
        opacity: 0.85;
        margin-left: 2px;
      }

      .footer {
        margin-top: 12px;
        font-size: 10px;
        opacity: 0.55;
        text-align: center;
      }

      .error {
        padding: 20px;
        background: rgba(200,50,50,0.3);
        border-radius: 8px;
        text-align: center;
      }
    `;
  }

  render() {
    const base = this.config.entity;
    const mainState = this._state(base);

    const bgImage = this.config.background_image || MARS_BG_IMAGE;

    if (!mainState) {
      return html`
        <ha-card>
          <div class="card" style="--mars-bg-image: url('${bgImage}')">
            <div class="bg"></div>
            <div class="overlay"></div>
            <div class="content">
              <div class="error">Entity not found: ${base}</div>
            </div>
          </div>
        </ha-card>
      `;
    }

    // Derive sibling entity IDs from the base entity
    const domain = 'sensor';
    const prefix = base.replace(/^sensor\.mars_/, '').replace(/_average$/, '');
    const entities = {
      temp:     `sensor.mars_avg_temperature`,
      pressure: `sensor.mars_avg_pressure`,
      wind:     `sensor.mars_avg_wind_speed`,
      dir:      `sensor.mars_wind_direction`,
    };

    const temp     = mainState.state ?? 'N/A';
    const pressure = this._val(this.config.pressure_entity   || entities.pressure);
    const wind     = this._val(this.config.wind_entity       || entities.wind);
    const dir      = this._val(this.config.direction_entity  || entities.dir);
    const sol      = mainState.attributes?.source_sol;

    return html`
      <ha-card>
        <div class="card" style="--mars-bg-image: url('${bgImage}')">
          <div class="bg"></div>
          <div class="overlay"></div>
          <div class="content">
            <div class="header">
              <h2 class="title">🔴 Mars Weather</h2>
              ${sol ? html`<div class="sol">Sol ${sol}</div>` : ''}
            </div>

            <div class="grid">
              <div class="tile">
                <div class="tile-label">Temperature</div>
                <div class="tile-value">${temp}<span class="tile-unit">°C</span></div>
              </div>
              <div class="tile">
                <div class="tile-label">Pressure</div>
                <div class="tile-value">${pressure}<span class="tile-unit">Pa</span></div>
              </div>
              <div class="tile">
                <div class="tile-label">Wind Speed</div>
                <div class="tile-value">${wind}<span class="tile-unit">m/s</span></div>
              </div>
              <div class="tile">
                <div class="tile-label">Wind Dir</div>
                <div class="tile-value">${dir}</div>
              </div>
            </div>

            <div class="footer">NASA InSight Mars Weather Service</div>
          </div>
        </div>
      </ha-card>
    `;
  }
}

customElements.define('mars-weather-card', MarsWeatherCard);
