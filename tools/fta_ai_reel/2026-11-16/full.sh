#!/bin/bash
# bash full.sh <dir> : 全コマ書き出し→1回だけ本番エンコード→見る用→表紙
set -e; cd "$(dirname "$0")"; d=$1
rm -rf $d/fr; N=$(python3 -c "import json,math;print(math.ceil(json.load(open('$d/timing.json'))['scenes'][-1][1]*30))")
Q=$(( (N+3)/4 ))
for k in 0 1 2 3; do node render.js $d full $((k*Q)) $(((k+1)*Q)) & done; wait
ffmpeg -v error -y -framerate 30 -i $d/fr/%05d.png -i $d/voice.wav -c:v libx264 -preset slow -crf 16 -profile:v high -level 4.2 -tune film -pix_fmt yuv420p -x264-params keyint=60:min-keyint=30 -c:a aac -b:a 192k -shortest -movflags +faststart $d/hq.mp4
ffmpeg -v error -y -i $d/hq.mp4 -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart $d/view.mp4
cp $d/fr/00105.png $d/cover.png
python3 -c "from PIL import Image;Image.open('$d/cover.png').convert('RGB').save('$d/cover.jpg',quality=95)"
ls -la $d/hq.mp4 $d/view.mp4 $d/cover.jpg; echo DONE $d
