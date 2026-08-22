# Viaje a Tailandia · 2026

Salida de Madrid el **29 oct**, en Tailandia del **30 oct al 20 nov** (21 noches).
Ruta e itinerario con calma: Bangkok · norte · islas del Andamán.

👉 **Ver la web:** https://iaadileli.github.io/viaje-tailandia-2026/

Mapa de la ruta, día a día con fotos, qué comer en cada sitio, barrios y hoteles, y presupuesto orientativo.

## Cómo se toca esto

Los sitios de comer **no se editan a mano en el HTML**: viven en `generador/datos1.py`,
`datos2.py` y `datos3.py` (una tupla por sitio). Tras cambiarlos, y en este orden:

```bash
python3 generador/generar.py    # reescribe las fichas dentro de index.html
python3 actualizar-sitios.py    # regenera sitios.js (el «¿qué tengo cerca?»)
python3 generador/kml.py        # regenera el KML de Google My Maps
python3 hacer-copia.py          # regenera tailandia-sin-conexion.html
```

Un sitio nuevo sale sin coordenadas y `actualizar-sitios.py` avisa: usará el centro de su
zona hasta que se le pongan a mano en `sitios.js`.

El ZIP del Escritorio se actualiza aparte, sustituyendo dentro el HTML sin conexión:

```bash
zip -u ~/Escritorio/tailandia-2026-sin-conexion.zip tailandia-2026/index.html
```

En `generador/` está además lo que da contenido a la web y no se puede rehacer de memoria:
`frases.py` (las frases en tailandés con su fonética, de donde salen los MP3 con `genfrases.sh`),
`madrugador.py` (el plan de madrugador de cada día), `geocodifica.py` (coordenadas verificadas),
`buscafotos.py` (búsqueda de fotos en Wikimedia) y `datos-fuente/` con los volcados de Michelin,
las fichas de fotos y los sitios geocodificados.

_Fotos: Wikimedia Commons (dominio público / CC)._
