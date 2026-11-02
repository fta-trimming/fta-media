import subprocess,sys,json,os
cfg=json.load(open(sys.argv[1]));src=cfg['src'];out=cfg['out'];tag=out[:-4]
R=lambda a:subprocess.run(['ffmpeg','-v','error','-y']+a,check=True)
enc=['-an','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p','-r','30']
SC='scale=1080:1920:flags=lanczos,setsar=1'
files=[];t=0;labels=[]
for i,s in enumerate(cfg['segs']):
  f=f'{tag}_s{i}.mp4'
  if s['type']=='still':
    R(['-ss',str(s['at']),'-i',src,'-frames:v','1','-vf',SC,'st.png'])
    d=s['dur'];R(['-loop','1','-t',str(d+0.3),'-i','st.png','-vf',f"scale=1145:-2,crop=1080:1920,zoompan=z='1+0.03*on/{int(d*30)}':d=1:s=1080x1920:fps=30,setsar=1"]+enc+['-t',str(d),f])
  else:
    sp=s['speed'];d=(s['b']-s['a'])/sp
    N=max(int(d*30),1);mv=s.get('move',['in','right','left','out'][i%4]);Z=1.08
    zz={'in':f"1+{Z-1}*on/{N}",'out':f"{Z}-{Z-1}*on/{N}"}.get(mv,str(Z))
    xx={'right':f"(iw-iw/zoom)*on/{N}",'left':f"(iw-iw/zoom)*(1-on/{N})"}.get(mv,"iw/2-iw/zoom/2")
    R(['-ss',str(s['a']),'-t',str(s['b']-s['a']),'-i',src,'-vf',f"scale=2160:3840:flags=lanczos,setsar=1,setpts=PTS/{sp},fps=30,zoompan=z='{zz}':x='{xx}':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30,setsar=1,fade=t=in:st=0:d=0.12,fade=t=out:st={d-0.12:.2f}:d=0.12"]+enc+[f])
  d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
  if s.get('label'): labels.append((s['label'],t,t+d))
  files.append(f);t+=d
sp=cfg['split'];d=sp['dur']
R(['-ss',str(sp['before']),'-i',src,'-frames:v','1','b.png']);R(['-ss',str(sp['after']),'-i',src,'-frames:v','1','a.png'])
f=f'{tag}_split.mp4'
# same source, same scale, side by side full frames (no crop -> no misalignment)
R(['-loop','1','-t',str(d),'-i','b.png','-loop','1','-t',str(d),'-i','a.png','-filter_complex',
 f"[0:v]crop={sp.get('bc','iw:ih:0:0')},scale=536:952,pad=540:952:0:0:color=0x111111[x];[1:v]crop={sp.get('ac','iw:ih:0:0')},scale=536:952,pad=540:952:4:0:color=0x111111[y];[x][y]hstack,pad=1080:1920:0:500:color=0x111111,fade=t=in:st=0:d=0.2,fade=t=out:st={d-0.4}:d=0.4,setsar=1"]+enc+[f])
labels.append(('l_split2.png',t,t+d));files.append(f);t+=d
open(f'{tag}_list.txt','w').write(''.join(f"file '{x}'\n" for x in files))
R(['-f','concat','-safe','0','-i',f'{tag}_list.txt','-c','copy',f'{tag}_cat.mp4'])
inp=['-i',f'{tag}_cat.mp4'];fc=['[0:v]eq=contrast=1.07:saturation=1.08,vignette=PI/5[b0]'];cur='b0'
for k,(png,s0,s1) in enumerate(labels):
  inp+=['-loop','1','-t',f'{t:.2f}','-i',png]
  fc.append(f"[{k+1}:v]format=rgba,fade=t=in:st={s0:.2f}:d=0.25:alpha=1,fade=t=out:st={s1-0.25:.2f}:d=0.25:alpha=1[l{k}]")
  fc.append(f"[{cur}][l{k}]overlay=0:0:enable='between(t,{s0:.2f},{s1:.2f})'[o{k}]");cur=f'o{k}'
fc.append(f'[{cur}]format=yuv420p[out]')
R(inp+['-filter_complex',';'.join(fc),'-map','[out]','-an','-c:v','libx264','-b:v','4500k','-maxrate','6000k','-bufsize','9000k','-preset','medium','-movflags','+faststart','-t',f'{t:.2f}',out])
print(out,round(t,2),os.path.getsize(out))
