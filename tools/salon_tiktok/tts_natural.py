import sys
from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile
V='/tmp/vv/'
ort=Onnxruntime.load_once(filename=V+'voicevox_onnxruntime-linux-x64-1.17.3/lib/libvoicevox_onnxruntime.so.1.17.3')
syn=Synthesizer(ort,OpenJtalk(V+'open_jtalk_dic_utf_8-1.11'))
with VoiceModelFile.open(V+'0.vvm') as m: syn.load_voice_model(m)
text,out=sys.argv[1],sys.argv[2]
text=text.replace('毛','け')  # 11/2 藤原さんの指示：毛は必ず「け」（今後も変えない）
q=syn.create_audio_query(text,2)
q.speed_scale=float(sys.argv[3]) if len(sys.argv)>3 else 1.0
q.intonation_scale=1.3      # 抑揚を大きく（棒読み感を減らす）
q.pitch_scale=-0.02
q.pre_phoneme_length=0.05; q.post_phoneme_length=0.08
open(out,'wb').write(syn.synthesis(q,2))
