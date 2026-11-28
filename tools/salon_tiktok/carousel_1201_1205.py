import json, sys, subprocess, os
CSS = """*{box-sizing:border-box;margin:0;padding:0}body{font-family:'Noto Sans CJK JP',sans-serif;color:#333}
.s{width:1080px;height:1080px;position:relative;background:#fff;overflow:hidden;padding:120px 90px 130px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start}.s>.big,.s>.sm{align-self:stretch}
.top{position:absolute;top:44px;left:90px;right:90px;display:flex;justify-content:space-between;font-size:24px;font-weight:700;color:#3d6b4f;letter-spacing:.08em}
.dots{position:absolute;bottom:54px;left:90px;display:flex;gap:14px}.dots i{width:16px;height:16px;border-radius:50%;background:#d6e4db}.dots i.on{background:#3d6b4f}
.nx{position:absolute;bottom:44px;right:90px;font-size:28px;font-weight:700;color:#3d6b4f}
.tag{display:inline-block;background:#3d6b4f;color:#fff;font-weight:700;font-size:30px;padding:8px 24px;border-radius:999px}
h1{font-size:76px;line-height:1.3;color:#24402f;margin-top:26px;font-weight:900}
h2{font-size:62px;line-height:1.35;color:#24402f;margin-top:22px;font-weight:900}
.g{color:#3d6b4f}.r{color:#c8443a}.y{background:#f6d77a;padding:0 10px}
.ex{align-self:stretch;margin-top:36px;border-left:10px solid #3d6b4f;background:#e8f2ec;padding:26px 32px;font-size:36px;line-height:1.7}
.big{font-size:120px;font-weight:900;color:#24402f;text-align:center;margin-top:40px}
.sm{font-size:26px;color:#6b6b6b;margin-top:18px}
.cover{background:#24402f;color:#fff}.cover h1{color:#fff;font-size:88px}.cover .y{color:#24402f}
.ck{font-size:44px;line-height:1.6;margin-top:30px;font-weight:700;color:#24402f}
.gift{background:#e8f2ec}.giftbox{align-self:stretch;margin-top:40px;background:#fff;border:4px solid #3d6b4f;border-radius:28px;padding:40px;text-align:center}
.kw{display:inline-block;background:#f6d77a;color:#24402f;font-size:84px;font-weight:900;padding:6px 40px;border-radius:20px;margin:18px 0}
"""
def page(i, n, inner, cls=''):
    dots = ''.join(f"<i class='{'on' if k == i else ''}'></i>" for k in range(1, n + 1))
    nx = '保存して見返してね' if i == n else 'スワイプ →'
    return f"<div class='s {cls}'><div class='top'><span>FUJIWARA TRIMMING ACADEMY</span><span>{i} / {n}</span></div>{inner}<div class='dots'>{dots}</div><div class='nx'>{nx}</div></div>"
