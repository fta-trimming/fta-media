import subprocess, os, sys, json
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
SALON = sys.argv[1]
CFG = json.load(open(f'{SALON}.json'))
W, H = 1080, 1920
TTS = os.path.join(os.path.dirname(HERE), 'voicevox', 'tts.py')
OUT = f'out_{SALON}'
os.makedirs(OUT, exist_ok=True)
def run(c): subprocess.run(c, shell=True, check=True)
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode())

C = CFG['color']
FONT = "'Noto Serif CJK JP','Noto Sans CJK JP',serif"
SANS = "'Noto Sans CJK JP',sans-serif"
CSS = f"""*{{margin:0;padding:0;box-sizing:border-box}}body{{width:{W}px;height:{H}px;background:transparent;position:relative;font-family:{FONT};color:#fff}}
.hdr{{position:absolute;left:60px;right:60px;top:150px}}
.hdr .row{{display:flex;justify-content:space-between;font-family:{SANS};font-size:26px;font-weight:700;letter-spacing:.04em;text-shadow:0 2px 6px rgba(0,0,0,.45)}}
.hdr .ln{{height:2px;background:rgba(255,255,255,.75);margin:10px 0 14px}}
.pill{{display:inline-block;font-family:{SANS};font-weight:700;border-radius:999px;padding:6px 20px;font-size:28px;background:{C['pill']};color:#fff}}
.card{{position:absolute;left:60px;right:120px;border-radius:26px;background:{C['card']};padding:30px 36px 34px;box-shadow:0 10px 30px rgba(0,0,0,.25)}}
.card .lab{{display:inline-block;font-family:{SANS};font-weight:700;font-size:26px;border-radius:999px;padding:4px 16px;background:{C['lab']};color:{C['labfg']};margin-bottom:14px}}
.card .tx{{font-size:56px;font-weight:700;line-height:1.38;letter-spacing:.02em}}
.card .sm{{font-family:{SANS};font-size:36px;font-weight:700;line-height:1.5;margin-top:14px;opacity:.95}}
.shade{{position:absolute;left:0;right:0;top:0;height:820px;background:linear-gradient(rgba(0,0,0,.45),rgba(0,0,0,0))}}
.ttl{{position:absolute;left:0;right:0;text-align:center;text-shadow:0 3px 12px rgba(0,0,0,.55)}}
.hl{{display:inline-block;background:{C['hl']};color:{C['hlfg']};padding:0 14px;border-radius:8px;text-shadow:none;margin:0 4px}}
"""
def page(pg, html, path):
    pg.set_content(f"<html><head><style>{CSS}</style></head><body>{html}</body></html>")
    pg.wait_for_timeout(120)
    pg.screenshot(path=path, omit_background=True)

scenes = CFG['scenes']
N = sum(1 for s in scenes if s.get('num'))
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium'); pg = b.new_page(viewport={'width': W, 'height': H})
    k = 0
    for i, s in enumerate(scenes):
        html = ''
        if s.get('num'):
            k += 1
            html += f"<div class='hdr'><div class='row'><span>{CFG['brand']}</span><span>{k:02d} / {N:02d}</span></div><div class='ln'></div><span class='pill'>{CFG['tag']}</span></div>"
        t = s['type']
        if t == 'end':
            html += ''
        elif t == 'title':
            html += f"<div class='shade'></div><div class='ttl' style='top:{s.get('y',300)}px'>{s['html']}</div>"
        elif t == 'card':
            html += f"<div class='card' style='top:{s.get('y',1150)}px'>{('<span class=lab>'+s['lab']+'</span><br>') if s.get('lab') else ''}<div class='tx'>{s['text']}</div>{('<div class=sm>'+s['sm']+'</div>') if s.get('sm') else ''}</div>"
        elif t == 'big':
            html += f"<div class='ttl' style='top:{s.get('y',330)}px'>{s['html']}</div>"
        page(pg, html, f'{OUT}/t{i}.png')
    b.close()

