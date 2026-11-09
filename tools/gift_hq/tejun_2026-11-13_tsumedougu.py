# 11/13 手順まとめ（爪切り道具）を高画質で組み直す：文字・枠・しるしは2倍の細かさで描き直し、写真は今ある一番よいもの
import base64,io,sys,os
from PIL import Image
from playwright.sync_api import sync_playwright
S=int(sys.argv[1]) if len(sys.argv)>1 else 2
old=Image.open('old.jpg').convert('RGB')
def ph(box):
    b=io.BytesIO(); old.crop(box).save(b,'PNG'); return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
D='#231613';Y='#f2d06b';R='#c9573b'
tools=[('爪切り','よく切れるもの',70),('電動ヤスリ','基本はこれ',390),('手動のヤスリ','音が苦手な子に',710)]
steps=['切れ味のよい<br>爪切りを使う','深爪をふせぎ<br>長さを整える','ヤスリは電動<br>当てるだけ','音が苦手な子は<br>手動のヤスリ','無理な力をかけず<br>足先を安定']
h=f'''<html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;background:{D};font-family:'Noto Sans CJK JP',sans-serif;color:#fff;overflow:hidden;position:relative}}
.a{{position:absolute}} .y{{color:{Y}}}
.ph{{position:absolute;overflow:hidden;border-radius:18px}} .ph img{{display:block;width:100%;height:100%}}
.tg{{position:absolute;font-weight:900;border-radius:8px;white-space:nowrap}}
</style></head><body>
<div class="a" style="left:60px;top:74px;font-size:31px;letter-spacing:3.3px;font-weight:500;color:#f3ebe3">CUT TECHNIQUE ／ @naohide_fujiwara</div>
<div class="a" style="left:60px;top:118px;height:56px;padding:0 18px;background:{R};border-radius:8px;font-size:30px;font-weight:900;line-height:56px">保存版・手順まとめ</div>
<div class="a" style="left:58px;top:192px;font-size:90px;font-weight:900;line-height:108px;letter-spacing:-2px">爪切りは<span class="y">切れ味</span>、<br>ヤスリは<span class="y">電動</span>が基本</div>
<div class="a" style="left:60px;top:418px;font-size:27px;letter-spacing:-.3px;font-weight:500;color:#cfc4ba">爪切り・ヤスリの道具の使い分け（5つの手順）</div>
<div class="ph" style="left:50px;top:480px;width:470px;height:600px"><img src="{ph((50,480,520,1080))}"></div>
<div class="ph" style="left:560px;top:480px;width:470px;height:600px"><img src="{ph((560,480,1030,1080))}"></div>
<div class="tg" style="left:66px;top:496px;height:64px;padding:0 20px;background:#fff;color:{D};font-size:37px;line-height:64px">BEFORE</div>
<div class="tg" style="left:576px;top:496px;height:64px;padding:0 20px;background:{Y};color:{D};font-size:37px;line-height:64px">AFTER</div>
<div class="tg" style="left:66px;top:1008px;height:56px;padding:0 16px;background:rgba(35,22,19,.92);color:#fff;font-size:31px;line-height:56px">ヤスリの前</div>
<div class="tg" style="left:576px;top:1008px;height:56px;padding:0 16px;background:rgba(35,22,19,.92);color:{Y};font-size:31px;line-height:56px">ヤスリの後</div>
<div class="a" style="left:510px;top:750px;width:60px;height:60px;border-radius:50%;background:{Y};border:2px solid {D}"><div style="position:absolute;left:23px;top:17px;width:0;height:0;border-left:19px solid {D};border-top:13px solid transparent;border-bottom:13px solid transparent"></div></div>
'''
for i,(t,s,x) in enumerate(tools):
    h+=f'''<div class="a" style="left:{x}px;top:1110px;width:300px;height:160px;background:#f6f1eb;border-radius:12px"></div>
<div class="ph" style="left:{x+10}px;top:1148px;width:112px;height:84px;border-radius:9px"><img src="{ph((x+10,1148,x+122,1232))}"></div>
<div class="a" style="left:{x+135}px;top:1150px;font-size:26px;font-weight:900;color:{D};white-space:nowrap">{t}</div>
<div class="a" style="left:{x+135}px;top:1196px;font-size:19px;font-weight:900;color:#b5643c;white-space:nowrap">{s}</div>'''
for i,t in enumerate(steps):
    x=30+210*i
    h+=f'''<div class="ph" style="left:{x}px;top:1300px;width:200px;height:240px;border-radius:12px"><img src="{ph((x,1300,x+200,1540))}"></div>
<div class="tg" style="left:{x+6}px;top:1306px;height:46px;padding:0 9px;background:{R};color:#fff;font-size:25px;line-height:46px;border-radius:7px">{i+1:02d}</div>
<div class="a" style="left:{x}px;top:1552px;font-size:23px;font-weight:700;line-height:36px;letter-spacing:-.4px;white-space:nowrap">{t}</div>'''
h+=f'''<div class="a" style="left:0;top:1662px;width:1080px;text-align:center;font-size:50px;font-weight:900;line-height:72px">ワンコの負担をおさえて、<br><span class="y">少ない動き</span>で安全に</div>
<div class="a" style="left:0;top:1830px;width:1080px;text-align:center;font-size:31px;font-weight:500;color:#cfc4ba;letter-spacing:1px">保存して、次のカットの前に見返してね</div>
</body></html>'''
open('t.html','w').write(h)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920},device_scale_factor=S)
    pg.goto('file://'+os.path.abspath('t.html')); pg.wait_for_timeout(400); pg.screenshot(path=f'out{S}.png'); b.close()
print('ok')
