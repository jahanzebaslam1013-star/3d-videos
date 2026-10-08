#!/usr/bin/env bash
# Usage: bash setup.sh <project_dir>   — copies the kit, installs three.js + Montserrat, builds the caption font.
set -e; K="$(cd "$(dirname "$0")" && pwd)"; P="$1"; mkdir -p "$P"; cd "$P"
cp "$K"/{engine.js,index.html,render.py,captions.py,sfxlib.py,mix.py,sheet.py,trim_voice.py,build_timing.py} .
[ -f package.json ] || npm init -y >/dev/null
[ -d node_modules/three ] || npm i three @fontsource/montserrat >/dev/null 2>&1
pip install --break-system-packages -q numpy scipy playwright fonttools brotli pillow soundfile >/dev/null 2>&1 || true
mkdir -p fonts && python3 - <<'PY'
from fontTools.ttLib import TTFont
f=TTFont('node_modules/@fontsource/montserrat/files/montserrat-latin-800-normal.woff2');f.flavor=None
for r in f['name'].names:
    if r.nameID in (1,4,16): r.string='ZkitCaption'
    if r.nameID==6: r.string='ZkitCaption-Regular'
    if r.nameID in (2,17): r.string='Regular'
f.save('fonts/ZkitCaption.ttf')
PY
printf 'node_modules/\nfonts/\nchunks/\ntest/\n*.log\n' > .gitignore
echo "ready: $P"
