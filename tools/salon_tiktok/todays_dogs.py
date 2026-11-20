# 今日のワンコたち（OLLIE MAGIC の TikTok）
# 11/20 藤原さん「毎日来たその日のワンコを動画にして切り替えながら紹介したい」
#   「飼い主さんが喜ぶ感じにして、季節的なものも取り入れて」「集客導線も成約につながる様に」
# 使い方: python3 todays_dogs.py <設定.json>
#   設定: {"out":..., "date":"11/20（金）", "season":"autumn", "photos":[...], "endPhoto": 0, "anniv": "18th"}
import json, os, sys, subprocess, shutil
from playwright.sync_api import sync_playwright

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(sys.argv[1]))
OUT = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), 'out_' + os.path.splitext(os.path.basename(sys.argv[1]))[0])
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
TTS = os.path.join(HERE, 'tts_natural.py')
SEC = CFG.get('sec', 2.3)          # 1頭の長さ
XF = 0.35                          # 切りかえ（やさしく重ねる）

def run(c): subprocess.run(c, shell=True, check=True)
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode())

# 季節の飾り（右上・左下に葉っぱ／雪など。顔にかからない端だけ）
SEASON = {
  'autumn': {'items': ['#c8642a', '#d98a3a', '#a8461f', '#e0b04a'], 'word': '秋のおめかし', 'shape': 'leaf'},
  'winter': {'items': ['#ffffff', '#e8f0f8', '#ffffff', '#dfe9f3'], 'word': '冬のおめかし', 'shape': 'snow'},
  'spring': {'items': ['#f6c1cf', '#f9d6de', '#f3a9bd', '#ffe3ea'], 'word': '春のおめかし', 'shape': 'petal'},
  'summer': {'items': ['#7cc6e8', '#a8dcf0', '#5bb3dd', '#ffe08a'], 'word': '夏のおめかし', 'shape': 'petal'},
}[CFG.get('season', 'autumn')]

def leaf(x, y, s, r, c):
    if SEASON['shape'] == 'leaf':
        return (f"<svg style='position:absolute;left:{x}px;top:{y}px;transform:rotate({r}deg)' width='{s}' height='{s}' viewBox='0 0 100 100'>"
                f"<path d='M50 4 L58 30 L84 18 L72 44 L96 52 L70 60 L80 86 L54 72 L50 98 L46 72 L20 86 L30 60 L4 52 L28 44 L16 18 L42 30 Z' fill='{c}' opacity='.92'/>"
                f"<path d='M50 30 L50 98' stroke='rgba(90,40,10,.45)' stroke-width='3'/></svg>")
    if SEASON['shape'] == 'snow':
        return (f"<svg style='position:absolute;left:{x}px;top:{y}px;transform:rotate({r}deg)' width='{s}' height='{s}' viewBox='0 0 100 100'>"
                f"<g stroke='{c}' stroke-width='7' stroke-linecap='round'><path d='M50 8V92M14 29L86 71M14 71L86 29'/></g></svg>")
    return (f"<svg style='position:absolute;left:{x}px;top:{y}px;transform:rotate({r}deg)' width='{s}' height='{s}' viewBox='0 0 100 100'>"
            f"<ellipse cx='50' cy='50' rx='26' ry='44' fill='{c}' opacity='.9'/></svg>")

