#!/usr/bin/env bash
# Render a Remotion film in segments, so one heavy scene can use fewer browser tabs.
# Usage: render_segments.sh <CompositionId> <out.mp4> "<from-to:concurrency> ..." [audio.wav]
#   e.g. render_segments.sh Film out/final.mp4 "0-4439:8 4440-4739:1 4740-6839:8" public/audio/soundtrack.wav
# Why: 8 headless-Chrome tabs rendering one deeply nested 3D/blur scene can deadlock the GPU process
# (the render stops progressing with no error). That scene alone at --concurrency=1 is fast.
# Prints RENDER_SECONDS=<wall clock> so an on-screen "render time" can show the measured number.
set -euo pipefail
if [[ "${1:-}" == "--help" || $# -lt 3 ]]; then sed -n 2,8p "$0"; exit 0; fi
comp=$1; out=$2; segs=$3; audio=${4:-}
tmp=$(mktemp -d); list="$tmp/segs.txt"; : > "$list"
start=$(date +%s); i=0
for seg in $segs; do
  range=${seg%%:*}; conc=${seg##*:}; part="$tmp/seg_$i.mp4"
  perl -e 'alarm 1800; exec @ARGV' npx remotion render "$comp" "$part" --frames="$range" --concurrency="$conc" --muted --crf=16 --log=error
  pkill -f chrome-headless-shell || true
  echo "file '$part'" >> "$list"; i=$((i+1))
done
echo "RENDER_SECONDS=$(( $(date +%s) - start ))"
if [[ -n "$audio" ]]; then
  ffmpeg -y -loglevel error -f concat -safe 0 -i "$list" -c copy "$tmp/picture.mp4"
  ffmpeg -y -loglevel error -i "$tmp/picture.mp4" -i "$audio" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart "$out"
else
  ffmpeg -y -loglevel error -f concat -safe 0 -i "$list" -c copy "$out"
fi
ffprobe -v error -count_packets -show_entries stream=nb_read_packets -show_entries format=duration -of compact "$out"
