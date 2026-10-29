#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Predicción real del tiempo, día a día y en el sitio donde estáis ese día.

Open-Meteo llega a 16 días vista, así que los últimos días del viaje salen
«todavía sin predicción» hasta que entren en el horizonte. La tabla de etapas
de debajo (media de ocho años) sigue valiendo para esos días.

Esto escribe la predicción de hoy en index.html, entre las marcas
<!-- PREDICCION --> y <!-- /PREDICCION -->, para que se vea sin conexión.
El JS del bloque la vuelve a pedir al abrir la web, así que con cobertura
siempre se ve la última.

Uso:  python3 generador/tiempo.py"""
import datetime, json, os, re, sys, urllib.request

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA = {'User-Agent': 'guia-tailandia/1.0 (uso personal)'}

# Coordenadas verificadas en Nominatim (29-oct-2026)
LUGARES = {
    'bkk':   ('Bangkok',    13.7563, 100.5018),
    'crai':  ('Chiang Rai', 19.9105,  99.8406),
    'cdao':  ('Chiang Dao', 19.3696,  98.9657),
    'cmai':  ('Chiang Mai', 18.7883,  98.9853),
    'krabi': ('Krabi',       8.0863,  98.9063),
    'jum':   ('Koh Jum',     7.7926,  98.9913),
    'lanta': ('Koh Lanta',   7.5598,  99.0573),
}
ORDEN = list(LUGARES)

# Dónde pasáis el día. Los días de viaje cuentan como el destino.
def lugar(f):
    tramos = [('2026-11-02', 'bkk'), ('2026-11-04', 'crai'), ('2026-11-06', 'cdao'),
              ('2026-11-10', 'cmai'), ('2026-11-11', 'krabi'), ('2026-11-14', 'jum'),
              ('2026-11-18', 'lanta'), ('2026-11-21', 'bkk')]
    for hasta, l in tramos:
        if f < hasta:
            return l

PRIMER, ULTIMO = '2026-10-30', '2026-11-20'

CIELO = {0:('☀️','despejado'), 1:('🌤️','casi despejado'), 2:('⛅','nubes y claros'), 3:('☁️','nublado'),
         45:('🌫️','niebla'), 48:('🌫️','niebla'),
         51:('🌦️','llovizna'), 53:('🌦️','llovizna'), 55:('🌧️','llovizna fuerte'),
         61:('🌦️','lluvia floja'), 63:('🌧️','lluvia'), 65:('🌧️','lluvia fuerte'),
         80:('🌦️','chubascos'), 81:('🌧️','chubascos'), 82:('🌧️','chubascos fuertes'),
         95:('⛈️','tormentas'), 96:('⛈️','tormentas'), 99:('⛈️','tormentas')}
SEMANA = ['lun','mar','mié','jue','vie','sáb','dom']
MESES = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto',
         'septiembre','octubre','noviembre','diciembre']

API = ('https://api.open-meteo.com/v1/forecast?latitude=%s&longitude=%s'
       '&daily=weather_code,temperature_2m_max,temperature_2m_min,'
       'precipitation_probability_max,precipitation_sum'
       '&timezone=Asia%%2FBangkok&forecast_days=16'
       % (','.join(str(LUGARES[k][1]) for k in ORDEN), ','.join(str(LUGARES[k][2]) for k in ORDEN)))

resp = json.load(urllib.request.urlopen(urllib.request.Request(API, headers=UA), timeout=30))
pred = {}
for k, r in zip(ORDEN, resp):
    d = r['daily']
    for i, f in enumerate(d['time']):
        pred[(k, f)] = (d['weather_code'][i], d['temperature_2m_max'][i], d['temperature_2m_min'][i],
                        d['precipitation_probability_max'][i], d['precipitation_sum'][i])

filas, con, sin = [], 0, 0
f = datetime.date.fromisoformat(PRIMER)
while f.isoformat() <= ULTIMO:
    iso = f.isoformat()
    k = lugar(iso)
    p = pred.get((k, iso))
    cuando = '%s %d %s' % (SEMANA[f.weekday()], f.day, 'oct' if f.month == 10 else 'nov')
    if p and p[1] is not None:
        con += 1
        e, t = CIELO.get(p[0], ('🌡️', 'variable'))
        prob, mm = p[3] or 0, p[4] or 0
        celdas = ('<td class="pr-cielo">%s %s</td><td class="clima-t"><span class="t-max">%d°</span> / '
                  '<span class="t-min">%d°</span></td><td class="clima-ll">%d %%<br>'
                  '<span class="clima-fecha">%s mm</span></td>'
                  % (e, t, round(p[1]), round(p[2]), prob, ('%.1f' % mm).replace('.', ',')))
    else:
        sin += 1
        celdas = ('<td class="pr-cielo pr-sin" colspan="3">todavía sin predicción · '
                  'mira la media de la etapa abajo</td>')
    filas.append('      <tr data-t="%s" data-l="%s"><td><b>%s</b></td><td>%s</td>%s</tr>'
                 % (iso, k, cuando, LUGARES[k][0], celdas))
    f += datetime.timedelta(days=1)

hoy = datetime.date.today()
sello = 'Predicción del %d de %s · se actualiza sola al abrir la web con cobertura' % (hoy.day, MESES[hoy.month-1])

coords_js = json.dumps([[k, LUGARES[k][1], LUGARES[k][2]] for k in ORDEN])
bloque = '''<!-- PREDICCION -->
  <h3 class="pr-tit">La predicción real, día a día</h3>
  <p class="pr-nota">Cada día, el tiempo del sitio donde estaréis. Los modelos llegan a dos semanas: los días
  que todavía no tienen predicción se irán rellenando solos. <b>En el trópico casi todos los días salen
  «tormentas»</b>: es el chaparrón de la tarde. Fijaos más en los milímetros que en el dibujo: con menos de
  5 mm es un rato de agua y nada más.</p>
  <div class="tabla-wrap">
    <table class="hoteles clima prediccion" id="prediccion">
      <thead><tr><th>Día</th><th>Dónde</th><th>Cielo</th><th>Día / noche</th><th>Lluvia</th></tr></thead>
      <tbody>
%s
      </tbody>
    </table>
  </div>
  <p class="pr-sello" id="prSello">%s</p>
<script>
/* Repinta la predicción con lo último de Open-Meteo. Si no hay red, se queda la escrita. */
(function(){
  var tabla = document.getElementById('prediccion');
  if (!tabla) return;
  var L = %s;
  var CIELO = {0:['☀️','despejado'],1:['🌤️','casi despejado'],2:['⛅','nubes y claros'],3:['☁️','nublado'],
    45:['🌫️','niebla'],48:['🌫️','niebla'],51:['🌦️','llovizna'],53:['🌦️','llovizna'],55:['🌧️','llovizna fuerte'],
    61:['🌦️','lluvia floja'],63:['🌧️','lluvia'],65:['🌧️','lluvia fuerte'],
    80:['🌦️','chubascos'],81:['🌧️','chubascos'],82:['🌧️','chubascos fuertes'],
    95:['⛈️','tormentas'],96:['⛈️','tormentas'],99:['⛈️','tormentas']};
  var MESES = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
  var url = 'https://api.open-meteo.com/v1/forecast?latitude=' + L.map(function(x){return x[1];}).join(',') +
    '&longitude=' + L.map(function(x){return x[2];}).join(',') +
    '&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum' +
    '&timezone=Asia%%2FBangkok&forecast_days=16';
  fetch(url).then(function(r){ return r.json(); }).then(function(res){
    if (!Array.isArray(res)) return;
    var cambiados = 0;
    res.forEach(function(r, n){
      var d = r && r.daily; if (!d || !d.time) return;
      d.time.forEach(function(f, i){
        var fila = tabla.querySelector('tr[data-t="' + f + '"][data-l="' + L[n][0] + '"]');
        if (!fila || d.temperature_2m_max[i] == null) return;
        var c = CIELO[d.weather_code[i]] || ['🌡️','variable'];
        var mm = (d.precipitation_sum[i] || 0).toFixed(1).replace('.', ',');
        var celdas = fila.querySelectorAll('td');
        for (var j = celdas.length - 1; j >= 2; j--) celdas[j].remove();
        fila.insertAdjacentHTML('beforeend',
          '<td class="pr-cielo">' + c[0] + ' ' + c[1] + '</td>' +
          '<td class="clima-t"><span class="t-max">' + Math.round(d.temperature_2m_max[i]) + '°</span> / ' +
          '<span class="t-min">' + Math.round(d.temperature_2m_min[i]) + '°</span></td>' +
          '<td class="clima-ll">' + (d.precipitation_probability_max[i] || 0) + ' %%<br>' +
          '<span class="clima-fecha">' + mm + ' mm</span></td>');
        cambiados++;
      });
    });
    var s = document.getElementById('prSello');
    if (s && cambiados) {
      var h = new Date();
      s.textContent = 'Predicción de hoy, ' + h.getDate() + ' de ' + MESES[h.getMonth()] + ', a las ' +
        String(h.getHours()).padStart(2,'0') + ':' + String(h.getMinutes()).padStart(2,'0');
    }
  }).catch(function(){});
})();
</script>
  <h3 class="pr-tit">Lo normal en esas fechas, etapa por etapa</h3>
<!-- /PREDICCION -->''' % ('\n'.join(filas), sello, coords_js)

html = open('index.html', encoding='utf-8').read()
if '<!-- PREDICCION -->' in html:
    html = re.sub(r'<!-- PREDICCION -->.*?<!-- /PREDICCION -->', lambda m: bloque, html, flags=re.S)
else:
    # Primera vez: justo antes de la tabla de medias por etapa
    ancla = '  <div class="tabla-wrap">\n    <table class="hoteles clima">'
    if html.count(ancla) != 1:
        sys.exit('No encuentro la tabla del clima en index.html')
    html = html.replace(ancla, '  ' + bloque + '\n\n' + ancla)
open('index.html', 'w', encoding='utf-8').write(html)
print('Predicción escrita: %d días con datos, %d todavía sin predicción' % (con, sin))