def deco(corner_only=True):
    c = SEASON['items']
    out = ''
    # 右上
    for i, (x, y, s, r) in enumerate([(930, 150, 120, 20), (850, 250, 80, -30), (990, 300, 70, 60)]):
        out += leaf(x, y, s, r, c[i % 4])
    # 左下（TikTok の文字より上）
    for i, (x, y, s, r) in enumerate([(-20, 1380, 110, -15), (70, 1470, 76, 40), (10, 1290, 64, 75)]):
        out += leaf(x, y, s, r, c[(i + 1) % 4])
    return out

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;background:transparent;font-family:'Noto Serif CJK JP',serif;color:#fff;position:relative;overflow:hidden}
.top{position:absolute;left:0;right:0;top:0;height:330px;background:linear-gradient(rgba(60,35,25,.55),rgba(60,35,25,0))}
.hdr{position:absolute;left:60px;top:130px;display:flex;align-items:center;gap:18px;font-family:'Noto Sans CJK JP',sans-serif}
.chip{background:rgba(122,78,62,.92);color:#fff;border-radius:999px;padding:10px 26px;font-size:34px;font-weight:700}
.cnt{font-size:34px;font-weight:700;text-shadow:0 2px 8px rgba(0,0,0,.5)}
.ttlcard{position:absolute;left:70px;right:70px;top:1120px;background:rgba(122,78,62,.86);border-radius:36px;padding:46px 40px 50px;text-align:center}
.ttlcard .k{display:inline-block;background:#f1e1d8;color:#6b4334;font-family:'Noto Sans CJK JP',sans-serif;font-weight:700;font-size:36px;border-radius:999px;padding:8px 28px}
.ttlcard .t{font-size:104px;font-weight:700;margin-top:18px;line-height:1.2}
.ttlcard .s{font-size:40px;margin-top:16px;font-family:'Noto Sans CJK JP',sans-serif}
.thanks{position:absolute;left:70px;right:70px;top:1200px;background:rgba(122,78,62,.86);border-radius:36px;padding:44px 40px;text-align:center}
.thanks .t{font-size:70px;font-weight:700;line-height:1.35}
.thanks .s{font-size:38px;margin-top:18px;font-family:'Noto Sans CJK JP',sans-serif;line-height:1.5}
"""

photos = CFG['photos']; N = len(photos)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium'); pg = b.new_page(viewport={'width': W, 'height': H})
    def shot(html, path):
        pg.set_content(f"<html><head><style>{CSS}</style></head><body>{html}</body></html>"); pg.wait_for_timeout(120)
        pg.screenshot(path=path, omit_background=True)
    anniv = f"<div class='s'>{CFG['anniv']}</div>" if CFG.get('anniv') else ''
    shot(f"<div class='top'></div>{deco()}<div class='hdr'><span class='chip'>{CFG['date']}</span></div>"
         f"<div class='ttlcard'><span class='k'>{SEASON['word']}</span><div class='t'>今日の<br>ワンコたち</div><div class='s'>Dog salon OLLIE MAGIC</div>{anniv}</div>", f'{OUT}/o_title.png')
    for i in range(N):
        shot(f"<div class='top'></div>{deco()}<div class='hdr'><span class='chip'>今日のワンコ</span><span class='cnt'>{i+1} / {N}</span></div>", f'{OUT}/o_{i}.png')
    shot(f"<div class='top'></div>{deco()}<div class='hdr'><span class='chip'>{CFG['date']}</span></div>"
         f"<div class='thanks'><div class='t'>今日も来てくれて<br>ありがとう</div><div class='s'>{CFG.get('thanksSub','また、きれいにしにきてね')}</div></div>", f'{OUT}/o_thanks.png')
    b.close()

def clip(src, ov, d, out, z0=1.0, z1=1.07):
    # 写真を縦 1920 に合わせて中央で切り取り（縮めすぎない）、ゆっくり寄る。上に飾りの画像を重ねる。途中は劣化なし。
    n = int(round(d * FPS))
    vf = (f"scale=-2:3840,crop=2160:3840,zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},format=yuv444p")
    run(f"ffmpeg -v error -y -loop 1 -i '{src}' -i '{ov}' -filter_complex \"[0:v]{vf}[b];[b][1:v]overlay=0:0,format=yuv444p\" -t {d} -r {FPS} -c:v libx264 -qp 0 -preset ultrafast {out}")

# 声（最初と最後だけ。途中は写真をゆっくり見てもらう）
v1, v2 = f'{OUT}/v_title.wav', f'{OUT}/v_end.wav'
run(f'python3 {TTS} "{CFG.get("voiceTitle","今日、オーリーマジックに来てくれた、ワンコたちです。")}" {v1} >/dev/null 2>&1')
run(f'python3 {TTS} "{CFG.get("voiceThanks","今日も来てくれて、ありがとう。")}" {OUT}/v_thanks.wav >/dev/null 2>&1')
run(f'python3 {TTS} "{CFG.get("voiceEnd","ご予約は、プロフィールのラインから、どうぞ。")}" {v2} >/dev/null 2>&1')
dT = max(3.2, 0.3 + dur(v1) + 0.6); dK = max(2.8, 0.3 + dur(f'{OUT}/v_thanks.wav') + 0.6); dE = max(4.0, 0.3 + dur(v2) + 0.7)

parts = []
# 題の背景：今日の子を全員並べた写真（同じ子が2回続かないように）
from PIL import Image, ImageOps
cols = 3; rows = (N + cols - 1) // cols
cw, ch = 2160 // cols, 3840 // rows
col = Image.new('RGB', (2160, 3840), (251, 244, 238))
for i, f in enumerate(photos):
    im = ImageOps.fit(Image.open(f).convert('RGB'), (cw - 12, ch - 12), Image.LANCZOS, centering=(0.5, 0.4))
    col.paste(im, ((i % cols) * cw + 6, (i // cols) * ch + 6))
if N % cols:
    # あまった枠はロゴの色の地に店名
    pass
col.save(f'{OUT}/collage.jpg', quality=97, subsampling=0)
clip(f'{OUT}/collage.jpg', f'{OUT}/o_title.png', dT, f'{OUT}/c_title.mp4', 1.0, 1.04); parts.append((f'{OUT}/c_title.mp4', dT))
for i, ph in enumerate(photos):
    clip(ph, f'{OUT}/o_{i}.png', SEC, f'{OUT}/c_{i}.mp4'); parts.append((f'{OUT}/c_{i}.mp4', SEC))
clip(photos[CFG.get('thanksPhoto', -1)], f'{OUT}/o_thanks.png', dK, f'{OUT}/c_thanks.mp4', 1.05, 1.0); parts.append((f'{OUT}/c_thanks.mp4', dK))

# 最後の画面：end_ollie.jpg の枠に、今日の子の写真（顔のアップ・正方形）
from PIL import Image
end = Image.open(os.path.join(HERE, 'end_ollie.jpg')).convert('RGB')
ph = Image.open(photos[CFG.get('endPhoto', 0)]).convert('RGB')
fx, fy, fs = CFG.get('endCrop', [0.5, 0.42, 0.62])  # 顔の中心（割合）と切り取る幅（写真の幅に対する割合）
s = int(ph.width * fs); cx, cy = int(ph.width * fx), int(ph.height * fy)
box = (max(0, cx - s // 2), max(0, cy - s // 2)); box = (box[0], box[1], box[0] + s, box[1] + s)
end.paste(ph.crop(box).resize((597, 597), Image.LANCZOS), (242, 511))
end.save(f'{OUT}/end.png')
run(f"ffmpeg -v error -y -loop 1 -i {OUT}/end.png -vf format=yuv444p -t {dE} -r {FPS} -c:v libx264 -qp 0 -preset ultrafast {OUT}/c_end.mp4")
parts.append((f'{OUT}/c_end.mp4', dE))

# つなぐ（やさしく重ねる切りかえ）
inp = ' '.join(f'-i {p}' for p, _ in parts)
fc = ''; prev = '[0:v]'; off = 0.0
for k in range(1, len(parts)):
    off += parts[k-1][1] - XF
    fc += f"{prev}[{k}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[x{k}];"; prev = f'[x{k}]'
total = sum(d for _, d in parts) - XF * (len(parts) - 1)
# 声の位置
tEnd = total - dE + 0.3; tThanks = total - dE - dK + XF + 0.3
fc += f"{prev}format=yuv420p[v];[{len(parts)}:a]adelay=300|300[a1];[{len(parts)+1}:a]adelay={int(tThanks*1000)}|{int(tThanks*1000)}[a2];[{len(parts)+2}:a]adelay={int(tEnd*1000)}|{int(tEnd*1000)}[a3];[a1][a2][a3]amix=inputs=3:normalize=0,apad[a]"
run(f"ffmpeg -v error -y {inp} -i {v1} -i {OUT}/v_thanks.wav -i {v2} -filter_complex \"{fc}\" -map [v] -map [a] -t {total:.3f} "
    f"-c:v libx264 -crf 16 -preset slow -profile:v high -pix_fmt yuv420p -r {FPS} -c:a aac -b:a 192k -movflags +faststart {CFG['out']}")
print('done', CFG['out'], round(total, 2), os.path.getsize(CFG['out']))
