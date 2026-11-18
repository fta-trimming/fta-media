import json
dog=open('/tmp/dog.svgfrag').read()
F="font-family='Noto Sans CJK JP' font-weight='700'"
G='#24402f'; Y='#f6d77a'; R='#e0412f'; LG='#3d7a55'
def svg(body,vb="0 0 920 700"): return f"<svg width='860' height='654' viewBox='{vb}' xmlns='http://www.w3.org/2000/svg'>{body}</svg>"
def D(x,y,s): return f"<g transform='translate({x},{y}) scale({s})'>{dog}</g>"
def t(x,y,txt,size=34,col=G,anchor='middle'): return f"<text x='{x}' y='{y}' {F} font-size='{size}' fill='{col}' text-anchor='{anchor}'>{txt}</text>"
ill={}
# 新人：1か所だけ見る
ill['shinjin']=svg(D(150,40,1.05)+
 "<circle cx='392' cy='594' r='62' fill='none' stroke='#e0412f' stroke-width='9'/>"
 "<circle cx='640' cy='300' r='80' fill='rgba(255,255,255,.6)' stroke='#555' stroke-width='12'/><line x1='698' y1='358' x2='770' y2='430' stroke='#555' stroke-width='22' stroke-linecap='round'/>"
 "<path d='M600 380 Q 500 470 440 560' fill='none' stroke='#e0412f' stroke-width='6' stroke-dasharray='14 10'/>"
 +t(460,70,'ここを、どう切ろう…',40,R))
# ベテラン：つながり・左右・奥行き
pts=[(392,594),(320,420),(600,580),(520,330)]
lines="".join(f"<line x1='{a[0]}' y1='{a[1]}' x2='{b[0]}' y2='{b[1]}' stroke='{LG}' stroke-width='7' stroke-dasharray='16 10'/>" for a,b in zip(pts,pts[1:]))
dots="".join(f"<circle cx='{x}' cy='{y}' r='26' fill='{Y}' stroke='{G}' stroke-width='5'/>"+t(x,y+12,str(i+1),32) for i,(x,y) in enumerate(pts))
ill['veteran']=svg(D(150,40,1.05)+lines+dots+
 f"<rect x='610' y='60' width='280' height='200' rx='20' fill='#eef5f0'/>"+t(750,115,'つながり',38)+t(750,170,'左右のバランス',36)+t(750,225,'奥行き',38))
# 保存されていない：グラフ
ill['hozon']=svg(
 "<line x1='110' y1='590' x2='860' y2='590' stroke='#888' stroke-width='4'/><line x1='110' y1='590' x2='110' y2='110' stroke='#888' stroke-width='4'/>"
 +t(485,650,'時間がたつ →',34,'#666')+t(60,350,'できる',30,'#666')
 +f"<path d='M120 560 C 220 200, 300 160, 380 180 S 600 470, 840 520' fill='none' stroke='{R}' stroke-width='10'/>"
 +f"<path d='M120 560 C 220 220, 300 190, 380 190 L 840 170' fill='none' stroke='{LG}' stroke-width='10'/>"
 +f"<circle cx='380' cy='185' r='16' fill='{Y}' stroke='{G}' stroke-width='4'/>"+t(380,140,'練習した日',32)
 +t(760,140,'保存できた',36,LG)+t(740,480,'保存なし',36,R))
# アタッチメントで保存：表
rows=[('①','後ろ側','◯mm'),('②','前側','◯mm'),('③','側面','◯mm'),('④','仕上げ','ハサミ')]
tb="".join(f"<rect x='330' y='{150+i*110}' width='540' height='94' rx='14' fill='{'#eef5f0' if i%2==0 else '#ffffff'}' stroke='#cfe0d4' stroke-width='3'/>"+t(380,f'{210+i*110}',a,40,G)+t(560,f'{210+i*110}',b,38,G)+t(780,f'{210+i*110}',c,38,R if c=='ハサミ' else LG) for i,(a,b,c) in enumerate(rows))
ill['att']=svg(
 # clipper icon
 f"<g transform='translate(60,170) rotate(-20)'><rect x='0' y='0' width='120' height='330' rx='50' fill='#2b2b2b'/><rect x='18' y='60' width='84' height='26' rx='10' fill='#9be15d'/><rect x='-20' y='-70' width='160' height='90' rx='16' fill='#d0d0d0' stroke='#888' stroke-width='4'/>"
 +"".join(f"<line x1='{-10+k*16}' y1='-70' x2='{-10+k*16}' y2='-120' stroke='#888' stroke-width='6'/>" for k in range(10))+"</g>"
 +t(600,110,'刈る順番とミリ数を「残す」',38)+tb)
# 教え方：考え方＋練習
ill['oshie']=svg(
 f"<rect x='60' y='190' width='300' height='220' rx='30' fill='#eef5f0' stroke='{LG}' stroke-width='6'/>"+t(210,280,'💡',70)+t(210,370,'考え方',48)
 +t(445,330,'＋',90,G)
 +f"<rect x='530' y='190' width='300' height='220' rx='30' fill='#fff7dc' stroke='#d9b440' stroke-width='6'/>"+t(680,280,'✂',70)+t(680,370,'練習',48)
 +f"<path d='M445 450 L445 520' stroke='{G}' stroke-width='10' marker-end='url(#a)'/><defs><marker id='a' markerWidth='6' markerHeight='6' refX='3' refY='3' orient='auto'><path d='M0 0 L6 3 L0 6z' fill='{G}'/></marker></defs>"
 +f"<rect x='250' y='560' width='390' height='100' rx='50' fill='{G}'/>"+t(445,627,'身につく',48,Y))
# 負担が軽く：迷う時間のバー
ill['futan']=svg(
 t(460,90,'迷う時間',44)
 +t(150,220,'今まで',34,'#666','start')+f"<rect x='300' y='180' width='560' height='60' rx='30' fill='{R}'/>"
 +t(150,350,'これから',34,'#666','start')+f"<rect x='300' y='310' width='200' height='60' rx='30' fill='{LG}'/>"
 +f"<rect x='90' y='450' width='350' height='170' rx='26' fill='#eef5f0'/>"+t(265,520,'新人さん',38)+t(265,585,'気持ちが軽い',36,LG)
 +f"<rect x='480' y='450' width='350' height='170' rx='26' fill='#eef5f0'/>"+t(655,520,'教える人',38)+t(655,585,'負担が減る',36,LG))
json.dump(ill,open('/tmp/ill/ill.json','w'),ensure_ascii=False)
page="<html><body style='margin:0;background:#888;display:flex;flex-wrap:wrap;gap:10px'>"+"".join(f"<div style='background:#fffdf8;border-radius:20px'>{v}</div>" for v in ill.values())+"</body></html>"
open('/tmp/ill/prev.html','w').write(page)
