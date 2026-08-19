# Audioguía

37 pistas locutadas con edge-tts (voz es-ES-AlvaroNeural).

- `guiones/*.txt` — el texto de cada audio. Es la fuente: se edita aquí.
- `generar.sh` — regenera los MP3 cuyo guion se haya tocado. Necesita el entorno
  `~/.local/venvs/tts` (`python3 -m venv --without-pip`, get-pip y `pip install edge-tts mutagen`).
- `catalogo.py` — reconstruye `catalogo.js` (títulos, duración y peso) leyendo los MP3.
  Ejecutar siempre después de `generar.sh`.

Para añadir una pista: escribir el guion en `guiones/`, añadir su entrada al
diccionario `META` de `catalogo.py`, y ejecutar `./generar.sh && python3 catalogo.py`.

Los nombres tailandeses van transcritos fonéticamente en los guiones
("Uat Pra Keo" en vez de "Wat Phra Kaew") para que la voz española los pronuncie bien.
