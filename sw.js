const CACHE_NAME = 'labat-mittermayer-offline-v4';

const CRITICAL_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './Sumerian.ttf',
  './Babylonian.ttf',
  './Assyrian.ttf',
  './icons/apple-touch-icon.png',
  './icons/icon-192.png',
  './icons/icon-512.png'
];

const IMAGE_ASSETS = [
  './images/1.png',
  './images/100.png',
  './images/109.png',
  './images/141.png',
  './images/144.png',
  './images/151.png',
  './images/195.png',
  './images/297.png',
  './images/307.png',
  './images/308.png',
  './images/343.png',
  './images/366.png',
  './images/396.png',
  './images/399.png',
  './images/411.png',
  './images/480.png',
  './images/560.png',
  './images/579-1.png',
  './images/579-2.png',
  './images/579-3.png'
];

function fetchWithTimeout(request, ms) {
  if (typeof AbortController === 'undefined') {
    return fetch(request);
  }
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ms);
  return fetch(request, { signal: controller.signal }).finally(() => clearTimeout(timer));
}

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      await Promise.allSettled(
        CRITICAL_ASSETS.map((url) =>
          cache.add(new Request(url, { cache: 'reload' })).catch(() => {})
        )
      );
      await Promise.allSettled(
        IMAGE_ASSETS.map((url) =>
          cache.add(new Request(url, { cache: 'reload' })).catch(() => {})
        )
      );
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const req = event.request;
  const url = new URL(req.url);
  const isNav = req.mode === 'navigate' || req.destination === 'document';
  const isCodeOrData =
    isNav ||
    /\.(html|htm|json|js|css)$/i.test(url.pathname) ||
    url.pathname.endsWith('/');

  const networkPromise = isCodeOrData
    ? fetchWithTimeout(new Request(req, { cache: 'no-store' }), 2200)
        .catch(() => fetchWithTimeout(req, 2200))
    : fetch(req);

  event.respondWith(
    networkPromise
      .then((networkResp) => {
        if (networkResp && (networkResp.ok || networkResp.type === 'opaque')) {
          const copy = networkResp.clone();
          const navCopy1 = isNav ? networkResp.clone() : null;
          const navCopy2 = isNav ? networkResp.clone() : null;
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(req, copy);
            if (navCopy1) cache.put('./index.html', navCopy1);
            if (navCopy2) cache.put('./', navCopy2);
          }).catch(() => {});
        }
        return networkResp;
      })
      .catch(async () => {
        const exact = await caches.match(req, { ignoreSearch: false });
        if (exact) return exact;

        const loose = await caches.match(req, { ignoreSearch: true });
        if (loose) return loose;

        if (isNav) {
          return (
            (await caches.match(req, { ignoreSearch: true })) ||
            (await caches.match('./index.html')) ||
            (await caches.match('./')) ||
            (await caches.match('index.html'))
          );
        }
        return undefined;
      })
  );
});
