import json, subprocess, time, re, sys
# coordenadas conocidas de los vídeos, que son exactas
CONOCIDAS = {
 'Jok Pa Mali':(13.7340327,100.5121937), 'Kway Teow Roo':(13.7325202,100.5138923),
 'Puesto de coco y khanom krok':(13.732135,100.513549), 'Lalai Sap Market':(13.7261255,100.5273154),
 'DK Bakery':(13.7244291,100.5226551), 'Heng Hoitod Chawlae':(13.7177061,100.5077839),
 'Noor':(13.7130476,100.5025891), 'ROTINI':(13.7252514,100.5124123),
 'Patongo con leche de soja':(13.717792,100.507797), 'Kluay tod':(13.713011,100.503128),
 'Tang Bak Seng':(13.7422789,100.5116176), 'Pa Lek-Pa Yai':(13.7424053,100.5116501),
 'Jai Rad Na Noodle':(13.7405203,100.5128622), 'Bok Kia Tha Din Daeng':(13.7328026,100.5031647),
 'Pork Satay Tee Tha Din Daeng':(13.7330978,100.502525), 'Amin Mutton & Chicken Biryani':(13.7204342,100.5050894),
 "Jack's Chicken Rice":(13.7475692,100.5007523), 'Somsak Pu Ob':(13.726908,100.4873205),
}
# centro de cada zona, como último recurso
ZONAS = {'bangkok1':(13.7460,100.5340),'chiangrai':(19.9105,99.8406),'chiangdao':(19.3667,98.9667),
         'chiangmai':(18.7883,98.9853),'krabi':(8.0863,98.9063),'kohjum':(7.7833,99.0500),
         'kohlanta':(7.6167,99.0333)}

def nominatim(q):
    cmd = ['curl','-s','--max-time','20','-H','User-Agent: guia-viaje-personal-adil','-G',
           'https://nominatim.openstreetmap.org/search',
           '--data-urlencode',f'q={q}','--data-urlencode','format=json','--data-urlencode','limit=1']
    try:
        r = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)
        if r: return float(r[0]['lat']), float(r[0]['lon'])
    except Exception: pass
    return None

sitios = json.load(open('sitios.json'))
out, stats = [], {'conocida':0,'nominatim':0,'zona':0}
for s in sitios:
    lat = lon = None; fuente = ''
    if s['consulta'].startswith('@'):
        lat, lon = map(float, s['consulta'][1:].split(',')); fuente='conocida'
    elif s['nombre'] in CONOCIDAS:
        lat, lon = CONOCIDAS[s['nombre']]; fuente='conocida'
    else:
        r = nominatim(s['consulta']); time.sleep(1.1)
        if r: lat, lon = r; fuente='nominatim'
        else: lat, lon = ZONAS[s['etapa']]; fuente='zona'
    stats[fuente] += 1
    out.append({**s, 'lat': round(lat,6), 'lon': round(lon,6), 'fuente': fuente})
    print(f"  {fuente[:4]:5s} {s['nombre'][:34]:36s} {lat:.4f},{lon:.4f}")
json.dump(out, open('sitios-geo.json','w'), ensure_ascii=False)
print('\n', stats)
