from PIL import Image,ImageDraw,ImageFont
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc';L='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
Y=(242,208,107,255);W=(255,255,255,255)
def lab(name,num,en,jp):
  im=Image.new('RGBA',(1080,1920),(0,0,0,0));d=ImageDraw.Draw(im)
  x,y=90,300
  d.rectangle((x,y,x+6,y+120),fill=Y)
  d.text((x+28,y-4),num,font=ImageFont.truetype(B,30),fill=Y)
  d.text((x+28,y+30),en,font=ImageFont.truetype(B,58),fill=W,stroke_width=2,stroke_fill=(0,0,0,110))
  d.text((x+30,y+100),jp,font=ImageFont.truetype(L,30),fill=W,stroke_width=2,stroke_fill=(0,0,0,110))
  im.save(name)
lab('l_before.png','','BEFORE','カット前')
lab('l_att.png','01','ATTACHMENT','アタッチメント')
lab('l_sci.png','02','SCISSORS','ハサミ')
lab('l_after.png','','AFTER','仕上がり')
# split labels
im=Image.new('RGBA',(1080,1920),(0,0,0,0));d=ImageDraw.Draw(im)
d.rectangle((538,0,542,1920),fill=W)
for x,t,c in [(90,'BEFORE',W),(630,'AFTER',Y)]:
  d.text((x,300),t,font=ImageFont.truetype(B,52),fill=c,stroke_width=2,stroke_fill=(0,0,0,120))
im.save('l_split.png')
lab('l_sciF.png','02','SCISSORS','ハサミ｜前側 上→下')
lab('l_sciB.png','03','SCISSORS','ハサミ｜後ろ側 上→下')
im=Image.new('RGBA',(1080,1920),(0,0,0,0));d=ImageDraw.Draw(im);f=ImageFont.truetype(B,52);fj=ImageFont.truetype(L,28)
for cx,t,j,c in [(270,'BEFORE','カット前',W),(810,'AFTER','仕上がり',Y)]:
  w=d.textlength(t,font=f);d.text((cx-w/2,385),t,font=f,fill=c)
  w=d.textlength(j,font=fj);d.text((cx-w/2,1475),j,font=fj,fill=W)
im.save('l_split2.png')
