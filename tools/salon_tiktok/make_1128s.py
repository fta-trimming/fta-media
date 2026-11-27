# 11/28（土）差しかえ：手順・技術のリール「後肢は 四角→八角→丸」（11/27 23:45 藤原さん「至急明日分から修正を」）
# 1場面目＝仕上がりの実際の映像＋答えを大きく／実演（早回し）を3場面／プレゼント
import json, os, sys, base64, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
from make_w1123 import svg, t, box, B, HL, RD, G, Y, R, LG, GR
SRC = sys.argv[1]
V2 = os.path.join(SRC, 'v2.mp4')  # 11/7 撮影（カット中心のまだ使っていない素材 2）
def hookv(top, big, red, voice, clip, start):
    html = (f"<div style='font-family:Noto Sans CJK JP;font-size:70px;font-weight:900;color:#fff;-webkit-text-stroke:3px #000;paint-order:stroke'>{top}</div>"
            f"<div style='font-family:Noto Sans CJK JP;font-size:150px;font-weight:900;line-height:1.1;margin-top:16px;color:#f6d77a;-webkit-text-stroke:7px #1b2e22;paint-order:stroke'>{big}</div>"
            f"<div style='display:inline-block;margin-top:22px;background:#e0412f;color:#fff;font-family:Noto Sans CJK JP;font-weight:900;font-size:58px;padding:8px 30px;border-radius:14px'>{red}</div>")
    return {'type': 'title', 'y': 380, 'min': 3.4, 'pad': 0.35, 'html': html, 'bg': {'kind': 'video', 'file': clip, 'start': start, 'speed': 1.0}, 'voice': voice, 'pop': True, 'punch': True}
def demo(num, step, text, shape, voice, start, speed):
    sh = {'sq': "<rect x='14' y='14' width='72' height='72' fill='none' stroke='#f6d77a' stroke-width='9'/>",
          'oc': "<polygon points='35,10 65,10 90,35 90,65 65,90 35,90 10,65 10,35' fill='none' stroke='#f6d77a' stroke-width='9'/>",
          'ci': "<circle cx='50' cy='50' r='40' fill='none' stroke='#f6d77a' stroke-width='9'/>"}[shape]
    html = (f"<div style='display:inline-flex;align-items:center;gap:26px;background:rgba(36,64,47,.9);border-radius:28px;padding:22px 36px;box-shadow:0 10px 30px rgba(0,0,0,.3)'>"
            f"<svg width='160' height='160' viewBox='0 0 100 100'>{sh}</svg><div style='text-align:left'>"
            f"<div style='font-family:Noto Sans CJK JP;font-size:52px;font-weight:900;color:#f6d77a'>{step}</div>"
            f"<div style='font-family:Noto Sans CJK JP;font-size:84px;font-weight:900;color:#fff;line-height:1.2'>{text}</div></div></div>"
            f"<div style='margin-top:16px'><span style='background:#fff;color:#24402f;font-family:Noto Sans CJK JP;font-weight:900;font-size:32px;padding:4px 18px;border-radius:999px'>実際の作業 ×{speed}倍速</span></div>")
    return {'type': 'big', 'num': num, 'y': 300, 'html': html, 'bg': {'kind': 'video', 'file': V2, 'start': start, 'speed': speed}, 'voice': voice, 'min': 4.4, 'pad': 0.6, 'pop': True, 'punch': False}
def card(num, lab, text, sm, voice, bg, illus, mn=4.4, pad=0.75):
    return {'type': 'card', 'num': num, 'y': 1070, 'lab': lab, 'text': text, 'sm': sm, 'bg': B(bg), 'voice': voice, 'min': mn, 'pad': pad, 'pop': True, 'punch': True, 'illus': illus, 'iy': 290, 'ih': 720}
def leg_top(x, y, kind, col):
    if kind == 'free': return f"<path d='M{x-60} {y} q 10 -70 70 -64 q 62 10 50 74 q -12 60 -70 52 q -58 -6 -50 -62z' fill='#fff' stroke='{col}' stroke-width='10'/>"
    if kind == 'free2': return f"<path d='M{x-48} {y-10} q 20 -60 62 -50 q 52 14 40 64 q -6 64 -62 56 q -50 -10 -40 -70z' fill='#fff' stroke='{col}' stroke-width='10'/>"
    return f"<circle cx='{x}' cy='{y}' r='62' fill='#fff' stroke='{col}' stroke-width='10'/>"
