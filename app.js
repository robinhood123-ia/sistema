// app.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-app.js";
import { getAuth, signInWithEmailAndPassword, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyAQJfBPBGFo8IujYZeNK3kr6EiX9xCGvdU",
  authDomain: "sistemaderiego-8950d.firebaseapp.com",
  projectId: "sistemaderiego-8950d",
  storageBucket: "sistemaderiego-8950d.appspot.com",
  messagingSenderId: "23168988354",
  appId: "1:23168988354:web:bd1cf85aeec5b0df36f75b"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const API_URL = "https://api.sistemaderiego.online";

const valvesContainer = document.getElementById("valves-container");
const loginForm = document.getElementById("login-form");
const loginBtn = document.getElementById("login-btn");
const loginError = document.getElementById("login-error");

// --- Login ---
loginBtn.addEventListener("click", async () => {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  loginError.style.display = "none";
  try {
    await signInWithEmailAndPassword(auth, email, password);
    // Oculta login y muestra válvulas
    loginForm.style.display = "none";
    document.querySelector("main").style.display = "block";
    loadStatus();
  } catch (err) {
    console.error(err);
    loginError.textContent = "Error en login: " + err.message;
    loginError.style.display = "block";
  }
});

// Mantener sesión iniciada
onAuthStateChanged(auth, (user) => {
  if (user) {
    loginForm.style.display = "none";
    document.querySelector("main").style.display = "block";
    loadStatus();
  } else {
    loginForm.style.display = "block";
    document.querySelector("main").style.display = "none";
  }
});

// --- Funciones de válvulas ---
function createValveCard(id, state) {
  const card = document.createElement("div");
  card.classList.add("valve-card");
  if (state) card.classList.add("active");
  card.id = `valve-${id}`;

  card.innerHTML = `
    <h2>Válvula ${id}</h2>
    <p>Estado: <span class="state-text">${state ? "ON" : "OFF"}</span></p>
    <button class="toggle-btn">${state ? "Apagar" : "Encender"}</button>
    <input type="number" id="time-${id}" placeholder="Segundos">
    <button class="schedule-btn">Programar</button>
  `;

  valvesContainer.appendChild(card);

  // Eventos
  card.querySelector(".toggle-btn").addEventListener("click", () => toggleValve(id));
  card.querySelector(".schedule-btn").addEventListener("click", () => scheduleValve(id));
}

async function loadStatus() {
  try {
    const res = await fetch(`${API_URL}/status`);
    if (!res.ok) throw new Error("Error al obtener estado");
    const data = await res.json();
    valvesContainer.innerHTML = "";
    for (let id = 1; id <= 12; id++) {
      createValveCard(id, data[id]);
    }
  } catch (e) {
    console.error("No se pudo cargar el estado:", e);
    valvesContainer.innerHTML = "<p style='color:red;'>Error conectando al backend</p>";
  }
}

async function toggleValve(id) {
  const card = document.getElementById(`valve-${id}`);
  const state = card.classList.contains("active");
  const endpoint = state ? "off" : "on";

  try {
    await fetch(`${API_URL}/valve/${id}/${endpoint}`, { method: "POST" });
    loadStatus();
  } catch (e) {
    console.error("Error toggleValve:", e);
  }
}

async function scheduleValve(id) {
  const seconds = parseInt(document.getElementById(`time-${id}`).value);
  if (!seconds || seconds <= 0) return alert("Ingresa segundos válidos");

  try {
    await fetch(`${API_URL}/valve/${id}/schedule?seconds=${seconds}`, { method: "POST" });
    alert(`Válvula ${id} programada por ${seconds} segundos`);
    loadStatus();
  } catch (e) {
    console.error("Error scheduleValve:", e);
  }
}
