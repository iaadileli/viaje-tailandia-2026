# -*- coding: utf-8 -*-
"""Reescribe los bloques <ul class="sitios"> de cada etapa con las fichas nuevas."""
import sys, re, html
import os
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datos1 import BANGKOK, CHIANGRAI
from datos2 import CHIANGDAO, CHIANGMAI
from datos3 import KRABI, KOHJUM, KOHLANTA

# título del bloque en la web -> lista de sitios
MAPA = {
 'Bangkok': BANGKOK, 'Chiang Rai': CHIANGRAI, 'Chiang Dao': CHIANGDAO,
 'Chiang Mai': CHIANGMAI, 'Krabi': KRABI, 'Koh Jum': KOHJUM,
 'Koh Lanta': KOHLANTA,
}
# Los sellos van en SVG y no como caracteres: los símbolos tipo estrella los
# pintaba la fuente de emoji del sistema, descuadrados y a otro tamaño.
_ESTRELLA = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
             '<path d="M12 2.6l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5-5.8-3-5.8 3 1.1-6.5L2.6 9.4l6.5-.9z"/></svg>')
_CUBIERTOS = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
              'stroke-linecap="round"><path d="M7 3v8m0 0v10m0-10a3 3 0 0 0 0-6"/>'
              '<path d="M17 3c-1.8 1.4-2.6 3.4-2.6 5.5 0 1.6.9 2.5 2.6 2.5v10"/></svg>')
_ETIQUETA = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
             'stroke-linejoin="round"><path d="M11.5 2.5H20a1.5 1.5 0 0 1 1.5 1.5v8.5L12 21.5 2.5 12z"/>'
             '<circle cx="17" cy="7" r="1.6" fill="currentColor" stroke="none"/></svg>')
_CLOCHE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" '
           'stroke-linecap="round"><path d="M3 18h18"/><path d="M4.5 15a7.5 7.5 0 0 1 15 0"/>'
           '<path d="M12 7.5V5.5"/><circle cx="12" cy="4" r="1.2" fill="currentColor" stroke="none"/></svg>')
_PUNTO = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
          '<circle cx="12" cy="12" r="6"/></svg>')

SELLOS = {'leyenda':  (_ESTRELLA,  'lleva décadas abierto'),
          'estrella': (_ESTRELLA,  'estrella Michelin 2026'),
          'bib':      (_CUBIERTOS, 'Bib Gourmand Michelin 2026: se come bien y barato'),
          'local':    (_PUNTO,     'donde come la gente de aquí'),
          'barato':   (_ETIQUETA,  'de los más baratos: comida de calle a precio local'),
          'cena':     (_CLOCHE,    'mesa especial: para darse un capricho una noche')}

def ficha(s):
    # el noveno campo, si está, es el enlace para reservar
    reserva = s[8] if len(s) > 8 else None
    nombre, sello, zona, que, pide, horario, precio, consulta = s[:8]
    e = html.escape
    marca = ''
    if sello in SELLOS:
        sym, tit = SELLOS[sello]
        marca = f'<span class="sello {sello}" title="{tit}">{sym}</span>'
    # los puestos callejeros sin ficha en Maps se enlazan por coordenadas
    url = 'https://www.google.com/maps/search/?api=1&query=' + quote(consulta.lstrip('@'))
    partes = [f'      <li><span class="nombre">{e(nombre)}</span>{marca} — <span class="dir">{e(zona)}</span> · {e(que)}']
    partes.append(f'        <span class="pedir"><b>Pide</b> {e(pide)}</span>')
    if horario != '—':
        partes.append(f'        <span class="datos">🕐 {e(horario)} · 💵 {e(precio)}</span>')
    enlaces = f'<a href="{url}" target="_blank" rel="noopener">📍 Maps</a>'
    if reserva:
        etq = '📞 Llamar para reservar' if reserva.startswith('tel:') else '🍽 Reservar'
        destino = '' if reserva.startswith('tel:') else ' target="_blank" rel="noopener"'
        enlaces += f' <a class="reservar" href="{reserva}"{destino}>{etq}</a>'
    partes.append(f'        {enlaces}</li>')
    return '\n'.join(partes)

def bloque(sitios):
    return '<ul class="sitios">\n' + '\n'.join(ficha(s) for s in sitios) + '\n    </ul>'

p = '/home/adil/Escritorio/viaje-tailandia/index.html'
h = open(p).read()
cambios = 0
for titulo, sitios in MAPA.items():
    # localizar "Qué y dónde comer en <titulo>" y su <ul class="sitios">…</ul>
    # Acotar a la sección: si el <ul> buscado no está dentro, no vale.
    # (Sin esto, el regex saltaba a la etapa siguiente y le pisaba las fichas.)
    mh = re.search(r'Qué y dónde comer en ' + re.escape(titulo) + r'</h3>', h)
    if not mh:
        print('  NO ENCONTRADO el título de:', titulo); continue
    limite = h.find('</section>', mh.end())
    m = re.compile(r'(Qué y dónde comer en ' + re.escape(titulo) + r'</h3>.*?)<ul class="sitios">.*?</ul>', re.S).search(h, mh.start(), limite)
    if not m:
        print('  SIN <ul class="sitios"> dentro de la sección:', titulo); continue
    h = h[:m.start()] + m.group(1) + bloque(sitios) + h[m.end():]
    cambios += 1
    print(f'  {titulo:14s} {len(sitios)} fichas')

open(p, 'w').write(h)
print(f'{cambios} bloques reescritos')
