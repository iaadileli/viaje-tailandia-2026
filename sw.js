const CACHE = 'tailandia2026-v1';
const RECURSOS = [
  './',
  'index.html',
  'manifest.webmanifest',
  'img/portada.jpg',
  'img/icono-192.png',
  'img/icono-512.png',
  'img/bangkok-gran-palacio.jpg',
  'img/bangkok-jim-thompson.jpg',
  'img/bangkok-wat-arun.jpg',
  'img/bangkok-wat-pho.jpg',
  'img/bangkok-yaowarat.jpg',
  'img/chiang-dao-templo.jpg',
  'img/chiang-dao.jpg',
  'img/chiang-mai-chedi-luang.jpg',
  'img/chiang-mai-doi-suthep.jpg',
  'img/chiang-mai-phra-singh.jpg',
  'img/chiang-rai-te.jpg',
  'img/chiang-rai-templo-azul.jpg',
  'img/chiang-rai-wat-rong-khun.jpg',
  'img/comida-boat-noodles.jpg',
  'img/comida-curry-crab.jpg',
  'img/comida-hang-lay.jpg',
  'img/comida-nam-ngiao.jpg',
  'img/comida-roti.jpg',
  'img/comida-sai-ua.jpg',
  'img/comida-seafood-bbq.jpg',
  'img/comida-som-tam.jpg',
  'img/comida-street.jpg',
  'img/comida-tom-yum.jpg',
  'img/elefantes.jpg',
  'img/khao-soi.jpg',
  'img/koh-hong.jpg',
  'img/koh-lanta.jpg',
  'img/koh-rok.jpg',
  'img/koh-yao-noi.jpg',
  'img/krabi.jpg',
  'img/lanta-old-town.jpg',
  'img/mango-sticky-rice.jpg',
  'img/massaman.jpg',
  'img/pad-thai.jpg'
];


self.addEventListener('install', e => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(
  caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim())
));

// Cache-first para lo nuestro: una vez guardado, funciona sin conexión.
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  e.respondWith(
    caches.match(e.request, {ignoreSearch: true}).then(hit =>
      hit || fetch(e.request).then(resp => {
        if (resp.ok) { const copia = resp.clone(); caches.open(CACHE).then(c => c.put(e.request, copia)); }
        return resp;
      }).catch(() => caches.match('index.html', {ignoreSearch: true}))
    )
  );
});

// Descarga completa bajo demanda, informando del progreso.
self.addEventListener('message', async e => {
  if (!e.data || e.data.tipo !== 'GUARDAR') return;
  const cliente = e.source;
  const cache = await caches.open(CACHE);
  let hechos = 0;
  for (const r of RECURSOS) {
    try { await cache.add(new Request(r, {cache: 'reload'})); } catch (err) {}
    hechos++;
    cliente && cliente.postMessage({tipo: 'PROGRESO', hechos, total: RECURSOS.length});
  }
  cliente && cliente.postMessage({tipo: 'LISTO', total: RECURSOS.length});
});
