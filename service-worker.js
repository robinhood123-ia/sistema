const CACHE_NAME = 'sistema-cache-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/manifest.json',
  '/style.css',
  '/app.js',
  '/icon-192.png',
  '/icon-512.png',
  '/sistemairrigacion.jpg'
];

self.addEventListener('install', (event) => {
  console.log('Service Worker: installing and caching assets');
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS_TO_CACHE))
      .catch(err => console.error('Cache addAll error:', err))
  );
});

self.addEventListener('activate', (event) => {
  console.log('Service Worker: activated');
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      )
    )
  );
});

self.addEventListener('fetch', (event) => {
  // Para peticiones a la API: preferir red (network-first)
  if (event.request.url.includes('/valve') || event.request.url.includes('/status') || event.request.method !== 'GET') {
    event.respondWith(
      fetch(event.request).catch(() => caches.match(event.request))
    );
    return;
  }

  // Para recursos estáticos: cache-first
  event.respondWith(
    caches.match(event.request).then(cachedResp => {
      if (cachedResp) return cachedResp;
      return fetch(event.request)
        .then(networkResp => {
          // Almacenar en cache una copia para la próxima vez
          if (!networkResp || networkResp.status !== 200 || networkResp.type === 'opaque') return networkResp;
          const respClone = networkResp.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, respClone));
          return networkResp;
        })
        .catch(() => {
          // Si es navegación y no hay red: devolver index.html en cache
          if (event.request.mode === 'navigate') {
            return caches.match('/index.html');
          }
        });
    })
  );
});
