import json
dog=open('/tmp/dog.svgfrag').read()
F="font-family='Noto Sans CJK JP' font-weight='700'"
G='#24402f'; Y='#f6d77a'; R='#e0412f'; LG='#3d7a55'; P='#eef5f0'
def svg(b): return f"<svg width='860' height='654' viewBox='0 0 920 700' xmlns='http://www.w3.org/2000/svg'>{b}</svg>"
def t(x,y,s,size=34,col=G,a='middle'): return f"<text x='{x}' y='{y}' {F} font-size='{size}' fill='{col}' text-anchor='{a}'>{s}</text>"
def D(x,y,s,extra=''): return f"<g transform='translate({x},{y}) scale({s})' {extra}>{dog}</g>"
ill={}
# 1 時間の棒：540分 vs 480分
seg=lambda x,w,c,l: f"<rect x='{x}' y='0' width='{w}' height='90' rx='12' fill='{c}' stroke='#fff' stroke-width='4'/>"+t(x+w/2,58,l,34,'#fff')
W=700/540
bar="".join(seg(110+i*180*W,180*W,LG,'180分') for i in range(3))
ill['over']=svg(t(460,90,'1日の施術時間（例）',42)
  +f"<g transform='translate(0,220)'>{bar}</g>"
  +f"<line x1='{110+480*W}' y1='170' x2='{110+480*W}' y2='360' stroke='{R}' stroke-width='8' stroke-dasharray='14 10'/>"
  +t(110+480*W,160,'480分',34,R)
  +f"<rect x='{110+480*W}' y='220' width='{60*W}' height='90' fill='{R}' opacity='.55'/>"
  +t(460,450,'3頭で540分 → 60分オーバー',42,R)
  +t(460,540,'この60分が、毎日の残業に',36,G))
# 2 ハサミでバラバラ：形の違う3頭＋時計
ill['bara']=svg(t(460,80,'ハサミだけで作ると…',42)
  +D(20,90,0.48)+D(320,110,0.42,"")+f"<g transform='translate(620,100) scale(0.46)'><g transform='scale(1.15,0.9)'>{dog}</g></g>"
  +t(150,450,'Aさん',40,LG)+t(460,450,'Bさん',40,R)+t(770,450,'Cさん',40,'#c98a1b')
  +t(460,560,'人によって、時間も形もバラバラ',38,R))
# 3 90%
import math
def arc(p):
    a=2*math.pi*p-math.pi/2; return 260+200*math.cos(a), 360+200*math.sin(a)
x,y=arc(0.9)
ill['pct']=svg(t(460,80,'形の作り方',42)
  +f"<circle cx='260' cy='360' r='200' fill='{Y}'/><path d='M260 360 L260 160 A200 200 0 1 1 {x:.1f} {y:.1f} Z' fill='{LG}'/>"
  +t(240,370,'90%',72,'#fff')
  +f"<rect x='520' y='230' width='50' height='50' rx='10' fill='{LG}'/>"+t(590,268,'アタッチメント',38,G,'start')
  +f"<rect x='520' y='330' width='50' height='50' rx='10' fill='{Y}'/>"+t(590,368,'ハサミ（仕上げ）',38,G,'start')
  +t(700,480,'10%',44,'#c9a640'))
# 4 同じ形・同じ時間
rows=[('①','後ろ側','◯mm'),('②','前側','◯mm'),('③','側面','◯mm')]
tb="".join(f"<rect x='40' y='{120+i*80}' width='360' height='66' rx='12' fill='{P}'/>"+t(80,f'{165+i*80}',a,32)+t(210,f'{165+i*80}',b,32)+t(340,f'{165+i*80}',c,32,LG) for i,(a,b,c) in enumerate(rows))
ill['same']=svg(t(460,80,'ミリ数と順番を決めると',42)+tb
  +t(220,440,'決めた表',32,'#666')
  +f"<path d='M420 250 L480 250' stroke='{G}' stroke-width='10'/><polygon points='480,230 510,250 480,270' fill='{G}'/>"
  +D(520,110,0.36)+D(700,110,0.36)
  +t(600,430,'160分',36,LG)+t(780,430,'160分',36,LG)+t(690,520,'誰が刈っても同じ',40,G))
# 5 480ぴったり
W2=700/480
bar2="".join(seg(110+i*160*W2,160*W2,LG,'160分') for i in range(3))
ill['fit']=svg(t(460,90,'1頭を20分短くすると（例）',42)
  +f"<g transform='translate(0,220)'>{bar2}</g>"
  +f"<line x1='{110+480*W2}' y1='170' x2='{110+480*W2}' y2='360' stroke='{LG}' stroke-width='8' stroke-dasharray='14 10'/>"
  +t(110+480*W2-10,160,'480分',34,LG,'end')
  +t(460,450,'3頭でぴったり480分',44,LG)+t(460,540,'残業なしで終われる',38,G))
# 6 定時に帰れる
ill['home']=svg(f"<g transform='translate(230,330)'><circle r='210' fill='#fff' stroke='{LG}' stroke-width='14'/>"
  +"".join(f"<line x1='0' y1='-180' x2='0' y2='-155' stroke='{G}' stroke-width='8' transform='rotate({i*30})'/>" for i in range(12))
  +f"<line x1='0' y1='0' x2='0' y2='-130' stroke='{G}' stroke-width='12' stroke-linecap='round'/><line x1='0' y1='0' x2='0' y2='95' stroke='{G}' stroke-width='12' stroke-linecap='round' transform='rotate(0)'/><circle r='14' fill='{G}'/></g>"
  +t(230,600,'定時',44,LG)
  +f"<rect x='500' y='150' width='360' height='150' rx='24' fill='{P}'/>"+t(680,215,'体の負担',38)+t(680,270,'↓ 軽く',38,LG)
  +f"<rect x='500' y='350' width='360' height='150' rx='24' fill='{P}'/>"+t(680,415,'気持ちの負担',38)+t(680,470,'↓ 軽く',38,LG))
# 7 プレゼント：チェック表
items=['1ページ：○×チェック','2ページ：何分こえている？','3ページ：終わる時刻']
ill['gift']=svg(f"<rect x='200' y='60' width='520' height='600' rx='20' fill='#fff' stroke='#d9c9a3' stroke-width='6'/>"
  +f"<rect x='200' y='60' width='520' height='100' rx='20' fill='{G}'/>"+t(460,125,'残業ゼロの時間チェック表',36,Y)
  +"".join(f"<rect x='240' y='{200+i*140}' width='440' height='110' rx='16' fill='{P}'/>"+t(460,f'{265+i*140}',s,32) for i,s in enumerate(items)))
json.dump(ill,open('/tmp/ill/illz.json','w'),ensure_ascii=False)
open('/tmp/ill/prevz.html','w').write("<html><body style='margin:0;background:#888;display:flex;flex-wrap:wrap;gap:10px'>"+"".join(f"<div style='background:#fffdf8;border-radius:20px'>{v}</div>" for v in ill.values())+"</body></html>")
