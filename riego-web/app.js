
const API_URL = "https://api.sistemaderiego.online";
const API_TOKEN = "MI_TOKEN_SUPER_SEGURO_12345"; // cambiar por seguro real

const valvesContainer = document.getElementById("valves-container");

// CREAR TARJETAS DE VÁLVULAS
function createValveCard(id, state) {
  const card = document.createElement("div");
  card.classList.add("valve-card");
  if (state) card.classList.add("active");
  card.id = `valve-${id}`;

  card.innerHTML = `
    <h2>Válvula ${id}</h2>
    <p>Estado: <span class="state-text">${state ? "ON" : "OFF"}</span></p>
    <button onclick="toggleValve(${id})">${state ? "Apagar" : "Encender"}</button>
    <input type="number" id="time-${id}" placeholder="Segundos">
    <button onclick="scheduleValve(${id})">Programar</button>
  `;

  valvesContainer.appendChild(card);
}

// CARGAR ESTADO INICIAL
async function loadStatus() {
  const res = await fetch(`${API_URL}/status`, {
    headers: { "x-api-token": API_TOKEN }
  });
  const data = await res.json();
  valvesContainer.innerHTML = "";
  for (let id = 1; id <= 12; id++) {
    createValveCard(id, data[id]);
  }
}

// ENCENDER / APAGAR
async function toggleValve(id) {
  const card = document.getElementById(`valve-${id}`);
  const state = card.classList.contains("active");
  const endpoint = state ? "off" : "on";

  await fetch(`${API_URL}/valve/${id}/${endpoint}`, {
    method: "POST",
    headers: { "x-api-token": API_TOKEN }
  });

  loadStatus();
}

// PROGRAMAR VÁLVULA
async function scheduleValve(id) {
  const seconds = parseInt(document.getElementById(`time-${id}`).value);
  if (!seconds || seconds <= 0) return alert("Ingresa segundos válidos");

  await fetch(`${API_URL}/valve/${id}/schedule?seconds=${seconds}`, {
    method: "POST",
    headers: { "x-api-token": API_TOKEN }
  });

  alert(`Válvula ${id} programada por ${seconds} segundos`);
  loadStatus();
}

// CARGAR AL INICIO
loadStatus();
