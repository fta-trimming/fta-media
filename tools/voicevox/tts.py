# 四国めたん（ノーマル id 2）で文章を読み上げて WAV にする。
# 使い方: python3 tools/voicevox/tts.py "文章" out.wav [話す速さ 既定1.1]
# 動画・投稿文には必ず「VOICEVOX:四国めたん」とクレジットを入れる（利用規約）。
import sys
from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile
V = '/tmp/vv/'
ort = Onnxruntime.load_once(filename=V + 'voicevox_onnxruntime-linux-x64-1.17.3/lib/libvoicevox_onnxruntime.so.1.17.3')
syn = Synthesizer(ort, OpenJtalk(V + 'open_jtalk_dic_utf_8-1.11'))
with VoiceModelFile.open(V + '0.vvm') as m:
    syn.load_voice_model(m)
SID = 2  # 四国めたん ノーマル
text, out = sys.argv[1], sys.argv[2]
q = syn.create_audio_query(text, SID)
q.speed_scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.1
open(out, 'wb').write(syn.synthesis(q, SID))
