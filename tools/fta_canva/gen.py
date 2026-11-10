import json
Y=lambda s:f"<span class='y'>{s}</span>"
G=lambda s:f"<span class='g'>{s}</span>"
def car(n,tag,h,art,ah=600,note=None,cmp=None,lst=None,band=None,small=None,tagc='',out=None,aimg_top=420,extra=None):
  b=[{'t':'tag','v':tag,'c':tagc,'s':{'top':120}},{'t':'h','v':h,'s':{'top':190}}]
  if art: b.append({'t':'art','v':art,'s':{'top':aimg_top,'height':ah}})
  y=aimg_top+ah+30
  if cmp: b.append({'t':'cmp','x':cmp[0],'o':cmp[1],'s':{'top':y}}); y+=230
  if lst: b.append({'t':'list','v':lst,'s':{'top':y}}); y+=len(lst)*100
  if note: b.append({'t':'note','v':note,'s':{'bottom':120}})
  if band: b.append({'t':'band','v':band,'s':{'bottom':150}})
  if small: b.append({'t':'small','v':small,'s':{'bottom':100}})
  if extra: b+=extra
  return {'w':1080,'h':1350,'pn':f'{n} / 8','dots':n,'blocks':b,'out':out}
def single(tag,h,art,note,out,ah=640,tagc='',cmp=None):
  b=[{'t':'tag','v':tag,'c':tagc,'s':{'top':120}},{'t':'h','v':h,'s':{'top':190}},{'t':'art','v':art,'s':{'top':420,'height':ah}}]
  if cmp:b.append({'t':'cmp','x':cmp[0],'o':cmp[1],'s':{'top':420+ah+30}})
  b.append({'t':'note','v':note,'s':{'bottom':100}})
  return {'w':1080,'h':1350,'pn':'','blocks':b,'out':out}
def story(tag,h,art,out,note=None,cmp=None,lst=None,band='保存して見返してね',big=None,ah=440,tagc='',small=None,artTop=600):
  b=[{'t':'tag','v':tag,'c':tagc,'s':{'top':260}},{'t':'h','v':h,'s':{'top':330,'font-size':80}}]
  y=artTop
  if art: b.append({'t':'art','v':art,'s':{'top':y,'height':ah}}); y+=ah+30
  if big: b.append({'t':'big','v':big,'s':{'top':y,'font-size':60,'line-height':'1.35'}}); y+=190
  if cmp: b.append({'t':'cmp','x':cmp[0],'o':cmp[1],'s':{'top':y}}); y+=250
  if lst: b.append({'t':'list','v':lst,'s':{'top':y}}); y+=len(lst)*100
  if note: b.append({'t':'note','v':note,'s':{'top':y}}); y+=170
  if band: b.append({'t':'band','v':band,'s':{'top':1560}})
  if small: b.append({'t':'small','v':small,'s':{'top':1540}})
  return {'w':1080,'h':1920,'topY':200,'pn':'','blocks':b,'out':out}
I=[]
# carousel 1 (11/10)
I+= [car(1,'新人さんを教える方へ',f'新人に時間がかかるのは、<br>技術不足より{Y("「順番」")}','k13.png',note=f'原因は「荒刈り」。{G("ミリ数で形を先に作る")}',tagc='yl',out='c1_1.png'),
 car(2,'原因',f'時間がかかるのは、<br>{Y("荒刈りで形を探すこと")}','k9.png',ah=560,note='形のイメージがまだ少ない → 少しずつ切り進める → 形が出るまで時間がかかる',out='c1_2.png'),
 car(3,'くらべる',f'形は、<br>{Y("先に作れる")}','k3.png',ah=470,cmp=['少しずつ切って<br>形を探す','ミリ数を決めて<br>一気に荒刈り'],out='c1_3.png'),
 car(4,'伝え方',f'「このくらい」ではなく、<br>{Y("番号で")}','k4.png',ah=480,note='迷う時間が減る。教える言葉がそろう。手直しが減る。',out='c1_4.png'),
 car(5,'新人さんへの声かけ',f'ミリ数と順番で、<br>{Y("渡す")}','k14.png',ah=420,cmp=['「このくらい<br>残して」','「後肢は19mmで、<br>上から下へ」（例）'],out='c1_5.png'),
 car(6,'時間',f'急がなくても、<br>{Y("時間は空く")}','k5.png',ah=520,note='1頭180分→160分（例）なら、3頭で1時間',out='c1_6.png'),
 car(7,'すぐできること',f'明日からできる<br>{Y("3つ")}','k8.png',ah=260,lst=['よく来る犬種を1つ決める','部位ごとのミリ数と順番を1枚に書く','新人さんには、ミリ数で伝える'],small='くわしい手順はプロフィールのリンクから（note）',out='c1_7.png'),
 car(8,'🎁 プレゼント',f'荒刈りミリ数チェック表<br>{Y("＋スタートキット")}','gift1.jpg',ah=520,tagc='yl',band='コメントで「やってみる」→ DMでお送りします<br><span style="font-size:28px">（登録・ログイン不要）</span>',out='c1_8.png')]
