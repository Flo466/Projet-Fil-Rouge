/**
 * Site B - Application Web
 * Script Front-End (app.js)
 * Rôle : Gestion du thème (clair/sombre) et communication REST avec le Back-End Python
 */

// Configuration de l'endpoint Back-End
const API_BASE_URL = window.location.port === "8000" ? "" : "http://localhost:8000";

// Éléments DOM
const themeToggleBtn = document.getElementById("theme-toggle");
const themeIcon = document.getElementById("theme-icon");
const refreshBtn = document.getElementById("refresh-status-btn");
const connectionAlert = document.getElementById("connection-alert");

// Indicateurs
const backendIndicator = document.getElementById("backend-indicator");
const backendStatusText = document.getElementById("backend-status-text");
const pulseIndicator = document.getElementById("pulse-indicator");

// Champs de télémétrie
const telemetryStatus = document.getElementById("telemetry-status");
const telemetryVersion = document.getElementById("telemetry-version");
const telemetryOs = document.getElementById("telemetry-os");
const telemetryUptime = document.getElementById("telemetry-uptime");

/**
 * Initialisation de la gestion du thème (clair / sombre)
 */
function initTheme() {
  const savedTheme = localStorage.getItem("theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const currentTheme = savedTheme || (prefersDark ? "dark" : "light");

  document.documentElement.setAttribute("data-theme", currentTheme);
  updateThemeIcon(currentTheme);

  themeToggleBtn.addEventListener("click", () => {
    const activeTheme = document.documentElement.getAttribute("data-theme") || "light";
    const newTheme = activeTheme === "dark" ? "light" : "dark";

    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
    updateThemeIcon(newTheme);
  });
}

function updateThemeIcon(theme) {
  themeIcon.textContent = theme === "dark" ? "☀️" : "🌙";
}

/**
 * Interroge l'API REST Python (/api/status)
 */
async function fetchBackendStatus() {
  // État de chargement
  pulseIndicator.className = "pulse-dot checking";
  backendIndicator.className = "status-indicator checking";
  backendStatusText.textContent = "Vérification...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/status`, {
      method: "GET",
      headers: {
        "Accept": "application/json"
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();

    // Mise à jour des valeurs télémétriques
    telemetryStatus.textContent = data.status || "En ligne";
    telemetryVersion.textContent = data.python_version || "Python 3";
    telemetryOs.textContent = `${data.system || "Linux"} (${data.release || ""})`;
    telemetryUptime.textContent = data.uptime || "Actif";

    // Mise à jour visuelle du succès
    backendIndicator.className = "status-indicator online";
    backendStatusText.textContent = "Connecté (Python)";
    pulseIndicator.className = "pulse-dot";
    connectionAlert.classList.add("hidden");

    // Chargement dynamique des services depuis fake_data.json
    await fetchServices();

  } catch (error) {
    // Gestion de l'erreur / Back-End éteint
    telemetryStatus.textContent = "Hors ligne";
    telemetryVersion.textContent = "--";
    telemetryOs.textContent = "--";
    telemetryUptime.textContent = "--";

    backendIndicator.className = "status-indicator offline";
    backendStatusText.textContent = "Déconnecté";
    pulseIndicator.className = "pulse-dot offline";
    connectionAlert.classList.remove("hidden");
  }
}

/**
 * Charge dynamiquement les services depuis l'endpoint /api/services
 */
async function fetchServices() {
  const container = document.getElementById("services-grid");
  if (!container) return;

  try {
    const response = await fetch(`${API_BASE_URL}/api/services`);
    if (!response.ok) return;

    const data = await response.json();
    if (!data.services || !Array.isArray(data.services) || data.services.length === 0) return;

    container.innerHTML = data.services.map(svc => `
      <article class="card">
        <div class="card-icon">${getServiceIcon(svc.id)}</div>
        <h3 class="card-title">${escapeHtml(svc.name)}</h3>
        <p class="card-text">${escapeHtml(svc.description || "")}</p>
        <div class="card-footer">
          <span class="status-indicator online"></span>
          <span class="status-text">${escapeHtml(svc.status)} (${escapeHtml(svc.zone)} &bull; ${escapeHtml(svc.ip)})</span>
        </div>
      </article>
    `).join("");
  } catch (err) {
    // Conservation de la structure HTML statique en cas d'erreur
  }
}

function getServiceIcon(id) {
  if (id.includes("proxy")) return "🛡️";
  if (id.includes("backend") || id.includes("web")) return "⚙️";
  if (id.includes("dns") || id.includes("ad")) return "📁";
  if (id.includes("zabbix")) return "📊";
  if (id.includes("squid")) return "🌐";
  if (id.includes("debian") || id.includes("base")) return "🗄️";
  return "📦";
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

// Initialisation globale
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  fetchBackendStatus();

  // Écouteur de clic sur le bouton de rafraîchissement
  if (refreshBtn) {
    refreshBtn.addEventListener("click", fetchBackendStatus);
  }
});

