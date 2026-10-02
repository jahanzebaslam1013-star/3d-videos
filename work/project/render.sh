#!/bin/bash
# usage: render.sh secN  -> secN_dir/video.mp4
m=$1; mkdir -p $m
NF=$(python3 -c "import $m; print(int($m.END*24))" 2>/dev/null | tail -1)
K=$(( (NF+3)/4 ))
for i in 0 1 2 3; do python3 $m.py --range $((i*K)) $(((i+1)*K)) $m/c$i.mp4 & done; wait
printf "file 'c0.mp4'\nfile 'c1.mp4'\nfile 'c2.mp4'\nfile 'c3.mp4'\n" > $m/list.txt
ffmpeg -loglevel error -y -f concat -safe 0 -i $m/list.txt -c copy $m/video.mp4
echo "$m frames=$NF dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $m/video.mp4)"
