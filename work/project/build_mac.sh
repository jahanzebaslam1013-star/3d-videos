#!/bin/bash
# DUNKI — full-quality build on the Mac.
# Renders all 4 sections from the code, adds the finished audio (audio/secN.m4a),
# and joins them into ../Dunki_FULL_1080p.mp4  (1920x1080, 24 fps).
#
#   cd "<this folder>"   then   bash build_mac.sh
#
# Safe to stop and re-run: finished chunks are kept and skipped.
set -e
cd "$(dirname "$0")"
JOBS=${JOBS:-$(sysctl -n hw.ncpu 2>/dev/null || nproc)}
[ "$JOBS" -gt 8 ] && JOBS=8
LIMIT=${LIMIT:-0}            # test mode: LIMIT=48 renders only 48 frames per section

echo "== 1/4 checking tools"
command -v ffmpeg >/dev/null || { echo "ffmpeg missing ->  brew install ffmpeg"; exit 1; }
python3 -c "import cairo, PIL, numpy" 2>/dev/null || {
  echo "python packages missing ->  brew install cairo pkg-config  &&  pip3 install pycairo pillow numpy"; exit 1; }

echo "== 2/4 installing fonts"
mkdir -p ~/Library/Fonts ~/.fonts
cp fonts/*.ttf ~/Library/Fonts/ 2>/dev/null || true
cp fonts/*.ttf ~/.fonts/
command -v fc-cache >/dev/null && fc-cache -f >/dev/null 2>&1 || true

echo "== 3/4 rendering ($JOBS parallel jobs per section)"
for n in 1 2 3 4; do
  m=sec$n; d=build/$m; mkdir -p $d
  NF=$(python3 -c "import $m; print(int($m.END*24))" | tail -1)
  [ "$LIMIT" -gt 0 ] && NF=$LIMIT
  K=$(( (NF + JOBS - 1) / JOBS ))
  echo "   section $n: $NF frames"
  : > $d/list.txt
  for ((i=0; i<JOBS; i++)); do
    a=$((i*K)); b=$(((i+1)*K)); [ $b -gt $NF ] && b=$NF; [ $a -ge $NF ] && break
    f=$d/c$(printf %02d $i)_${a}_${b}.mp4
    echo "file '$(basename $f)'" >> $d/list.txt
    if [ -s $f ] && ffprobe -v error $f >/dev/null 2>&1; then continue; fi
    python3 $m.py --range $a $b $f &
  done
  wait
  ffmpeg -loglevel error -y -f concat -safe 0 -i $d/list.txt -c copy $d/video.mp4
  ffmpeg -loglevel error -y -i $d/video.mp4 -i audio/sec$n.m4a -map 0:v -map 1:a -c:v copy -c:a copy -shortest \
         -movflags +faststart build/Dunki_Section$n.mp4
  echo "   section $n done: $(ffprobe -v error -show_entries format=duration -of csv=p=0 build/Dunki_Section$n.mp4) s"
done

echo "== 4/4 joining"
printf "file 'Dunki_Section1.mp4'\nfile 'Dunki_Section2.mp4'\nfile 'Dunki_Section3.mp4'\nfile 'Dunki_Section4.mp4'\n" > build/full.txt
ffmpeg -loglevel error -y -f concat -safe 0 -i build/full.txt -c copy -movflags +faststart ../Dunki_FULL_1080p.mp4
echo "DONE -> $(cd ..; pwd)/Dunki_FULL_1080p.mp4  ($(ffprobe -v error -show_entries format=duration -of csv=p=0 ../Dunki_FULL_1080p.mp4) s)"
echo "Sections are also in build/ (Dunki_Section1..4.mp4)."
