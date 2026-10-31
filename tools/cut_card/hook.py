# カット中心リールの「最初の縦書きカード（表紙のカード）」を、毎回同じ位置・大きさで作る。
# 10/31 藤原さんの指示「タイトルカードを前回と同じ位置に。今後もその位置で同じになる様に」
# 見本：cut/2026-10-30/reel.mp4（アタッチメント8本）の最初のカード。
#   カード：左 342px・上 457px・幅 396px・高さ 994px（右はし 738・下 1451）、角丸 22px、色 rgba(36,23,19,0.80)
#   右の列：小見出し（例「足先バリカン」）白・太字。数字などは黄色 #f2d06b にできる
#   左の2列：見出し（大きい白の太字）。強調の言葉は黄色 #f2d06b
#   文字の長さでカードの位置・大きさは変えない（文字の大きさだけ自動で小さくして収める）
# 使い方：python3 tools/cut_card/hook.py hook.json out.png [背景.png]
#   hook.json の例：{"label":"足先バリカン","lines":["足を曲げた","[角]から爪へ"]}
#   [ ] で囲んだ所が黄色になる。背景を渡すと、背景＋カードの1080×1920（表紙用）を作る。
#   背景なしなら透明PNG（動画に overlay で重ねる）。
import json, sys, re, base64
from playwright.sync_api import sync_playwright

BOX = dict(left=342, top=457, width=396, height=994)


def mark(s):
    s = s.replace('&', '&amp;').replace('<', '&lt;')
    return re.sub(r'\[(.+?)\]', r'<em>\1</em>', s)


def html(cfg, bg=None):
    lines = cfg['lines']
    longest = max(len(re.sub(r'[\[\]]', '', l)) for l in lines)
    lab_len = len(re.sub(r'[\[\]]', '', cfg.get('label', '')))
    # 見出しは高さ 994 の中に収まる大きさ（見本は 7字で 約112px）
    big = min(112, int((BOX['height'] - 100) / (longest * 1.07)))
    small = min(50, int((BOX['height'] - 120) / max(lab_len, 1) / 1.02))
    bgcss = ''
    if bg:
        b64 = base64.b64encode(open(bg, 'rb').read()).decode()
        bgcss = f"background:url(data:image/png;base64,{b64}) center/cover;"
    cols = ''.join(f'<div class="big">{mark(l)}</div>' for l in lines)
    return f"""<html><head><style>
html,body{{margin:0;width:1080px;height:1920px;{bgcss}background-color:{'#000' if bg else 'transparent'};}}
.card{{position:absolute;left:{BOX['left']}px;top:{BOX['top']}px;width:{BOX['width']}px;height:{BOX['height']}px;
 border-radius:22px;background:rgba(36,23,19,0.80);display:flex;flex-direction:row-reverse;justify-content:center;
 align-items:flex-start;padding-top:44px;box-sizing:border-box;gap:10px;font-family:'Noto Sans CJK JP';}}
.lab{{writing-mode:vertical-rl;font-size:{small}px;font-weight:900;color:#fff;letter-spacing:2px;margin-top:4px;white-space:nowrap;text-combine-upright:none;}}
.big{{writing-mode:vertical-rl;font-size:{big}px;font-weight:900;color:#fff;line-height:1.08;letter-spacing:3px;white-space:nowrap;}}
em{{font-style:normal;color:#f2d06b;}}
</style></head><body><div class="card"><div class="lab">{mark(cfg.get('label',''))}</div>{cols}</div></body></html>"""


def render(cfg, out, bg=None):
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.set_content(html(cfg, bg))
        pg.wait_for_timeout(300)
        pg.screenshot(path=out, omit_background=not bg)
        b.close()


if __name__ == '__main__':
    cfg = json.load(open(sys.argv[1]))
    render(cfg, sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
