const CACHE = 'tailandia2026-v2';
const RECURSOS = [
  './',
  'index.html',
  'manifest.webmanifest',
  'audio/catalogo.js',
  'img/comida-gaeng-som.jpg',
  'img/comida-hoi-tod.jpg',
  'img/comida-jok.jpg',
  'img/comida-kanom-jeen.jpg',
  'img/comida-khanom-krok.jpg',
  'img/comida-khao-kha-moo.jpg',
  'img/comida-khao-man-gai.jpg',
  'img/comida-khao-mok-gai.jpg',
  'img/comida-kluay-tod.jpg',
  'img/comida-kuaitiao.jpg',
  'img/comida-laab.jpg',
  'img/comida-nam-prik-ong.jpg',
  'img/comida-pad-krapao.jpg',
  'img/comida-patongko.jpg',

  'tailandia-donde-comer.kml',
  'audio/frases/agua.mp3',
  'audio/frases/alergia.mp3',
  'audio/frases/ayuda.mp3',
  'audio/frases/bano.mp3',
  'audio/frases/caro.mp3',
  'audio/frases/carta.mp3',
  'audio/frases/cuanto.mp3',
  'audio/frases/cuantotarda.mp3',
  'audio/frases/cuenta.mp3',
  'audio/frases/gracias.mp3',
  'audio/frases/hola.mp3',
  'audio/frases/hospital.mp3',
  'audio/frases/ingles.mp3',
  'audio/frases/llevar.mp3',
  'audio/frases/maipenrai.mp3',
  'audio/frases/medico.mp3',
  'audio/frases/no.mp3',
  'audio/frases/noentiendo.mp3',
  'audio/frases/nopicante.mp3',
  'audio/frases/noquiero.mp3',
  'audio/frases/parar.mp3',
  'audio/frases/perdon.mp3',
  'audio/frases/pococpicante.mp3',
  'audio/frases/policia.mp3',
  'audio/frases/rebaja.mp3',
  'audio/frases/recto.mp3',
  'audio/frases/rico.mp3',
  'audio/frases/si.mp3',
  'audio/frases/sincilantro.mp3',
  'audio/frases/taximetro.mp3',
  'audio/frases/vegetariano.mp3',
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
  'img/koh-lanta.jpg',
  'img/koh-rok.jpg',
  'img/koh-jum.jpg',
  'img/koh-jum-barca.jpg',
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
// Los audios se piden por trozos (cabecera Range). Si están en la caché hay que
// servirlos troceados a mano, o el navegador no deja avanzar ni retroceder la pista.
async function desdeCache(peticion) {
  const guardado = await caches.match(peticion, {ignoreSearch: true});
  const rango = peticion.headers.get('range');
  if (!guardado || !rango) return guardado;

  const datos = await guardado.arrayBuffer();
  const trozos = /bytes=(\d*)-(\d*)/.exec(rango);
  let ini = trozos && trozos[1] ? parseInt(trozos[1], 10) : 0;
  let fin = trozos && trozos[2] ? parseInt(trozos[2], 10) : datos.byteLength - 1;
  if (isNaN(ini) || ini >= datos.byteLength) ini = 0;
  if (isNaN(fin) || fin >= datos.byteLength) fin = datos.byteLength - 1;

  return new Response(datos.slice(ini, fin + 1), {
    status: 206,
    statusText: 'Partial Content',
    headers: {
      'Content-Type': guardado.headers.get('Content-Type') || 'application/octet-stream',
      'Content-Range': 'bytes ' + ini + '-' + fin + '/' + datos.byteLength,
      'Content-Length': String(fin - ini + 1),
      'Accept-Ranges': 'bytes'
    }
  });
}

// La página y el catálogo cambian; las fotos y los audios, no.
// Por eso van con estrategias distintas: si todo fuera cache-first, una vez
// guardada la web nunca se verían las actualizaciones.
function esContenidoVivo(peticion, url) {
  return peticion.mode === 'navigate' ||
         url.pathname.endsWith('/') ||
         url.pathname.endsWith('.html') ||
         url.pathname.endsWith('catalogo.js');
}

function guarda(peticion, resp) {
  if (resp && resp.ok && resp.status === 200) {
    const copia = resp.clone();
    caches.open(CACHE).then(c => c.put(peticion, copia)).catch(() => {});
  }
  return resp;
}

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;

  if (esContenidoVivo(e.request, url)) {
    // Primero la red, para ver siempre la última versión. Si no hay cobertura,
    // se tira de lo guardado, que es justo lo que hace falta en el viaje.
    e.respondWith(
      fetch(e.request)
        .then(resp => guarda(e.request, resp))
        .catch(() => caches.match(e.request, {ignoreSearch: true})
          .then(hit => hit || caches.match('index.html', {ignoreSearch: true})))
    );
    return;
  }

  // Fotos, audios y demás: de la caché, que no cambian y pesan.
  e.respondWith(
    desdeCache(e.request).then(hit =>
      hit || fetch(e.request)
        .then(resp => guarda(e.request, resp))
        .catch(() => caches.match('index.html', {ignoreSearch: true}))
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
