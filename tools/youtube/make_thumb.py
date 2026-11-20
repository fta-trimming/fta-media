# YouTube ショートのサムネイル（1080×1920）：題が一目で分かる形。
# 11/20 21:48 藤原さん「サムネルをタイトルが分かる様にしてほしい」
# 使い方: python3 make_thumb.py <cut|fta> <札> <題1行目> <題2行目> <出力.jpg> [BEFORE画像] [AFTER画像]
#  画像が2枚ならBEFORE/AFTERを並べる。1枚なら大きく1枚。0枚なら文字だけ。
import sys, subprocess, tempfile, os, base64
acc, tag, t1, t2, out = sys.argv[1:6]; imgs = sys.argv[6:8]
bg, ac = ('#231a17', '#f2d27a') if acc == 'cut' else ('#24402f', '#f6d77a')
def uri(p): return 'data:image/jpeg;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
if len(imgs) == 2:
    pics = f"""<div style='display:flex;gap:24px;margin-top:70px'>
<div class=p><img src='{uri(imgs[0])}'><div class=l style='background:#fff;color:#1d3a2a'>BEFORE</div></div>
<div class=p><img src='{uri(imgs[1])}'><div class=l style='background:{ac};color:{bg}'>AFTER</div></div></div>"""
elif len(imgs) == 1:
    pics = f"<div class=p style='width:900px;height:980px;margin-top:70px'><img src='{uri(imgs[0])}'></div>"
else:
    pics = ''
html = f"""<html><head><meta charset=utf8><style>
body{{margin:0;width:1080px;height:1920px;background:{bg};font-family:'Noto Sans CJK JP',sans-serif;display:flex;flex-direction:column;align-items:center;padding-top:150px;box-sizing:border-box}}
.tag{{background:{ac};color:{bg};font-weight:900;font-size:56px;padding:14px 40px;border-radius:16px;letter-spacing:3px}}
.t1{{color:#fff;font-weight:900;font-size:104px;margin-top:50px;text-align:center;line-height:1.25}}
.t2{{color:{ac};font-weight:900;font-size:104px;text-align:center;line-height:1.25}}
.p{{width:438px;height:900px;border-radius:36px;overflow:hidden;position:relative;background:#000}}
.p img{{width:100%;height:100%;object-fit:cover;object-position:50% 40%}}
.l{{position:absolute;top:22px;left:22px;font-weight:900;font-size:40px;padding:8px 22px;border-radius:12px;letter-spacing:2px}}
</style></head><body><div class=tag>{tag}</div><div class=t1>{t1}</div><div class=t2>{t2}</div>{pics}</body></html>"""
d = tempfile.mkdtemp(); open(f'{d}/t.html', 'w').write(html)
subprocess.run(f"node -e \"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1080,height:1920}}}});await p.goto('file://{d}/t.html');await p.waitForTimeout(500);await p.screenshot({{path:'{d}/t.png'}});await b.close()}})()\"", shell=True, check=True)
from PIL import Image
Image.open(f'{d}/t.png').convert('RGB').save(out, quality=92)
print('ok', out, os.path.getsize(out))
