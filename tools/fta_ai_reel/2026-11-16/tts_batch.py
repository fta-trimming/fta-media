import sys,json,subprocess
from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile
V='/tmp/vv/'
ort=Onnxruntime.load_once(filename=V+'voicevox_onnxruntime-linux-x64-1.17.3/lib/libvoicevox_onnxruntime.so.1.17.3')
syn=Synthesizer(ort,OpenJtalk(V+'open_jtalk_dic_utf_8-1.11'))
with VoiceModelFile.open(V+'15.vvm') as m: syn.load_voice_model(m)
SID=13
for d in sys.argv[1:]:
  lines=[l.strip() for l in open(d+'/lines.txt') if l.strip()]
  for i,t in enumerate(lines):
    t=t.replace('毛','け').replace('施術','せじゅつ')  # 11/14 藤原さん：施術を「しじゅつ」と読ませない
    import re; t=re.sub(r'(しい|たい)方(は|へ|に|も)',r'\1かた\2',t)  # 11/14 藤原さん：「ほしい方」を「ほう」と読ませない
    q=syn.create_audio_query(t,SID); q.speed_scale=1.1
    kana=''.join(m.text for ph in q.accent_phrases for m in ph.moras)
    open(f'{d}/v{i+1}.wav','wb').write(syn.synthesis(q,SID))
    print(d[-4:],i+1,kana)
