#!/bin/bash
# VOICEVOX（四国めたん）を使えるようにする。毎回の作業の最初に1回だけ実行する。
# 使い方: bash tools/voicevox/setup.sh  → /tmp/vv に入る
set -e
V=/tmp/vv; mkdir -p $V; cd $V
[ -f done ] && exit 0
curl -sSLO https://github.com/VOICEVOX/voicevox_core/releases/download/0.16.2/voicevox_core-0.16.2-cp310-abi3-manylinux_2_34_x86_64.whl
curl -sSL https://github.com/VOICEVOX/onnxruntime-builder/releases/download/voicevox_onnxruntime-1.17.3/voicevox_onnxruntime-linux-x64-1.17.3.tgz | tar xz
curl -sSL https://github.com/r9y9/open_jtalk/releases/download/v1.11.1/open_jtalk_dic_utf_8-1.11.tar.gz | tar xz
curl -sSLO https://github.com/VOICEVOX/voicevox_vvm/releases/download/0.16.1/0.vvm
pip install --break-system-packages -q voicevox_core-0.16.2-*.whl
touch done
