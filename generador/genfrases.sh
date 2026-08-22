#!/bin/bash
# Genera un MP3 por frase con voz tailandesa nativa.
cd ~/Escritorio/viaje-tailandia/audio/frases || exit 1
TTS=~/.local/venvs/tts/bin/edge-tts
n=0
while IFS='|' read -r id texto; do
  [ -z "$id" ] && continue
  [ -f "$id.mp3" ] && continue
  T="$(mktemp)"; printf '%s' "$texto" > "$T"
  if $TTS --voice th-TH-NiwatNeural --rate=-15% --file "$T" --write-media "$id.mp3.tmp" 2>/dev/null && [ -s "$id.mp3.tmp" ]; then
    mv "$id.mp3.tmp" "$id.mp3"; n=$((n+1)); printf '%-14s OK\n' "$id"
  else
    rm -f "$id.mp3.tmp"; printf '%-14s ERROR\n' "$id"
  fi
  rm -f "$T"
done
echo "--- $n frases generadas ---"
