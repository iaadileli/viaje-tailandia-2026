#!/usr/bin/env python3
"""Regenera sitios.js (el que usa «¿qué tengo cerca?») desde los datos de comida,
reutilizando las coordenadas ya conocidas. Ejecutar tras cambiar sitios de comer."""
import json, sys, os, re, html
from urllib.parse import quote
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generador'))
from datos1 import BANGKOK, CHIANGRAI
from datos2 import CHIANGDAO, CHIANGMAI
from datos3 import KRABI, KOHJUM, KOHLANTA

ETAPAS = [('bangkok1','Bangkok',BANGKOK), ('chiangrai','Chiang Rai',CHIANGRAI),
          ('chiangdao','Chiang Dao',CHIANGDAO), ('chiangmai','Chiang Mai',CHIANGMAI),
          ('krabi','Krabi',KRABI), ('kohjum','Koh Jum',KOHJUM), ('kohlanta','Koh Lanta',KOHLANTA)]
ZONAS = {'bangkok1':(13.75,100.52),'chiangrai':(19.91,99.84),'chiangdao':(19.37,98.97),
         'chiangmai':(18.79,98.99),'krabi':(8.09,98.91),'kohjum':(7.78,99.05),'kohlanta':(7.62,99.03)}
# fichas que no son un local: no salen en «qué tengo cerca»
NO_SITIO = ['Ojo: no hay cajeros','Cenar en el alojamiento','Cena en el alojamiento','Clase de cocina',
            'Cafés de té y café de montaña','Puestos de la carretera 1096','Roti de la calle',
            'Puestos de roti de la carretera','Ojo: isla musulmana']

previas = {}
if os.path.exists('sitios.js'):
    for s in json.loads(open('sitios.js').read()[13:-2]):
        previas[s['n']] = (s['la'], s['lo'], s['ap'])

out, nuevos = [], []
for sid, nombre_etapa, lista in ETAPAS:
    for s in lista:
        n, sello, zona, consulta = s[0], s[1], s[2], s[7]
        if n in NO_SITIO: continue
        if n in previas:
            la, lo, ap = previas[n]
        elif consulta.startswith('@'):
            la, lo = map(float, consulta[1:].split(',')); ap = 0
        else:
            la, lo = ZONAS[sid]; ap = 1; nuevos.append(n)
        out.append({'n': n, 'z': zona, 'e': nombre_etapa, 's': sello,
                    'la': la, 'lo': lo, 'ap': ap, 'q': quote(consulta.lstrip('@'))})

open('sitios.js','w').write('const SITIOS=' + json.dumps(out, ensure_ascii=False, separators=(',',':')) + ';\n')
print(f'sitios.js regenerado: {len(out)} sitios')
if nuevos: print('  sin coordenadas precisas (usan el centro de su zona):', nuevos)
fuera = sorted(set(previas) - {x['n'] for x in out})
if fuera: print('  eliminados:', fuera)
