#!/bin/bash
# 声の入った動画に自作のBGMを小さく入れる（映像は作り直さない＝画質そのまま）。
# 11/20 藤原さん「音が少し大きくて音声と被るのが気になる」→ 曲は声より約16dB小さく、声の間はさらに下げる。
# 使い方: bash mix_bgm.sh <入力.mp4> <dogs|spa> <出力.mp4> [seed]
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
IN="$1"; ST="$2"; OUT="$3"; SEED="${4:-1}"
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
TMP=$(mktemp -d)
python3 "$HERE/bgm.py" "$ST" "$D" "$TMP/bgm.wav" "$SEED"
ffmpeg -v error -y -i "$IN" -i "$TMP/bgm.wav" -filter_complex \
 "[0:a]aresample=48000,aformat=channel_layouts=stereo,asplit=2[v][sc];[1:a]highpass=f=90,volume=0.075[b];[b][sc]sidechaincompress=threshold=0.012:ratio=8:attack=25:release=600:makeup=1[bd];[v][bd]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart "$OUT"
rm -rf "$TMP"
echo "ok $OUT"
