# VOICEVOX で文章を読み上げて WAV にする。
# 使い方: python3 tools/voicevox/tts.py "文章" out.wav [話す速さ 既定1.1] [声 metan|aoyama 既定metan]
#   metan  = 四国めたん（ノーマル id 2）… 技術系（ワンコを切る・バリカン・ハサミの作業を見せる回）
#   aoyama = 青山龍星（ノーマル id 13）… 座学系（道具・知識・選び方などの説明の回）
#   （10/28 藤原さんの指示「今後も技術系は四国で座学系は青山で」）
# 動画・投稿文には必ず使った声のクレジット（VOICEVOX:四国めたん / VOICEVOX:青山龍星）を入れる（利用規約）。
import sys
from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile
V = '/tmp/vv/'
VOICES = {'metan': ('0.vvm', 2), 'aoyama': ('15.vvm', 13)}
voice = sys.argv[4] if len(sys.argv) > 4 else 'metan'
vvm, SID = VOICES[voice]
ort = Onnxruntime.load_once(filename=V + 'voicevox_onnxruntime-linux-x64-1.17.3/lib/libvoicevox_onnxruntime.so.1.17.3')
syn = Synthesizer(ort, OpenJtalk(V + 'open_jtalk_dic_utf_8-1.11'))
with VoiceModelFile.open(V + vvm) as m:
    syn.load_voice_model(m)
text, out = sys.argv[1], sys.argv[2]
import re
text = re.sub(r'(しい|たい)方(は|へ|に|も)', r'\1かた\2', text)  # 11/14 藤原さんの指示：「ほしい方は」が「ほう」と読まれるので「かた」に（今後も変えない）
text = text.replace('施術', 'せじゅつ')  # 11/14 藤原さんの指示：施術が「しじゅつ」と読まれるので（今後も変えない）
text = text.replace('毛', 'け')  # 11/2 藤原さんの指示：毛は「もう」と読まれるので必ず「け」（今後も変えない）
q = syn.create_audio_query(text, SID)
q.speed_scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.1
open(out, 'wb').write(syn.synthesis(q, SID))
