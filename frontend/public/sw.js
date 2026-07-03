/* Service worker mínimo: instala la PWA y sirve el shell si no hay red.
   Estrategia network-first — en hackathon el código cambia a cada rato. */
const CACHE = 'nino-v1';

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(['/', '/paciente'])));
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))),
  );
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request)
      .then((res) => {
        const copia = res.clone();
        caches.open(CACHE).then((c) => c.put(e.request, copia));
        return res;
      })
      .catch(() => caches.match(e.request).then((r) => r ?? caches.match('/'))),
  );
});
