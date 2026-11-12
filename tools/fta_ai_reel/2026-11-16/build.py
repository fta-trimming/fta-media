# 使い方: python3 build.py <dir>  → voice.wav・timing.json・r.html を作る
import sys,json,subprocess,os
d=sys.argv[1]
def dur(f): return float(subprocess.check_output(['ffprobe','-v','0','-show_entries','format=duration','-of','csv=p=0',f]))
sc=[];t=0;ins=[];flt=[]
for i in range(7):
    x=dur(f'{d}/v{i+1}.wav'); sc.append([round(t,3),round(t+x+0.75,3)])
    ms=int(round((t+0.3)*1000)); ins+=['-i',f'{d}/v{i+1}.wav']; flt.append(f'[{i}:a]aresample=48000,adelay={ms}|{ms}[a{i}]'); t+=x+0.75
# 最後の場面の文字が出たあと少し余韻
sc[-1][1]=round(sc[-1][1]+0.6,3)
fc=';'.join(flt)+';'+''.join(f'[a{i}]' for i in range(7))+f'amix=inputs=7:normalize=0,apad,atrim=0:{sc[-1][1]}[out]'
subprocess.check_call(['ffmpeg','-y','-v','error']+ins+['-filter_complex',fc,'-map','[out]','-ac','2','-ar','48000',f'{d}/voice.wav'])
json.dump({'scenes':sc},open(f'{d}/timing.json','w'))
h=open('head.html').read()+open(f'{d}/body.html').read()+open('foot.html').read()
open(f'{d}/r.html','w').write(h.replace('__TIMING__',json.dumps({'scenes':sc})))
print(d,sc)
