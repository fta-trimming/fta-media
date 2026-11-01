# 11/2 藤原さん「今日のリールのプレゼントにくぼみの矢印が付いてない／ストーリーズの写真と同じようにしてほしい」
from PIL import Image,ImageDraw,ImageFont
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
Y=(242,208,107);D=(36,23,19);Wt=(255,255,255)
# ストーリーズと同じ点（リールの3.5秒のコマ 1080x1920 の座標）
EF=(679.7,825.4); KF=(640.7,1310.2)
S,OX,OY=0.66,-1,60   # コマ→プレゼントの画像（テンプレート合わせで求めた）
sc=1.75
o=Image.open('tejun.jpg').convert('RGB');d=ImageDraw.Draw(o)
e=(EF[0]*S+OX,EF[1]*S+OY);k=(KF[0]*S+OX,KF[1]*S+OY)
c=((e[0]+k[0])/2-38*sc,(e[1]+k[1])/2)
bz=lambda t:((1-t)**2*e[0]+2*(1-t)*t*c[0]+t*t*k[0],(1-t)**2*e[1]+2*(1-t)*t*c[1]+t*t*k[1])
pts=[bz(i/80) for i in range(81)]
for i in range(0,80,4):
  seg=(pts[i],pts[i+1],pts[min(i+2,80)]);d.line(seg,fill=(0,0,0),width=round(5.5*sc));d.line(seg,fill=Wt,width=round(3.6*sc))
for w,cc in ((round(8.3*sc),(0,0,0)),(round(6*sc),Y)):d.line((e,k),fill=cc,width=w)
r=10*sc
for p in (e,k):d.ellipse((p[0]-r,p[1]-r,p[0]+r,p[1]+r),fill=Y,outline=D,width=max(3,round(2.4*sc)))
def pill(xy,t,font,fg=Wt,sp=3,anchor='lm'):
  b=d.multiline_textbbox(xy,t,font=font,anchor=anchor,spacing=sp);d.rounded_rectangle((b[0]-6.5*sc,b[1]-5.3*sc,b[2]+6.5*sc,b[3]+5.3*sc),6*sc,fill=D);d.multiline_text(xy,t,font=font,fill=fg,anchor=anchor,spacing=sp);return b
f=ImageFont.truetype(F,round(18*sc))
print(pill((e[0]+20*sc,e[1]),'肘',f));print(pill((k[0]-6*sc,k[1]+18*sc),'手根球',f,anchor='mt'))
mn=min(pts,key=lambda p:p[0])[0]
print(pill((mn-16*sc,(e[1]+k[1])/2),'くぼみは\n刈らずに流す',ImageFont.truetype(F,round(16*sc)),fg=Y,anchor='rm'))
o.save('tejun_zenshi_v2.jpg',quality=93)
o.crop((40,380,1060,1200)).save('chk_gift.jpg')