# carousel 2 (11/15)
I+= [car(1,'一人サロンの方へ',f'一人サロンこそ、<br>{Y("ミリ数を書いておく")}','k10.png',note='「このくらい」は、その日の調子で変わります',tagc='yl',out='c2_1.png'),
 car(2,'一人サロンは',f'自分の時間が、<br>{Y("売り上げの上限")}','k11.png',note='だからこそ、迷う時間を先に消しておく',out='c2_2.png'),
 car(3,'くらべる',f'疲れている日も、<br>{Y("同じ形で")}','k2.png',ah=470,cmp=['「いつもの<br>感じで」','「背中は◯mm、<br>後肢は◯mm」'],out='c2_3.png'),
 car(4,'メモする',f'よく来る犬種を<br>{Y("3つだけ")}','k3.png',ah=520,note='部位ごとのミリ数と、刈る順番をメモ。カルテのすみでも、スマホのメモでも大丈夫',out='c2_4.png'),
 car(5,'分ける',f'形はアタッチメント、<br>{Y("ハサミは仕上げだけ")}','k1.png',ah=560,note='迷う時間が、いちばん減ります',out='c2_5.png'),
 car(6,'空いた時間',f'使い道も、<br>{Y("先に決めておく")}','k12.png',ah=330,lst=['予約を1つ増やす','お迎えの説明に使う','お店の準備に使う'],out='c2_6.png'),
 car(7,'すぐできること',f'明日からできる<br>{Y("3つ")}','k6.png',ah=260,lst=['よく来る犬種を3つ書く','部位ごとのミリ数と順番をメモ','1週間、荒刈りの時間を測る'],small='くわしい手順はプロフィールのリンクから（note）',out='c2_7.png'),
 car(8,'🎁 プレゼント',f'一人サロン ミリ数メモ<br>{Y("＋スタートキット")}','gift2.jpg',ah=520,tagc='yl',band='コメントで「やってみる」→ DMでお送りします<br><span style="font-size:28px">（登録・ログイン不要）</span>',out='c2_8.png')]
# stories
I+= [story('伝え方',f'「このくらい」は、<br>{Y("伝わらない")}','k14.png','s_d2.jpg',cmp=['「このくらい<br>残して」','「後肢は19mmで、<br>上から下へ」（例）'],note='番号で伝えると、迷わない'),
 story('ふりかえり',f'終わりどころを、<br>{Y("先に決める")}','k5.png','s_d3.jpg',cmp=['「全部、<br>完璧に」','「ここまでで<br>完成」'],note='時間が長くなるのは、技術ではなくゴールが無いから'),
 story('急がなくていい',f'1頭20分<br>{Y("早く終わると")}','k11.png','s_d4.jpg',ah=420,big='180分 → 160分（例）<br><b>3頭で1時間</b>',note='手を速くしなくても、時間は空く'),
 story('今日からできる',f'ミリ数の表は、<br>{Y("1枚でいい")}','k3.png','s_d5.jpg',note='よく来る犬種を1つ。①背中 ②後肢 ③前肢のミリ数（◯mm）と、刈る順番を書くだけ'),
 story('今日の有料note（やってみる編）',f'荒刈りを任せられる<br>{Y("新人に。")}','k13.png','s_link.jpg',ah=420,note='ミリ数で形を先に作る実践ノート<br><span style="font-size:30px">読むと分かること：よく来る犬種の「ミリ数の表」の作り方と、新人さんへの渡し方</span>',band='1,480円　▼下のリンクから読めます▼',tagc='yl'),
 story('ふりかえり',f'ウリは「得」の言葉に<br>{Y("言いかえる")}','k2.png','s_d6.jpg',ah=400,cmp=['「良いシャンプーを<br>使っています」','「フケ・かゆみ・赤みが気になる子に、皮膚に合わせて洗い方を変えます」']),
 story('今週のまとめ',f'明日からできる<br>{Y("3つ")}','k8.png','s_d7.jpg',ah=380,lst=['よく来る犬種を1つ決める','部位ごとのミリ数と刈る順番を書く','「このくらい」ではなくミリ数で伝える'])]
# threads
I+= [single('一人サロンの方へ',f'「このくらい」は、<br>{Y("明日の自分にも伝わらない")}','k9.png','よく来る犬種3つだけ、ミリ数と順番をメモしておく','t1.jpg',ah=580),
 single('明日、有料noteで全部',f'荒刈りは、<br>{Y("急がなくても縮む")}','k6.png','縮めるのは手の速さではなく、形を探す時間','t4.jpg',ah=580,tagc='yl'),
 single('有料note公開',f'荒刈りを任せられる新人は、<br>{Y("ミリ数で育つ")}','k10.png','荒刈りを任せられる新人に。ミリ数で形を先に作る実践ノート（1,480円）','t5.jpg',ah=560,tagc='yl'),
 single('一人サロンの方へ',f'時短は、ハサミを<br>{Y("速くすることじゃない")}','k1.png','形はアタッチメントで先に作る。ハサミは仕上げにだけ。','t2.jpg',ah=580)]
R=[dict(x,dots=None,out='r'+x['out']) for x in I if x['out'].startswith('c1_')]
I+=R
json.dump(I,open('items.json','w'),ensure_ascii=False)
print(len(I))
