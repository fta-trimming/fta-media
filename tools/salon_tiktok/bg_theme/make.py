# テーマの背景の絵（1080x1920）。上の帯(0-290)と下(1400-1920)に主役を置く。人の顔なし。
import json
dog=open('/tmp/dog.svgfrag').read()
G='#24402f'; LG='#3d7a55'; Y='#f6d77a'; R='#e0412f'
def page(body,bg): return f"<html><body style='margin:0'><svg width='1080' height='1920' viewBox='0 0 1080 1920' xmlns='http://www.w3.org/2000/svg' style='display:block'><rect width='1080' height='1920' fill='{bg}'/>{body}</svg></body></html>"
F="font-family='Noto Sans CJK JP' font-weight='700'"
def t(x,y,s,size,col,a='middle',op=1): return f"<text x='{x}' y='{y}' {F} font-size='{size}' fill='{col}' text-anchor='{a}' opacity='{op}'>{s}</text>"
def phone(x,y,s,screen):
    return f"<g transform='translate({x},{y}) scale({s})'><rect x='0' y='0' width='330' height='660' rx='48' fill='#1f2a24'/><rect x='18' y='60' width='294' height='560' rx='18' fill='#fff'/><rect x='125' y='24' width='80' height='14' rx='7' fill='#3a463f'/>{screen}</g>"
def search_screen():
    s=f"<rect x='34' y='80' width='262' height='54' rx='27' fill='#eef2ef'/>"+t(160,116,'🔍 トリミング 近く',22,'#555')
    for i in range(3):
        y=160+i*140
        s+=f"<rect x='34' y='{y}' width='262' height='120' rx='14' fill='#f6f8f6' stroke='#dde6df'/><rect x='48' y='{y+16}' width='88' height='88' rx='10' fill='#e7d9c4'/><rect x='150' y='{y+22}' width='120' height='16' rx='8' fill='#c9d6cc'/><rect x='150' y='{y+50}' width='90' height='14' rx='7' fill='#dfe7e1'/>"+t(200,y+96,'★★★★☆',20,'#e3b341')
    return s
def booking_screen():
    s=t(165,110,'予約',28,G)
    for r in range(5):
        for c in range(7):
            x=40+c*36; y=140+r*48
            fill=(Y if (r,c) in [(2,3)] else '#eef2ef')
            s+=f"<rect x='{x}' y='{y}' width='30' height='40' rx='6' fill='{fill}'/>"
    s+=f"<rect x='50' y='420' width='230' height='70' rx='35' fill='{LG}'/>"+t(165,466,'予約する',28,'#fff')
    return s
def map_pins(x,y):
    s=f"<g transform='translate({x},{y})'><rect width='420' height='300' rx='30' fill='#e3ece5'/>"
    s+="".join(f"<path d='M{px} {py} c-22 -34 -34 -50 -34 -66 a34 34 0 1 1 68 0 c0 16 -12 32 -34 66z' fill='{c}'/><circle cx='{px}' cy='{py-66}' r='12' fill='#fff'/>" for px,py,c in [(110,200,R),(250,150,LG),(330,250,LG)])
    s+=f"<path d='M0 220 Q 200 120 420 200' stroke='#fff' stroke-width='18' fill='none'/></g>"
    return s
bgs={}
# 集客1：スマホで探す
bgs['search']=page(
  f"<circle cx='980' cy='160' r='220' fill='#dbe8de'/><circle cx='80' cy='1800' r='260' fill='#dbe8de'/>"
  +phone(90,1330,0.82,search_screen())+map_pins(560,1450)
  +"".join(f"<circle cx='{x}' cy='{y}' r='6' fill='{LG}' opacity='.35'/>" for x,y in [(200,120),(320,200),(460,90),(640,180),(820,260)]),
  '#f1f5f0')
# 集客2：予約
bgs['booking']=page(
  f"<circle cx='120' cy='150' r='200' fill='#f3e8c9'/><circle cx='1000' cy='1750' r='260' fill='#f3e8c9'/>"
  +phone(620,1300,0.86,booking_screen())
  +f"<g transform='translate(90,1440)'><rect width='420' height='360' rx='26' fill='#fff' stroke='#e6dcc2' stroke-width='4'/><rect width='420' height='80' rx='26' fill='{LG}'/>"+t(210,55,'11月',38,'#fff')
  +"".join(f"<rect x='{30+c*55}' y='{110+r*58}' width='44' height='44' rx='8' fill='{'#f6d77a' if (r,c) in [(1,2),(3,4)] else '#f2f4f2'}'/>" for r in range(4) for c in range(7))+"</g>",
  '#fbf7ec')
