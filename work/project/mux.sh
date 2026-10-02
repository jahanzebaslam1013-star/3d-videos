#!/bin/bash
# usage: mux.sh N   (secN/video.mp4 or s1/video.mp4 + mix_secN.wav -> ../Dunki_SectionN.mp4)
n=$1; v=sec$n/video.mp4; [ $n = 1 ] && v=s1/video.mp4
ffmpeg -loglevel error -y -i mix_sec$n.wav -af loudnorm=I=-15:TP=-1.5:LRA=11 -ar 48000 mix_sec${n}_ln.wav
ffmpeg -loglevel error -y -i $v -i mix_sec${n}_ln.wav -c:v libx264 -preset medium -crf 22 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -shortest ../Dunki_Section$n.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 ../Dunki_Section$n.mp4