def build(name, slides):
    n = len(slides)
    html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>" + ''.join(page(i + 1, n, s[1], s[0]) for i, s in enumerate(slides)) + "</body></html>"
    open(f'{name}.html', 'w').write(html)
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1080,height:1080}}}});
await p.goto('file://'+process.cwd()+'/{name}.html');await p.waitForTimeout(300);const s=await p.$$('.s');for(let i=0;i<s.length;i++)await s[i].screenshot({{path:'{name}_'+String(i+1).padStart(2,'0')+'.png'}});await b.close()}})();"""
    open('shot.js', 'w').write(js); subprocess.run(['node', 'shot.js'], check=True)
    for i in range(1, n + 1):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{name}_{i:02d}.png', '-q:v', '2', f'{name}_{i:02d}.jpg'], check=True); os.remove(f'{name}_{i:02d}.png')
def bars(items, unit):
    # items: (label, value, color)
    mx = max(abs(v) for _, v, _ in items); out = ''
    for lab, v, c in items:
        w = int(abs(v) / mx * 440)
        out += f"<div style='display:flex;align-items:center;gap:20px;margin-top:34px'><div style='width:200px;font-size:38px;font-weight:700;text-align:right'>{lab}</div><div style='height:64px;width:{max(w,8)}px;background:{c};border-radius:12px'></div><div style='font-size:40px;font-weight:900;color:{c};white-space:nowrap'>{'+' if (v>0 and unit=='万円') else ''}{v}{unit}</div></div>"
    return out
S1 = [
 ('cover', "<span class='tag' style='background:#f6d77a;color:#24402f'>集客</span><h1>時短で空いた枠、<br>どう埋める？</h1><p style='font-size:44px;margin-top:40px;line-height:1.6'>新規を待つより先に、<br><span class='y'>リピーターさんの月1回</span>で埋める</p>"),
 ('', "<span class='tag'>あるある</span><h2>早くなったのに、<br>空いた枠が<span class='r'>そのまま</span></h2><div class='ex'>時短で生まれた時間に、<br>予約が入っていない。</div>"),
 ('', "<span class='tag'>理由</span><h2>新規だけで埋めようと<br>している</h2><div class='ex'>新規は、知ってもらって、<br>予約が入るまでに時間がかかります。</div>"),
 ('', "<span class='tag'>すぐできること</span><h2>リピーターさんの<br><span class='g'>来る周期</span>を短くする</h2><div class='ex'>新しいお客様を探さなくても、<br>今のお客様だけで枠が埋まり始めます。</div>"),
 ('', "<span class='tag'>数字で見る（例）</span><h2 style='font-size:54px'>リピーターさん20頭が<br>2か月に1回 → 月1回なら</h2>" + bars([('2か月に1回', 10, '#9bb8a6'), ('月1回', 20, '#3d6b4f')], '頭/月') + "<p class='big' style='font-size:84px;margin-top:30px;align-self:stretch'>＋<span class='g'>10枠</span> / 月</p><p class='sm'>（例）20頭÷2か月＝月10頭 → 月1回で月20頭</p>"),
 ('', "<span class='tag'>やること</span><p class='ck'>✅ 月1回のケアをおすすめする</p><p class='ck'>✅ スタイルを保つなら、<br>　 最低でも月1回とお伝えする</p><div class='ex'>おすすめする理由（毛玉・形が保てる）を、<br>お迎えのときにひと言で。</div>"),
 ('', "<span class='tag'>まとめ</span><h2>空いた枠は、<br>まず<span class='y'>リピーターさん</span>から</h2><div class='ex'>空いた時間の一部は、<br>スタッフの練習にも使えます。</div>"),
 ('gift', "<span class='tag'>🎁 プレゼント</span><div class='giftbox'><p style='font-size:46px;font-weight:900;color:#24402f'>空いた枠を埋める<br>来店の周期メモ</p><p style='font-size:36px;margin-top:20px'>コメントに</p><span class='kw'>周期</span><p style='font-size:36px'>と書いてください → DMでお送りします</p><p class='sm'>登録・ログイン不要</p></div>"),
]
S5 = [
 ('cover', "<span class='tag' style='background:#f6d77a;color:#24402f'>数字</span><h1>早くなったのに、<br>余裕がない…</h1><p style='font-size:50px;margin-top:40px;line-height:1.5'><span class='y'>59頭までは赤字</span>（例）</p><p style='font-size:30px;margin-top:20px;opacity:.85'>毎月36万円・1頭6,000円なら</p>"),
 ('', "<span class='tag'>あるある</span><h2>時短で早くなっても、<br>予約が入らないと…</h2><div class='ex'>空き時間が増えるだけ。<br>売上は変わりません。</div>"),
 ('', "<span class='tag'>計算①</span><h2>トントンの頭数</h2><p class='big'>36万 ÷ 6,000<br>＝ <span class='g'>60頭</span></p><p class='sm'>（例）毎月かかるお金 ÷ 1頭の料金</p>"),
 ('', "<span class='tag'>数字で見る（例）</span><h2 style='font-size:54px'>頭数でこう変わる</h2>" + bars([('50頭', -6, '#c8443a'), ('60頭', 0, '#9bb8a6'), ('75頭', 9, '#3d6b4f')], '万円') + "<p class='sm' style='margin-top:30px'>（例）50頭×6,000＝30万−36万＝−6万／75頭×6,000＝45万−36万＝＋9万</p>"),
 ('', "<span class='tag'>計算②</span><h2>1日に直すと</h2><p class='big' style='font-size:96px'>60頭 ÷ 25日<br>＝ 1日<span class='g'>2.4頭</span></p><p class='sm'>（例）営業日25日。1日3頭なら黒字側</p>"),
 ('', "<span class='tag'>やること</span><p class='ck'>✅ 形はアタッチメント、<br>　 ハサミは仕上げだけ</p><p class='ck'>✅ 時短した分の時間に、<br>　 予約を入れる</p>"),
 ('', "<span class='tag'>まとめ</span><h2>1日3頭 × 25日 ＝ 75頭で<br><span class='g'>＋9万円</span>（例）</h2><div class='ex'>早くなった時間に予約が入って、<br>はじめて黒字になります。</div>"),
 ('gift', "<span class='tag'>🎁 プレゼント</span><div class='giftbox'><p style='font-size:46px;font-weight:900;color:#24402f'>何頭で黒字？<br>頭数の計算シート</p><p style='font-size:36px;margin-top:20px'>コメントに</p><span class='kw'>計算</span><p style='font-size:36px'>と書いてください → DMでお送りします</p><p class='sm'>登録・ログイン不要</p></div>"),
]
build('c1201', S1); build('c1205', S5)
from PIL import Image
for nm in ('c1201', 'c1205'):
    ims = [Image.open(f'{nm}_{i:02d}.jpg').resize((360, 360)) for i in range(1, 9)]
    c = Image.new('RGB', (1440, 720), 'white')
    for i, im in enumerate(ims): c.paste(im, ((i % 4) * 360, (i // 4) * 360))
    c.save(f'{nm}_sheet.jpg')
print('ok')
