#!/usr/bin/env python3
"""Genera catalogo.js a partir de los MP3 existentes. Ejecutar tras generar.sh."""
import os, json, glob
from mutagen.mp3 import MP3

# slug -> (titulo, seccion de la web, tipo)
#   tipo: 'capsula' (corto, delante del sitio) | 'guia' (largo) | 'fondo' (contexto)
META = {
 '00-tailandia-historia':  ('Tailandia en 12 minutos: de Sukhothai a hoy', 'avion', 'fondo'),
 '00-leer-un-templo':      ('Cómo leer un templo budista', 'avion', 'fondo'),
 '00-monarquia':           ('La monarquía: por qué está en todas partes', 'avion', 'fondo'),
 '00-comida':              ('La comida: el chile llegó de América', 'avion', 'fondo'),
 '00-casitas-espiritus':   ('Las casitas de espíritus', 'avion', 'fondo'),
 '01-bangkok-historia':    ('Historia de Bangkok', 'bangkok1-1', 'fondo'),
 '01-gran-palacio-capsula':('Gran Palacio y Wat Phra Kaew', 'bangkok1-2', 'capsula'),
 '01-gran-palacio-guia':   ('Gran Palacio y Wat Phra Kaew', 'bangkok1-2', 'guia'),
 '01-wat-pho-capsula':     ('Wat Pho, el Buda reclinado', 'bangkok1-2', 'capsula'),
 '01-wat-pho-guia':        ('Wat Pho, el Buda reclinado', 'bangkok1-2', 'guia'),
 '01-wat-arun-capsula':    ('Wat Arun, el templo del amanecer', 'bangkok1-2', 'capsula'),
 '01-wat-arun-guia':       ('Wat Arun, el templo del amanecer', 'bangkok1-2', 'guia'),
 '01-yaowarat-capsula':    ('Yaowarat, el barrio chino', 'bangkok1-2', 'capsula'),
 '01-yaowarat-guia':       ('Yaowarat, el barrio chino', 'bangkok1-2', 'guia'),
 '01-chao-phraya':         ('El río Chao Phraya', 'bangkok1-3', 'fondo'),
 '02-lanna-el-norte':      ('Lanna: el reino que fue otro país', 'bangkok1-4', 'fondo'),
 '02-chiang-rai-historia': ('Historia de Chiang Rai', 'chiangrai-1', 'fondo'),
 '02-templo-blanco-capsula':('Wat Rong Khun, el Templo Blanco', 'chiangrai-2', 'capsula'),
 '02-templo-blanco-guia':  ('Wat Rong Khun, el Templo Blanco', 'chiangrai-2', 'guia'),
 '02-templo-azul-capsula': ('Wat Rong Suea Ten, el Templo Azul', 'chiangrai-2', 'capsula'),
 '02-casa-negra-capsula':  ('Baan Dam, la Casa Negra', 'chiangrai-2', 'capsula'),
 '02-triangulo-de-oro':    ('El Triángulo de Oro y el opio', 'chiangrai-3', 'fondo'),
 '03-chiang-dao-historia': ('Chiang Dao: la montaña y la cueva', 'chiangdao-1', 'fondo'),
 '03-tribus-montana':      ('Las tribus de la montaña', 'chiangdao-2', 'fondo'),
 '04-chiang-mai-historia': ('Historia de Chiang Mai', 'chiangmai-1', 'fondo'),
 '04-doi-suthep-capsula':  ('Doi Suthep, el templo de la montaña', 'chiangmai-2', 'capsula'),
 '04-doi-suthep-guia':     ('Doi Suthep, el templo de la montaña', 'chiangmai-2', 'guia'),
 '04-wat-phra-singh-capsula':('Wat Phra Singh', 'chiangmai-1', 'capsula'),
 '04-wat-chedi-luang-capsula':('Wat Chedi Luang', 'chiangmai-1', 'capsula'),
 '04-elefantes':           ('El elefante en Tailandia', 'chiangmai-4', 'fondo'),
 '05-krabi-historia':      ('Krabi y el mar de Andamán', 'krabi-1', 'fondo'),
 '05-tsunami-2004':        ('El tsunami de 2004', 'krabi-1', 'fondo'),
 '06-koh-yao-noi-historia':('Koh Yao Noi: la isla que no se vendió', 'kohyaonoi-1', 'fondo'),
 '07-koh-lanta-historia':  ('Historia de Koh Lanta', 'kohlanta-1', 'fondo'),
 '07-chao-ley-gitanos-del-mar':('Los chao ley, gitanos del mar', 'kohlanta-4', 'fondo'),
 '07-koh-rok-capsula':     ('Koh Rok', 'kohlanta-3', 'capsula'),
 '08-jim-thompson':        ('Jim Thompson: la seda y la desaparición', 'bangkok2-2', 'fondo'),
 '00-masaje-tailandes':    ('El masaje tailandés', 'bangkok2-2', 'fondo'),
 '01-wat-traimit-capsula': ('Wat Traimit, el Buda de oro', 'bangkok1-2', 'capsula'),
 '04-mercados-chiang-mai': ('Los mercados de Chiang Mai', 'chiangmai-3', 'fondo'),
 '05-railay-capsula':      ('Railay', 'krabi-1', 'capsula'),
 '05-phang-nga-capsula':   ('La bahía de Phang Nga', 'kohyaonoi-3', 'capsula'),
 '07-playas-koh-lanta':    ('Las playas, una por una', 'kohlanta-2', 'fondo'),
}

pistas = []
for slug, (titulo, sec, tipo) in META.items():
    f = slug + '.mp3'
    if not os.path.exists(f):
        print('  FALTA:', f); continue
    a = MP3(f)
    pistas.append({'id': slug, 't': titulo, 's': sec, 'k': tipo,
                   'd': int(a.info.length), 'mb': round(os.path.getsize(f)/1048576, 1)})

js = 'const AUDIOS=' + json.dumps(pistas, ensure_ascii=False, separators=(',', ':')) + ';\n'
open('catalogo.js', 'w').write(js)
tot = sum(p['d'] for p in pistas); peso = sum(p['mb'] for p in pistas)
print(f"{len(pistas)} pistas · {tot//3600}h {(tot%3600)//60}min · {peso:.0f} MB")
