import subprocess,sys,json,os
cfg=json.load(open(sys.argv[1]));src=cfg['src'];out=cfg['out'];tag=out[:-4]
R=lambda a:subprocess.run(['ffmpeg','-v','error','-y']+a,check=True)
enc=['-an','-c:v','libx264','-qp','0','-preset','ultrafast','-pix_fmt','yuv420p','-r','30']  # 11/9 途中は劣化なし
W,H=cfg.get('W',1080),cfg.get('H',1920)  # 11/9 元が720×1280なら W:720,H:1280 で元の大きさのまま作る
k=W/1080
SC=f'scale={W}:{H}:flags=lanczos,setsar=1'
files=[];t=0;labels=[]
for i,s in enumerate(cfg['segs']):
  f=f'{tag}_s{i}.mp4'
  if s['type']=='still':
    R(['-ss',str(s['at']),'-i',src,'-frames:v','1','-vf',SC,'st.png'])
    d=s['dur'];R(['-loop','1','-t',str(d+0.3),'-i','st.png','-vf',f"scale={round(W*1.06/2)*2}:-2,crop={W}:{H},zoompan=z='1+0.03*on/{int(d*30)}':d=1:s={W}x{H}:fps=30,setsar=1"]+enc+['-t',str(d),f])
  else:
    sp=s['speed'];d=(s['b']-s['a'])/sp
    N=max(int(d*30),1);mv=s.get('move',['in','right','left','out'][i%4]);Z=1.08
    zz={'in':f"1+{Z-1}*on/{N}",'out':f"{Z}-{Z-1}*on/{N}"}.get(mv,str(Z))
    xx={'right':f"(iw-iw/zoom)*on/{N}",'left':f"(iw-iw/zoom)*(1-on/{N})"}.get(mv,"iw/2-iw/zoom/2")
    R(['-ss',str(s['a']),'-t',str(s['b']-s['a']),'-i',src,'-vf',f"scale={2*W}:{2*H}:flags=lanczos,setsar=1,setpts=PTS/{sp},fps=30,zoompan=z='{zz}':x='{xx}':y='ih/2-ih/zoom/2':d=1:s={W}x{H}:fps=30,setsar=1,fade=t=in:st=0:d=0.12,fade=t=out:st={d-0.12:.2f}:d=0.12"]+enc+[f])
  d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
  if s.get('label'): labels.append((s['label'],t,t+d))
  files.append(f);t+=d
sp=cfg['split'];d=sp['dur']
R(['-ss',str(sp['before']),'-i',src,'-frames:v','1','b.png']);R(['-ss',str(sp['after']),'-i',src,'-frames:v','1','a.png'])
f=f'{tag}_split.mp4'
# same source, same scale, side by side full frames (no crop -> no misalignment)
R(['-loop','1','-t',str(d),'-i','b.png','-loop','1','-t',str(d),'-i','a.png','-filter_complex',
 f"[0:v]crop={sp.get('bc','iw:ih:0:0')},scale={round(536*k/2)*2}:{round(952*k/2)*2},pad={round(540*k/2)*2}:{round(952*k/2)*2}:0:0:color=0x111111[x];[1:v]crop={sp.get('ac','iw:ih:0:0')},scale={round(536*k/2)*2}:{round(952*k/2)*2},pad={round(540*k/2)*2}:{round(952*k/2)*2}:{round(4*k)}:0:color=0x111111[y];[x][y]hstack,pad={W}:{H}:0:{round(500*k)}:color=0x111111,fade=t=in:st=0:d=0.2,fade=t=out:st={d-0.4}:d=0.4,setsar=1"]+enc+[f])
labels.append(('l_split2.png',t,t+d));files.append(f);t+=d
open(f'{tag}_list.txt','w').write(''.join(f"file '{x}'\n" for x in files))
R(['-f','concat','-safe','0','-i',f'{tag}_list.txt','-c','copy',f'{tag}_cat.mp4'])
inp=['-i',f'{tag}_cat.mp4'];fc=['[0:v]eq=contrast=1.07:saturation=1.08,vignette=PI/5[b0]'];cur='b0'
for j,(png,s0,s1) in enumerate(labels):
  k=j
  inp+=['-loop','1','-t',f'{t:.2f}','-i',png]
  fc.append(f"[{k+1}:v]scale={W}:{H}:flags=lanczos,format=rgba,fade=t=in:st={s0:.2f}:d=0.25:alpha=1,fade=t=out:st={s1-0.25:.2f}:d=0.25:alpha=1[l{k}]")
  fc.append(f"[{cur}][l{k}]overlay=0:0:enable='between(t,{s0:.2f},{s1:.2f})'[o{k}]");cur=f'o{k}'
fc.append(f'[{cur}]format=yuv420p[out]')
R(inp+['-filter_complex',';'.join(fc),'-map','[out]','-an','-c:v','libx264','-crf',str(cfg.get('crf',13 if W<1080 else 16)),'-preset','slow','-tune','film','-profile:v','high','-movflags','+faststart','-t',f'{t:.2f}',out])
print(out,round(t,2),os.path.getsize(out))
# 11/9 藤原さん「とにかく画質が下がらない方法で」：本番は上の1回だけの書き出し（crf 16）。
# 司令室（20MBまで）に入らないときだけ、見る用の軽い版 <out>_view.mp4 を別に作る（本番は GitHub に置く）。
if os.path.getsize(out) > 19*1024*1024:
  view=out[:-4]+'_view.mp4'
  R(['-i',out,'-an','-c:v','libx264','-crf','23','-preset','slow','-movflags','+faststart',view])
  print('view',view,os.path.getsize(view))
