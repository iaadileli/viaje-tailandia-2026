#!/usr/bin/env node
// Revisión de la web CON LA PÁGINA EN MARCHA, no leyendo el HTML.
// Lo que se lee en el fichero no dice nada de lo que pasa cuando el JS pinta.
// Ejecutar SIEMPRE antes de dar por buena una revisión:  node generador/revisar.mjs
import { existsSync } from 'node:fs';
import path from 'node:path';

const RUTA = process.argv[2] || path.join(import.meta.dirname, '..', 'index.html');
const CANDIDATOS = [
  '/home/adil/Escritorio/viaje-tailandia/node_modules/playwright/index.mjs',
  '/home/adil/proyectos-adil/maquetador-libros/node_modules/playwright/index.mjs',
];
const donde = CANDIDATOS.find(existsSync);
if (!donde) {
  console.error('Falta Playwright. Instalar con:\n  npm i -D playwright && npx playwright install chromium');
  process.exit(2);
}
const { chromium } = await import(donde);

const fallos = [];
const mal = (m) => { fallos.push(m); console.log('  ⚠ ' + m); };
const bien = (m) => console.log('  ✓ ' + m);

const nav = await chromium.launch();
const p = await nav.newPage();
const errores = [];
p.on('pageerror', e => errores.push(e.message));
await p.goto('file://' + path.resolve(RUTA));
await p.waitForTimeout(900);

console.log('\nESTRUCTURA');
const est = await p.evaluate(() => ({
  anidados: [...document.querySelectorAll('.tip .madrugador, .madrugador .tip')].length,
  sinAlt: [...document.querySelectorAll('img')].filter(i => !i.alt).length,
  sinLazy: [...document.querySelectorAll('img')].filter(i => !i.loading || i.loading === 'eager').length,
  rotos: [...document.querySelectorAll('a[href^="#"]')]
    .map(a => a.getAttribute('href')).filter(h => h.length > 1)
    .filter(h => { try { return !document.querySelector(h); } catch { return true; } }),
  sitios: document.querySelectorAll('.sitios li').length,
  repes: (() => {
    const n = [...document.querySelectorAll('.sitios li .nombre')].map(e => e.textContent.trim());
    return n.filter((x, i) => n.indexOf(x) !== i);
  })(),
}));
est.anidados ? mal(`${est.anidados} bloques anidados donde no deben (madrugador dentro de aviso)`)
             : bien('ningún bloque anidado donde no debe');
est.rotos.length ? mal('enlaces internos rotos: ' + est.rotos.join(', ')) : bien('enlaces internos, todos existen');
est.sinAlt ? mal(`${est.sinAlt} imágenes sin alt`) : bien('todas las imágenes con alt');
est.repes.length ? mal('sitios repetidos: ' + est.repes.join(', ')) : bien(`${est.sitios} sitios de comer, ninguno repetido`);

console.log('\nMODO «HOY», DÍA A DÍA');
const primero = await p.$('#hoyVerPrimero');
if (primero) await primero.click();
const dias = await p.evaluate(() => {
  const out = [], norm = t => t.replace(/\s+/g, ' ').trim();
  for (let n = 0; n < 40; n++) {
    const caja = document.querySelector('#hoy .hoy-caja');
    if (!caja) break;
    const fecha = norm(caja.querySelector('.hoy-fecha')?.innerText || '').split('·')[0];
    const plano = norm(caja.innerText);
    const cuenta = (sel) => {
      const el = caja.querySelector(sel); if (!el) return null;
      const frase = norm(el.querySelector('p')?.innerText || el.innerText).slice(0, 60);
      let c = 0, i = -1; while (frase && (i = plano.indexOf(frase, i + 1)) !== -1) c++;
      return c;
    };
    out.push({ fecha, titulo: norm(caja.querySelector('h2')?.innerText || ''),
               mad: cuenta('.hoy-mad'), tip: cuenta('.hoy-tip:not(.hoy-mad)'),
               // ojo: el CSS pone los títulos en mayúsculas y innerText los devuelve así
               comer: [...caja.querySelectorAll('.hoy-tarjeta h4')]
                        .some(h => /comer/i.test(h.innerText)) });
    const sig = document.querySelector('#hoySig'); if (!sig) break;
    const antes = fecha; sig.click();               // pinta() es síncrona
    if (norm(document.querySelector('#hoy .hoy-fecha')?.innerText || '').split('·')[0] === antes) break;
  }
  return out;
});
const totalDias = await p.evaluate(() => new Set([...document.querySelectorAll('[data-fecha]')].map(d => d.dataset.fecha)).size);
dias.length === totalDias ? bien(`se recorren los ${totalDias} días con las flechas`)
  : mal(`las flechas solo llegan a ${dias.length} de ${totalDias} días (se atascan en ${dias.at(-1)?.fecha})`);
const dobles = dias.filter(d => (d.mad ?? 1) !== 1 || (d.tip ?? 1) !== 1);
dobles.length ? mal('texto repetido en: ' + dobles.map(d => d.titulo.split('·')[0]).join(', '))
              : bien(`ningún texto repetido (${dias.filter(d => d.mad).length} días con madrugador)`);
const sinComer = dias.filter(d => !d.comer);
sinComer.length ? mal('días sin dónde comer: ' + sinComer.map(d => d.fecha).join(', '))
                : bien('todos los días tienen dónde comer');

console.log('\nCONSOLA');
errores.length ? mal('errores de JavaScript: ' + errores.join(' | ')) : bien('sin errores de JavaScript');

await nav.close();
console.log(fallos.length ? `\n⚠ ${fallos.length} FALLO(S)` : '\n✓ todo correcto');
process.exit(fallos.length ? 1 : 0);
