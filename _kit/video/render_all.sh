#!/bin/bash
for v in "$@"; do
  cd /home/claude/videos/$v && mkdir -p renders qa && timeout 900 npx --yes hyperframes@0.8.185 render --output renders/raw.mp4 > renders/render.log 2>&1
  # loudness: voice to -14 LUFS integrated, true peak -1.5
  ffmpeg -v error -y -i renders/raw.mp4 -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 192k renders/final.mp4
  ffmpeg -v error -y -i renders/final.mp4 -vf "fps=1,scale=216:-1,tile=14x2" -frames:v 1 qa/sheet.jpg
  echo "done $v $(ffprobe -v error -show_entries format=duration -of csv=p=0 renders/final.mp4)"
done