# voices
starts = []; t0 = 0.0; parts = []
for i, s in enumerate(scenes):
    wav = f'{OUT}/v{i}.wav'
    run(f'python3 {TTS} "{s["voice"]}" {wav} {CFG.get("speed",1.05)} >/dev/null 2>&1')
    vd = dur(wav)
    d = max(s.get('min', 3.2), 0.35 + vd + s.get('pad', 0.9))
    s['_d'] = round(d, 2); starts.append(t0); t0 += s['_d']
T = round(t0, 2)
print('scene durations', [s['_d'] for s in scenes], 'total', T)

VF = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,format=yuv420p,setsar=1"
for i, s in enumerate(scenes):
    d = s['_d']; bg = s['bg']; seg = f'{OUT}/b{i}.mp4'
    if bg['kind'] == 'video':
        sp = bg.get('speed', 1.0)
        run(f"ffmpeg -v error -y -ss {bg['start']} -t {d*sp+0.3} -i {bg['file']} -an -vf \"setpts=PTS/{sp},{VF},trim=duration={d}\" -c:v libx264 -crf 18 -preset veryfast {seg}")
    else:
        fr = int(round(d * 30))
        z = bg.get('zoom', 0.06); ox = bg.get('x', 0.5); oy = bg.get('y', 0.5)
        run(f"ffmpeg -v error -y -loop 1 -i {bg['file']} -vf \"scale=-2:2400,crop='min(iw,ih*9/16)':'min(ih,iw*16/9)':'(iw-min(iw,ih*9/16))*{ox}':'(ih-min(ih,iw*16/9))*{oy}',scale=1620:2880,zoompan=z='1+{z}*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s={W}x{H}:fps=30,format=yuv420p,setsar=1\" -frames:v {fr} -c:v libx264 -crf 18 -preset veryfast {seg}")
    # overlay text with fade in (0.35s) and fade out at end (0.3s)
    run(f"ffmpeg -v error -y -i {seg} -loop 1 -t {d} -i {OUT}/t{i}.png -filter_complex \"[1]format=rgba,fade=in:st=0.15:d=0.4:alpha=1,fade=out:st={d-0.35}:d=0.3:alpha=1[o];[0][o]overlay=0:0:shortest=1\" -c:v libx264 -crf 18 -preset veryfast -t {d} {OUT}/V{i}.mp4")
# crossfade-free concat with short dip: just concat
open(f'{OUT}/list.txt', 'w').write(''.join(f"file 'V{i}.mp4'\n" for i in range(len(scenes))))
run(f"ffmpeg -v error -y -f concat -safe 0 -i {OUT}/list.txt -c copy {OUT}/silent.mp4")
ins = ''.join(f' -i {OUT}/v{i}.wav' for i in range(len(scenes)))
fl = ';'.join(f"[{i}]adelay={int((starts[i]+0.35)*1000)}|{int((starts[i]+0.35)*1000)}[a{i}]" for i in range(len(scenes)))
mix = ''.join(f'[a{i}]' for i in range(len(scenes)))
run(f"ffmpeg -v error -y{ins} -filter_complex \"{fl};{mix}amix=inputs={len(scenes)}:normalize=0,apad=whole_dur={T},atrim=0:{T},loudnorm=I=-15\" -ar 44100 -ac 2 {OUT}/voice.wav")
run(f"ffmpeg -v error -y -i {OUT}/silent.mp4 -i {OUT}/voice.wav -map 0:v -map 1:a -t {T} -c:v libx264 -crf 25 -preset medium -pix_fmt yuv420p -c:a aac -b:a 96k -movflags +faststart {CFG['out']}")
json.dump({'starts': starts, 'durs': [s['_d'] for s in scenes], 'T': T, 'lines': [s['voice'] for s in scenes]}, open(f'{OUT}/timing.json', 'w'), ensure_ascii=False)
print('done', CFG['out'], os.path.getsize(CFG['out']))
