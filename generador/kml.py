# -*- coding: utf-8 -*-
"""Genera un KML con todos los sitios de comida, una capa por ciudad.
My Maps geolocaliza por la dirección del <address>, así que no hacen falta coordenadas."""
import sys, html
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datos1 import BANGKOK, CHIANGRAI
from datos2 import CHIANGDAO, CHIANGMAI
from datos3 import KRABI, KOHJUM, KOHLANTA

CAPAS = [
 ("Bangkok", BANGKOK, "Krung Thep Maha Nakhon, Bangkok, Tailandia"),
 ("Chiang Rai", CHIANGRAI, "Chiang Rai, Tailandia"),
 ("Chiang Dao", CHIANGDAO, "Chiang Dao, Chiang Mai, Tailandia"),
 ("Chiang Mai", CHIANGMAI, "Chiang Mai, Tailandia"),
 ("Krabi", KRABI, "Krabi, Tailandia"),
 ("Koh Jum", KOHJUM, "Ko Jum, Krabi, Tailandia"),
 ("Koh Lanta", KOHLANTA, "Ko Lanta, Krabi, Tailandia"),
]
ICONO = {'leyenda': 'ylw-stars', 'estrella': 'red-stars', 'bib': 'red-circle',
         'local': 'grn-circle', 'barato': 'blu-circle', 'cena': 'purple-stars', '': 'wht-blank'}
e = html.escape

out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<kml xmlns="http://www.opengis.net/kml/2.2"><Document>',
       '<name>Tailandia 2026 · dónde comer</name>',
       f'<description>{sum(len(x[1]) for x in CAPAS)} sitios de comida, una capa por etapa. '
       'Estrella: lleva décadas abierto · Cubiertos: Bib Gourmand · Punto: donde come la gente de aquí</description>']

for sello, icono in ICONO.items():
    out.append(f'<Style id="s_{sello or "normal"}"><IconStyle><Icon>'
               f'<href>http://maps.google.com/mapfiles/kml/paddle/{icono}.png</href></Icon></IconStyle></Style>')

for ciudad, sitios, sufijo in CAPAS:
    out.append(f'<Folder><name>{e(ciudad)}</name>')
    for sitio in sitios:
        nombre, sello, zona, que, pide, horario, precio, consulta = sitio[:8]
        desc = f"{que}\n\nPIDE: {pide}\n\nHorario: {horario}\nPrecio: {precio}\nZona: {zona}"
        out.append('<Placemark>')
        out.append(f'  <name>{e(nombre)}</name>')
        out.append(f'  <description><![CDATA[{html.escape(desc).replace(chr(10), "<br>")}]]></description>')
        out.append(f'  <address>{e(consulta)}, {e(sufijo)}</address>')
        out.append(f'  <styleUrl>#s_{sello or "normal"}</styleUrl>')
        out.append('</Placemark>')
    out.append('</Folder>')

out.append('</Document></kml>')
destino = '/home/adil/Escritorio/viaje-tailandia/tailandia-donde-comer.kml'
open(destino, 'w').write('\n'.join(out))
total = sum(len(s) for _, s, _ in CAPAS)
print(f'KML con {total} sitios en {len(CAPAS)} capas → {destino}')
