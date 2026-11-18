import json
F="font-family='Noto Sans CJK JP' font-weight='700'"
G='#24402f'; Y='#f6d77a'; R='#e0412f'; LG='#3d7a55'; P='#eef5f0'
def svg(b): return f"<svg width='860' height='654' viewBox='0 0 920 700' xmlns='http://www.w3.org/2000/svg'>{b}</svg>"
def t(x,y,s,size=34,col=G,a='middle'): return f"<text x='{x}' y='{y}' {F} font-size='{size}' fill='{col}' text-anchor='{a}'>{s}</text>"
steps=['知る','気になる','確かめる','予約する']
def stairs(hl=None,stop=None):
    b=''
    for i,s in enumerate(steps):
        x=70+i*200; y=520-i*110; h=180+i*110
        fill=Y if hl==i else (P if stop!=i else '#fde3df')
        st=R if stop==i else LG
        b+=f"<rect x='{x}' y='{y}' width='190' height='{h}' rx='14' fill='{fill}' stroke='{st}' stroke-width='5'/>"+t(x+95,y+60,s,36)+t(x+95,y+110,str(i+1),40,LG)
    return b
ill={}
ill['steps']=svg(stairs()+t(460,80,'予約までの4つの段',44)+f"<path d='M120 470 Q 460 120 800 140' fill='none' stroke='{LG}' stroke-width='6' stroke-dasharray='16 12'/>")
# funnel
fb=''
for i,s in enumerate(steps):
    w=760-i*150; x=(920-w)/2; y=120+i*130
    fb+=f"<rect x='{x}' y='{y}' width='{w}' height='105' rx='18' fill='{P}' stroke='{LG}' stroke-width='5'/>"+t(460,y+68,s,40)
fb+=f"<circle cx='{820}' cy='{120+2*130+52}' r='46' fill='none' stroke='{R}' stroke-width='8'/>"+t(820,120+2*130+68,'？',48,R)
ill['funnel']=svg(t(460,80,'どこで止まっている？',44)+fb)
# example: seen but no booking
ill['stop']=svg(stairs(stop=2)+
  f"<g transform='translate(150,120)'><ellipse cx='60' cy='40' rx='70' ry='40' fill='#fff' stroke='{G}' stroke-width='6'/><circle cx='60' cy='40' r='20' fill='{G}'/></g>"+t(210,230,'見られている',34)
  +f"<g transform='translate(470,170)'><polygon points='40,0 80,0 110,30 110,70 80,100 40,100 10,70 10,30' fill='{R}'/>"+t(60,64,'止',44,'#fff')+"</g>")
# fix one
boxes=''
for i,s in enumerate(steps):
    x=40+i*215; c=Y if i==2 else P
    boxes+=f"<rect x='{x}' y='260' width='195' height='160' rx='20' fill='{c}' stroke='{G if i==2 else LG}' stroke-width='{8 if i==2 else 4}'/>"+t(x+97,355,s,34)
ill['one']=svg(t(460,120,'直すのは1つだけ',46)+boxes+t(567,520,'🔧 ここだけ直す',40,R)+f"<path d='M567 470 L567 430' stroke='{R}' stroke-width='6'/>")
# checklist
items=['4つの段を書き出す','止まっている段に印','1つだけ直して様子を見る']
cl=''.join(f"<rect x='90' y='{150+i*160}' width='740' height='130' rx='22' fill='{P}'/><rect x='120' y='{180+i*160}' width='70' height='70' rx='12' fill='#fff' stroke='{LG}' stroke-width='5'/>"+t(155,f'{232+i*160}','✓',54,LG)+t(230,f'{230+i*160}',s,40,G,'start') for i,s in enumerate(items))
ill['check']=svg(t(460,95,'やること',46)+cl)
# one path
ill['path']=svg(t(460,95,'止まっている段がわかれば',42)
  +f"<path d='M140 560 C 300 560, 360 300, 520 300 S 760 200, 800 170' fill='none' stroke='{LG}' stroke-width='16' stroke-linecap='round'/>"
  +f"<circle cx='140' cy='560' r='28' fill='{Y}' stroke='{G}' stroke-width='6'/><polygon points='780,140 840,160 790,205' fill='{LG}'/>"
  +f"<rect x='300' y='420' width='420' height='110' rx='55' fill='{G}'/>"+t(510,492,'やることは1つ',46,Y))
json.dump(ill,open('/tmp/ill/ill1121.json','w'),ensure_ascii=False)
open('/tmp/ill/prev1121.html','w').write("<html><body style='margin:0;background:#888;display:flex;flex-wrap:wrap;gap:10px'>"+"".join(f"<div style='background:#fffdf8;border-radius:20px'>{v}</div>" for v in ill.values())+"</body></html>")