# 育成1：トリミング台と道具（ワンコの絵）
bgs['table']=page(
  f"<rect x='0' y='1580' width='1080' height='340' fill='#cfd9d1'/><rect x='120' y='1540' width='840' height='60' rx='14' fill='#8aa595'/>"
  +f"<g transform='translate(330,1090) scale(0.95)'>{dog}</g>"
  +f"<g transform='translate(820,1300) rotate(25)'><circle cx='0' cy='0' r='26' fill='none' stroke='#555' stroke-width='10'/><circle cx='0' cy='70' r='26' fill='none' stroke='#555' stroke-width='10'/><line x1='14' y1='20' x2='130' y2='-110' stroke='#777' stroke-width='12'/><line x1='14' y1='50' x2='130' y2='170' stroke='#777' stroke-width='12' opacity='0'/></g>"
  +f"<g transform='translate(120,1330) rotate(-15)'><rect width='80' height='230' rx='34' fill='#2b2b2b'/><rect x='12' y='40' width='56' height='18' rx='8' fill='#9be15d'/><rect x='-10' y='-46' width='100' height='60' rx='10' fill='#ccc'/></g>"
  +f"<circle cx='160' cy='170' r='200' fill='#dbe8de'/><circle cx='960' cy='120' r='150' fill='#e9f1eb'/>",
  '#f1f5f0')
# 育成2：練習ノート
bgs['note']=page(
  f"<circle cx='940' cy='170' r='220' fill='#f3e8c9'/>"
  +f"<g transform='translate(110,1360) rotate(-4)'><rect width='640' height='470' rx='20' fill='#fff' stroke='#e2d6b8' stroke-width='5'/>"
  +"".join(f"<line x1='40' y1='{90+i*60}' x2='600' y2='{90+i*60}' stroke='#e8eef0' stroke-width='4'/>" for i in range(7))
  +t(60,80,'練習ノート',38,G,'start')+t(60,170,'① 後ろ側　◯mm',32,LG,'start')+t(60,230,'② 前側　　◯mm',32,LG,'start')+t(60,290,'③ 側面　　◯mm',32,LG,'start')+t(60,350,'④ 仕上げ　ハサミ',32,R,'start')+"</g>"
  +f"<g transform='translate(820,1380) rotate(30)'><rect width='34' height='360' rx='8' fill='#e3b341'/><polygon points='0,360 34,360 17,410' fill='#c9a640'/></g>",
  '#fbf7ec')
# 育成3：時計とチェック（負担・時間）
bgs['clock']=page(
  f"<circle cx='150' cy='160' r='190' fill='#dbe8de'/>"
  +f"<g transform='translate(300,1680)'><circle r='210' fill='#fff' stroke='{LG}' stroke-width='14'/>"+"".join(f"<line x1='0' y1='-180' x2='0' y2='-155' stroke='{G}' stroke-width='8' transform='rotate({i*30})'/>" for i in range(12))+f"<line x1='0' y1='0' x2='0' y2='-120' stroke='{G}' stroke-width='12' stroke-linecap='round'/><line x1='0' y1='0' x2='90' y2='0' stroke='{G}' stroke-width='12' stroke-linecap='round'/><circle r='14' fill='{G}'/></g>"
  +f"<g transform='translate(620,1500)'><rect width='360' height='330' rx='26' fill='#fff' stroke='#dde6df' stroke-width='5'/>"+"".join(f"<rect x='30' y='{40+i*95}' width='56' height='56' rx='10' fill='#eef5f0' stroke='{LG}' stroke-width='4'/>"+t(58,f'{84+i*95}','✓',44,LG)+f"<rect x='110' y='{58+i*95}' width='200' height='20' rx='10' fill='#dfe7e1'/>" for i in range(3))+"</g>",
  '#f1f5f0')
for k,v in bgs.items(): open(f'/tmp/bg/{k}.html','w').write(v)
print(list(bgs))
