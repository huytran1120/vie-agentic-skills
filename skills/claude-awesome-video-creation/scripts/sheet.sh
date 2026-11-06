#!/usr/bin/env bash
# Contact sheet of a video at given times: sheet.sh film.mp4 out.png 3 "2.5 11 18.5 31 43 53"
set -euo pipefail
if [[ "${1:-}" == "--help" || $# -lt 4 ]]; then sed -n 2p "$0"; exit 0; fi
v=$1; out=$2; cols=$3; times=$4; tmp=$(mktemp -d); n=0
for t in $times; do ffmpeg -y -v error -ss "$t" -i "$v" -frames:v 1 -vf scale=640:-1 "$tmp/$n.png"; n=$((n+1)); done
inputs=""; for ((i=0;i<n;i++)); do inputs="$inputs -i $tmp/$i.png"; done
rows=$(( (n + cols - 1) / cols ))
ffmpeg -y -v error $inputs -filter_complex "xstack=inputs=$n:grid=${cols}x${rows}" "$out"
echo "$out"
