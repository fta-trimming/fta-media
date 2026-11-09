import base64,io
from PIL import Image
from playwright.sync_api import sync_playwright
def b64(im,q=96):
    b=io.BytesIO(); im.save(b,'JPEG',quality=q); return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
BW,BH=470,591; SW,SH=164,238; S=2
# BEFORE/AFTER：元の大きさの止めたコマから切り出し、1回だけ lanczos で拡大
def crop1080(f,box):
    im=Image.open(f).convert('RGB'); x,y,w,h=[v/1.5 for v in box]
    return im.crop((round(x),round(y),round(x+w),round(y+h))).resize((BW*S,BH*S),Image.LANCZOS)
bc=(120,470,660,830); ac=(230,450,660,830)
B=crop1080('../v3/freeze720.png',bc); A=crop1080('../v3/a_10.png',ac)
def marks(M,o):
    ox,oy=o
    d='fill="none" stroke="#f6d77a" stroke-width="6" stroke-dasharray="18 12"'
    br,st,lp=M
    return (f'<rect x="{-br[2]/2}" y="-48" width="{br[2]}" height="96" rx="6" transform="translate({br[0]-ox},{br[1]-oy}) rotate({br[3]})" {d}/>'
            f'<circle cx="{st[0]-ox}" cy="{st[1]-oy}" r="52" {d}/>'
            f'<rect x="{lp[0]-ox}" y="{lp[1]-oy}" width="{lp[2]}" height="74" rx="8" {d}/>')
MB=((455,652,470,5),(452,768),(342,1008,180)); MA=((560,630,530,1.5),(560,742),(458,1030,184))
steps=[]
for k in range(1,7):
    im=Image.open(f'step{k}.png').convert('RGB').resize((SW*S,SH*S),Image.LANCZOS); steps.append(b64(im))
cap=[('目の上を','6mmで刈る'),('ストップを','2mmで刈る'),('リップは鼻の','幅で0.5mm'),('コームで','軽く引き出す'),('目にかかる毛を','毛流れで切る'),('鼻より前の毛を','毛流れで切る')]
st=''.join(f'<div class="st"><div class="ph"><img src="{steps[i]}"><b>{i+1:02d}</b></div><p>{a}<br>{c}</p></div>' for i,(a,c) in enumerate(cap))
html=f'''<html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;background:#231713;font-family:'Noto Sans CJK JP',sans-serif;color:#fff;overflow:hidden}}
.w{{padding:56px 56px 0}}
.ac{{font-size:28px;letter-spacing:3px;font-weight:700;color:#efe4d8}}
.tag{{display:inline-block;margin-top:12px;background:#c0503a;font-size:28px;font-weight:900;padding:6px 18px;border-radius:10px}}
h1{{font-size:76px;font-weight:900;line-height:1.2;margin-top:16px}} .y{{color:#f6d77a}}
.sub{{font-size:30px;font-weight:700;color:#d9cbbd;margin-top:10px}}
.ba{{position:relative;display:flex;gap:24px;margin-top:22px}}
.bx{{position:relative;width:{BW}px;height:{BH}px;border-radius:18px;overflow:hidden}}
.bx img{{width:100%;height:100%;display:block}} .bx svg{{position:absolute;inset:0}}
.bd{{position:absolute;left:14px;top:14px;font-weight:900;font-size:36px;padding:2px 16px;border-radius:10px}}
.pl{{position:absolute;left:{BW-14}px;top:{BH/2-38}px;width:76px;height:76px;border-radius:50%;background:#f6d77a;display:flex;align-items:center;justify-content:center}}
.pl i{{width:0;height:0;border-left:26px solid #231713;border-top:16px solid transparent;border-bottom:16px solid transparent;margin-left:8px}}
.mm{{text-align:center;white-space:nowrap;font-size:34px;font-weight:900;margin-top:26px}}
.sts{{display:flex;gap:8px;margin:26px -36px 0}}
.st{{width:{SW}px}} .st .ph{{position:relative;width:{SW}px;height:{SH}px;border-radius:12px;overflow:hidden}}
.st img{{width:100%;height:100%;display:block}}
.st b{{position:absolute;left:8px;top:8px;background:#c0503a;font-size:24px;padding:0 9px;border-radius:7px}}
.st p{{font-size:23px;font-weight:700;line-height:1.45;margin-top:10px}}
.end{{text-align:center;margin-top:44px}}
.end h2{{font-size:48px;font-weight:900;line-height:1.45}}
.end p{{font-size:32px;font-weight:700;color:#cfc2b5;margin-top:22px}}
</style></head><body><div class="w">
<div class="ac">CUT TECHNIQUE ／ @naohide_fujiwara</div>
<div class="tag">保存版・手順まとめ</div>
<h1>目の上と鼻周りで<br><span class="y">崩れにくい顔</span>になる</h1>
<div class="sub">顔カット（目周り・鼻周り）のバリカンとハサミ</div>
<div class="ba">
 <div class="bx"><img src="{b64(B)}"><svg viewBox="0 0 660 830" preserveAspectRatio="none">{marks(MB,bc[:2])}</svg><div class="bd" style="background:#fff;color:#231713">BEFORE</div></div>
 <div class="bx"><img src="{b64(A)}"><svg viewBox="0 0 660 830" preserveAspectRatio="none">{marks(MA,ac[:2])}</svg><div class="bd" style="background:#f6d77a;color:#231713">AFTER</div></div>
 <div class="pl"><i></i></div>
</div>
<div class="mm">バリカン　目の上<span class="y">6mm</span>・ストップ<span class="y">2mm</span>・リップ<span class="y">0.5mm</span></div>
<div class="sts">{st}</div>
<div class="end"><h2>目の上と鼻周りを整えると<br><span class="y">崩れにくいカット</span>になる</h2>
<p>ミリ数を決めたバリカンで、毎回同じ仕上がり</p><p style="margin-top:14px">保存して、次のカットの前に見返してね</p></div>
</div></body></html>'''
open('tejun.html','w').write(html)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920},device_scale_factor=S)
    pg.goto('file://'+__import__('os').path.abspath('tejun.html')); pg.wait_for_timeout(400)
    pg.screenshot(path='tejun_hq.png'); b.close()
im=Image.open('tejun_hq.png').convert('RGB'); im.save('tejun_kao.jpg',quality=95,subsampling=0)
print(im.size, __import__('os').path.getsize('tejun_kao.jpg'))
