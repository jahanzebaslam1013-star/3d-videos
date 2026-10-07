#!/usr/bin/env bash
# Hegemon Shorts project setup:  bash <skill>/kit/setup.sh <project-dir>
set -e; KIT="$(cd "$(dirname "$0")" && pwd)"; P="${1:?project dir}"; mkdir -p "$P/fonts" && cd "$P"
cp "$KIT"/{engine.js,lib.js,index.html,render.py,align.py,tighten.py,captions.py,sfxlib.py,mix.py,sheet.py,srt.py,thumbnail.py,M900.ttf} .
cp "$KIT/ZkitCaption.ttf" fonts/
[ -f package.json ] || npm init -y >/dev/null
[ -d node_modules/three ] || npm i three @fontsource/montserrat >/dev/null 2>&1
python3 -c "import numpy,scipy,playwright,PIL,soundfile,fontTools" 2>/dev/null || pip install --break-system-packages -q numpy scipy playwright pillow soundfile fonttools brotli
printf 'node_modules/\nchunks/\ntest/\nrender.log\n*.part.mp4\nvideo.mp4\n' > .gitignore
echo "ready: $P"
