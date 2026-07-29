// Caminho completo: C:\Users\vlula\OneDrive\Área de Trabalho\Projetos Backup\NETTSTUDY\static\service-worker.js
// Data e hora do último recode: 29/07/2026 16:15 -03:00
// Motivo da alteração: criar cache básico da interface inicial do NettStudy.

const CACHE_NAME = "nettstudy-v1";
const ARQUIVOS = ["/", "/login", "/portal", "/static/css/dashboard.css"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ARQUIVOS)));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key)))));
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  event.respondWith(fetch(event.request).catch(() => caches.match(event.request)));
});