def gift_illus():
    d = os.path.join(ROOT, 'gift', '2026-11-28s'); out = []
    for i in (2, 1):
        sm = os.path.join(HERE, f'_g1128s_{i}.jpg')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(d, f'kit_{i}.jpg'), '-vf', 'scale=840:-1:flags=lanczos', '-q:v', '2', sm], check=True)
        out.append(base64.b64encode(open(sm, 'rb').read()).decode()); os.remove(sm)
    imgs = ''.join(f"<img src='data:image/jpeg;base64,{b}' style='position:absolute;height:600px;left:{360+o*80}px;top:{40+o*10}px;transform:rotate({r}deg);box-shadow:0 8px 24px rgba(0,0,0,.25);border-radius:6px'>" for b, o, r in zip(out, (1, 0), (5, -2)))
    return f"<div style='position:relative;width:920px;height:668px'>{imgs}<div style='position:absolute;left:20px;top:170px;font-family:Noto Sans CJK JP;font-weight:900;font-size:120px'>🎁</div><div style='position:absolute;left:10px;top:330px;width:340px;text-align:center;font-family:Noto Sans CJK JP;font-weight:700;font-size:40px;color:{G};line-height:1.4'>A4・2ページ<br><span style='background:{Y};padding:0 10px;border-radius:8px'>DMでお届け</span></div></div>"

scenes = [
 hookv('「後肢が、左右でそろわない…」', '四角→八角→丸', 'この順で切るだけ', 'こうしが、左右でそろわない。四角、八角、丸の順で切ります。', V2, 220.0),
 card(1, 'なぜ？', 'いきなり丸く切ると<br>' + RD('左右で形が変わる'), '人によって、丸の形がちがう',
      'いきなり丸く切ると、人によって、左右で形が変わります。', 'table',
      svg(box(30, 40, 410, 600, '#fff2ef') + t(235, 110, 'いきなり丸', 50, R) + leg_top(160, 330, 'free', R) + leg_top(310, 330, 'free2', R) + t(235, 520, '左右で形がちがう', 40, R) + t(235, 590, '✕', 60, R)
          + box(480, 40, 410, 600, '#eef5f0') + t(685, 110, '四角→八角→丸', 46, LG)
          + "<rect x='520' y='180' width='90' height='90' fill='none' stroke='#3d7a55' stroke-width='8'/><polygon points='665,180 705,180 735,210 735,250 705,280 665,280 635,250 635,210' fill='none' stroke='#3d7a55' stroke-width='8'/><circle cx='810' cy='230' r='48' fill='none' stroke='#3d7a55' stroke-width='8'/>"
          + leg_top(610, 400, 'c', LG) + leg_top(760, 400, 'c', LG) + t(685, 520, '左右が同じ形', 40, LG) + t(685, 590, '○', 60, LG))),
 demo(2, '① 四角', '面を作る', 'sq', 'まずアタッチメントで、前、横、後ろの面。これが四角。', 4.0, 4),
 demo(3, '② 八角', '角を落とす', 'oc', '次にハサミで、四つの角だけ落とす。これで八角。', 134.0, 3),
 demo(4, '③ 丸', '角を取る', 'ci', '最後に、八角の角を取ると、丸です。', 176.0, 3),
 card(5, 'すると', '左右が<br>' + HL('同じ形') + 'になる', '新人さんにも、順番で教えられる',
      '左右が、同じ形になります。新人さんにも、順番で教えられます。', 'note',
      svg(leg_top(300, 300, 'c', LG) + leg_top(620, 300, 'c', LG) + "<line x1='160' y1='300' x2='760' y2='300' stroke='#3d7a55' stroke-width='6' stroke-dasharray='14 10'/>"
          + t(460, 470, '上から見ても、後ろから見ても', 40, G) + t(460, 560, '同じ太さ・同じ丸', 56, LG))),
 card(6, '🎁 プレゼント', '四角→八角→丸<br>後肢の手順シート', 'コメントに「手順」と書いてね',
      '手順シートがほしい方は、コメントで、てじゅん、と書いてね。', 'table', gift_illus(), 3.6, 0.8),
]
cfg = {'out': 'FTA_2026-11-28_shikaku.mp4', 'tts': '/home/claude/fta-media/tools/voicevox/tts_voices.py', 'voiceName': 'aoyama', 'speed': 1.2, 'crf': 14,
       'size': [720, 1280], 'brand': 'FUJIWARA TRIMMING ACADEMY', 'tag': 'トリミングサロンの生産性',
       'color': {'card': 'rgba(36,64,47,.86)', 'pill': 'rgba(61,107,79,.95)', 'lab': '#f6d77a', 'labfg': '#24402f', 'hl': '#f6d77a', 'hlfg': '#24402f'}, 'scenes': scenes}
json.dump(cfg, open(os.path.join(HERE, '2026-11-28_fta_shikaku.json'), 'w'), ensure_ascii=False, indent=1)
print('ok')
