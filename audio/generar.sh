#!/bin/bash
# Genera los MP3 de la audioguía a partir de los guiones de texto.
# Solo regenera los que faltan o cuyo guion se ha tocado después del MP3.
# Escribe primero en un temporal, así una interrupción nunca deja un MP3 a medias.
TTS=~/.local/venvs/tts/bin/edge-tts
VOZ=es-ES-AlvaroNeural
cd "$(dirname "$0")" || exit 1
n=0
for g in guiones/*.txt; do
  slug=$(basename "$g" .txt)
  mp3="$slug.mp3"
  if [ ! -f "$mp3" ] || [ "$g" -nt "$mp3" ]; then
    printf '%-38s' "$slug"
    if $TTS --voice "$VOZ" --rate=-5% --file "$g" --write-media "$mp3.tmp" 2>/dev/null && [ -s "$mp3.tmp" ]; then
      mv "$mp3.tmp" "$mp3"; echo "OK  $(du -h "$mp3" | cut -f1)"; n=$((n+1))
    else
      rm -f "$mp3.tmp"; echo "ERROR"
    fi
  fi
done
echo "--- $n audios generados ---"
