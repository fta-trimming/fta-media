# カット中心の座学リール（こげ茶の地・上に題・まん中に正方形の映像か図・下に大きな文字）を作る
# 使い方: python3 build_zagaku.py 設定.json
import json, os, sys, subprocess, tempfile, shutil
cfg = json.load(open(sys.argv[1])); W, H = 1080, 1920; MY = 330
TTS = '/home/claude/fta-media/tools/voicevox/tts_voices.py'
tmp = tempfile.mkdtemp(prefix='zg_'); out = cfg['out']
def run(a): subprocess.run(a, check=True)
def dur(f): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)
CSS = """*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1920px;background:transparent;font-family:'Noto Sans CJK JP',sans-serif;overflow:hidden}
.bg{position:absolute;inset:0;background:#1c1512}.hole{position:absolute;left:0;top:330px;width:1080px;height:1080px;box-shadow:0 0 0 2000px #1c1512}
.t{position:absolute;top:250px;left:0;right:0;text-align:center;color:#e9c46a;font-size:36px;font-weight:700;letter-spacing:.04em}
.cap{position:absolute;top:1470px;left:40px;right:40px;text-align:center;color:#fff;font-size:84px;font-weight:900;line-height:1.3}
.cap .y{color:#f2c14e}.ill{position:absolute;left:60px;top:390px;width:960px;height:960px;border-radius:28px;background:#f7efe2;display:flex;align-items:center;justify-content:center;overflow:hidden}
.ill svg{width:900px;height:900px}.badge{position:absolute;top:1360px;right:40px;background:#fff;color:#1c1512;font-size:30px;font-weight:900;padding:4px 18px;border-radius:999px}
.br{position:absolute;bottom:120px;left:0;right:0;text-align:center;color:#a8957f;font-size:30px}"""
segs = []
for i, s in enumerate(cfg['scenes']):
    wav = os.path.join(tmp, f'v{i}.wav')
    run(['python3', TTS, s['voice'], wav, str(cfg.get('speed', 1.15)), cfg.get('voiceName', 'aoyama')])
    d = max(s.get('min', 3.5), dur(wav) + s.get('pad', 0.6))
    if s['kind'] == 'video':
        mid = "<div class='hole'></div>" + (f"<div class='badge'>{s['badge']}</div>" if s.get('badge') else '')
    else:
        mid = f"<div class='bg'></div><div class='ill'>{s['illus']}</div>"
    html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{mid}<div class='t'>{cfg['title']}</div><div class='cap'>{s['cap']}</div><div class='br'>{cfg.get('brand','')}</div></body></html>"
    hp = os.path.join(tmp, f'o{i}.html'); open(hp, 'w').write(html)
    png = os.path.join(tmp, f'o{i}.png')
    js = f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1080,height:1920}}}});await p.goto('file://{hp}');await p.waitForTimeout(200);await p.screenshot({{path:'{png}',omitBackground:true}});await b.close()}})();"
    jp = os.path.join(tmp, 'o.js'); open(jp, 'w').write(js); run(['node', jp])
    seg = os.path.join(tmp, f's{i}.mp4'); fd = 0.25
    if s['kind'] == 'video':
        sp = s.get('speed', 1.0); cy = s.get('cy', 420)
        vf = (f"[0:v]trim=start={s['start']}:duration={d*sp:.3f},setpts=(PTS-STARTPTS)/{sp},crop=1080:1080:0:{cy},"
              f"pad=1080:1920:0:{MY}:color=0x1c1512,fps=30[v];[v][1:v]overlay=0:0,fade=in:0:{int(fd*30)},fade=out:st={d-fd:.3f}:d={fd}[o]")
        run(['ffmpeg', '-v', 'error', '-y', '-i', s['file'], '-loop', '1', '-i', png, '-i', wav, '-filter_complex', vf + f";[2:a]apad,atrim=0:{d:.3f}[a]",
             '-map', '[o]', '-map', '[a]', '-t', f'{d:.3f}', '-c:v', 'libx264', '-qp', '0', '-preset', 'ultrafast', '-pix_fmt', 'yuv444p', '-c:a', 'pcm_s16le', '-ar', '44100', seg])
    else:
        vf = f"[0:v]fps=30,fade=in:0:{int(fd*30)},fade=out:st={d-fd:.3f}:d={fd}[o]"
        run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-i', png, '-i', wav, '-filter_complex', vf + f";[1:a]apad,atrim=0:{d:.3f}[a]",
             '-map', '[o]', '-map', '[a]', '-t', f'{d:.3f}', '-c:v', 'libx264', '-qp', '0', '-preset', 'ultrafast', '-pix_fmt', 'yuv444p', '-c:a', 'pcm_s16le', '-ar', '44100', seg])
    segs.append(seg); print('scene', i, round(d, 2), flush=True)
lst = os.path.join(tmp, 'l.txt'); open(lst, 'w').write(''.join(f"file '{x}'\n" for x in segs))
run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c:v', 'libx264', '-crf', '14', '-preset', 'slow', '-profile:v', 'high', '-tune', 'film', '-x264-params', 'keyint=60', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out])
shutil.rmtree(tmp); print('done', out, round(dur(out), 2))
