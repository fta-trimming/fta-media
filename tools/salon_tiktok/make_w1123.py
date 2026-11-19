# 11/23 の週の生産性リール（インパクト版 v2：40〜43秒・7場面・テーマの背景の絵・イラスト・動きなし）の設定を作る。
# 使い方: python3 make_w1123.py → 2026-11-2X_fta_w1123.json を6つ書く → python3 build_fta.py <名前>
import json, os, base64, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
dog = open(os.path.join(HERE, 'dog_frag.svg')).read()
F = "font-family='Noto Sans CJK JP' font-weight='700'"
G = '#24402f'; Y = '#f6d77a'; R = '#e0412f'; LG = '#3d7a55'; GR = '#666'
def svg(b): return f"<svg width='860' height='654' viewBox='0 0 920 700' xmlns='http://www.w3.org/2000/svg'>{b}</svg>"
def t(x, y, s, size=38, col=G, a='middle'): return f"<text x='{x}' y='{y}' {F} font-size='{size}' fill='{col}' text-anchor='{a}'>{s}</text>"
def D(x, y, s): return f"<g transform='translate({x},{y}) scale({s})'>{dog}</g>"
def box(x, y, w, h, fill='#eef5f0', stroke='none', sw=0, r=24): return f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{r}' fill='{fill}' stroke='{stroke}' stroke-width='{sw}'/>"
def arrow(x1, y1, x2, y2, col=G, w=10): return f"<defs><marker id='m{x1}{y1}' markerWidth='5' markerHeight='5' refX='2.5' refY='2.5' orient='auto'><path d='M0 0 L5 2.5 L0 5z' fill='{col}'/></marker></defs><line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}' marker-end='url(#m{x1}{y1})'/>"
def bar(x, y, w, col, label, val=''): return t(x - 20, y + 42, label, 34, GR, 'end') + box(x, y, w, 60, col, r=30) + (t(x + w + 16, y + 44, val, 36, col, 'start') if val else '')
def bubble(x, y, w, h, s, size=36, col=G, fill='#fff', stroke=LG):
    return box(x, y, w, h, fill, stroke, 5, 30) + f"<polygon points='{x+60},{y+h} {x+100},{y+h} {x+50},{y+h+40}' fill='{fill}' stroke='{stroke}' stroke-width='5'/><rect x='{x+55}' y='{y+h-6}' width='50' height='10' fill='{fill}'/>" + t(x + w / 2, y + h / 2 + size * .36, s, size, col)
def clipper(x, y, rot=-20, s=1):
    return (f"<g transform='translate({x},{y}) rotate({rot}) scale({s})'><rect x='0' y='0' width='120' height='330' rx='50' fill='#2b2b2b'/><rect x='18' y='60' width='84' height='26' rx='10' fill='#9be15d'/>"
            f"<rect x='-20' y='-70' width='160' height='90' rx='16' fill='#d0d0d0' stroke='#888' stroke-width='4'/>" + "".join(f"<line x1='{-10+k*16}' y1='-70' x2='{-10+k*16}' y2='-120' stroke='#888' stroke-width='6'/>" for k in range(10)) + "</g>")
def dryer(x, y, s=1):
    return (f"<g transform='translate({x},{y}) scale({s})'><rect x='0' y='0' width='220' height='110' rx='50' fill='#4b6b8a'/><rect x='200' y='25' width='90' height='60' rx='14' fill='#3a556e'/>"
            f"<rect x='40' y='100' width='60' height='170' rx='22' fill='#4b6b8a'/>" + "".join(f"<path d='M{300+k*0} {40+k*18} q 40 -12 80 0 t 80 0' fill='none' stroke='#9cc3e6' stroke-width='8' stroke-linecap='round'/>" for k in range(3)) + "</g>")
def brush(x, y, s=1):
    return (f"<g transform='translate({x},{y}) scale({s})'><rect x='0' y='0' width='170' height='120' rx='20' fill='#e9e3d6' stroke='#b9ae96' stroke-width='5'/>" + "".join(f"<line x1='{18+i*20}' y1='{120}' x2='{18+i*20}' y2='150' stroke='#999' stroke-width='5'/>" for i in range(8)) + f"<rect x='60' y='-160' width='50' height='170' rx='20' fill='#c25b3c'/></g>")
def hair(x, y, ok=True):
    # 毛の断面（根元〜先）。ok=根元からまっすぐ、ng=根元が縮れたまま
    c = LG if ok else R; out = f"<g transform='translate({x},{y})'><rect x='-130' y='170' width='260' height='30' fill='#e7d9c4'/>"
    for i in range(5):
        x0 = -90 + i * 45
        out += (f"<line x1='{x0}' y1='170' x2='{x0}' y2='0' stroke='{c}' stroke-width='9' stroke-linecap='round'/>" if ok else
                f"<path d='M{x0} 170 q 18 -20 0 -40 q -18 -20 0 -40 q 18 -20 0 -40' fill='none' stroke='{c}' stroke-width='9' stroke-linecap='round'/>")
    return out + "</g>"
B = lambda k: {'kind': 'image', 'file': os.path.join(HERE, 'bg_theme', f'{k}.png'), 'zoom': 0}

def gift_illus(date, fname):
    d = os.path.join(ROOT, 'gift', date); out = []
    for i in (3, 2, 1):
        sm = os.path.join(HERE, f'_g{date}_{i}.jpg')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(d, f'kit_{i}.jpg'), '-vf', 'scale=840:-1:flags=lanczos', '-q:v', '2', sm], check=True)
        out.append(base64.b64encode(open(sm, 'rb').read()).decode()); os.remove(sm)
    imgs = ''.join(f"<img src='data:image/jpeg;base64,{b}' style='position:absolute;height:600px;left:{330+o*70}px;top:{40+o*10}px;transform:rotate({r}deg);box-shadow:0 8px 24px rgba(0,0,0,.25);border-radius:6px'>" for b, o, r in zip(out, (2, 1, 0), (6, 3, -2)))
    return f"<div style='position:relative;width:920px;height:668px'>{imgs}<div style='position:absolute;left:20px;top:170px;font-family:Noto Sans CJK JP;font-weight:900;font-size:120px'>🎁</div><div style='position:absolute;left:10px;top:330px;width:320px;text-align:center;font-family:Noto Sans CJK JP;font-weight:700;font-size:40px;color:{G};line-height:1.4'>A4・3ページ<br><span style='background:{Y};padding:0 10px;border-radius:8px'>DMでお届け</span></div></div>"

def title(top, big, red, voice, bg, bigsize=132):
    html = (f"<div style='font-family:Noto Sans CJK JP;font-size:72px;font-weight:900;color:#fff;-webkit-text-stroke:3px #000;paint-order:stroke'>{top}</div>"
            f"<div style='font-family:Noto Sans CJK JP;font-size:{bigsize}px;font-weight:900;line-height:1.15;margin-top:18px;color:#f6d77a;-webkit-text-stroke:6px #1b2e22;paint-order:stroke'>{big}</div>"
            f"<div style='display:inline-block;margin-top:24px;background:#e0412f;color:#fff;font-family:Noto Sans CJK JP;font-weight:900;font-size:56px;padding:8px 30px;border-radius:14px'>{red}</div>")
    return {'type': 'title', 'y': 640, 'min': 3.2, 'pad': 0.3, 'html': html, 'bg': B(bg), 'voice': voice, 'pop': True, 'punch': True}
def card(num, lab, text, sm, voice, bg, illus, mn=4.4, pad=0.75):
    return {'type': 'card', 'num': num, 'y': 1070, 'lab': lab, 'text': text, 'sm': sm, 'bg': B(bg), 'voice': voice, 'min': mn, 'pad': pad, 'pop': True, 'punch': True, 'illus': illus, 'iy': 290, 'ih': 720}
def giftcard(num, date, fname, gname, bg):
    return card(num, '🎁 プレゼント', gname.replace(' ', '<br>'), "コメントに「やってみる」と書いてね",
                f"{gname.replace('の方へ','のかたへ')}がほしい方は、コメントで、やってみる、と書いてね。", bg, gift_illus(date, fname), 3.6, 0.8)
HL = lambda s: f"<span class=hl>{s}</span>"
RD = lambda s: f"<span style='color:#ff7a66'>{s}</span>"

R6 = {}
# ───── 11/23（月）育成・技術：ドライは根元 ─────
R6['2026-11-23'] = dict(kind='reel', cat='tech', head='乾かすのに時間がかかるなら、根元から。', gift=('dry_kit', '根元から乾かす ドライのチェック表'), scenes=[
 title('「乾かすのに時間がかかる…」', '見るのは「根元」', '先はあとから伸びる', '乾かすのに時間がかかる。見るのは根元。先は、あとから伸びます。', 'table', 124),
 card(1, '差が出るのは', HL('ブラシ') + 'の<br>力加減と距離', '新人さんとベテランで、ここが違う',
      '新人さんと差が出るのは、スリッカーブラシの、力加減と距離です。', 'table',
      svg(brush(120, 260, 1.4) + t(560, 120, '力加減', 50) + t(560, 190, '強すぎず・弱すぎず', 34, GR) + t(560, 330, '当てる距離', 50) + t(560, 400, '根元まで届く深さ', 34, GR) + D(430, 400, .55))),
 card(2, '時間がかかる原因', '根元まで<br>' + RD('届いていない'), '毛玉が残る・根元が伸びない',
      '力が弱いと、けだまが残る。距離が浅いと、根元まで届きません。', 'table',
      svg(t(230, 70, '浅い', 46, R) + t(690, 70, '根元まで', 46, LG) + hair(230, 280, False) + hair(690, 280, True) + t(230, 560, '根元が伸び切らない', 34, R) + t(690, 560, '根元から伸びる', 34, LG) + "<line x1='460' y1='100' x2='460' y2='600' stroke='#ddd' stroke-width='4'/>")),
 card(3, '乾かす前に', 'タオルとブロワーで<br>' + HL('水分を先に飛ばす'), 'タオルドライをしっかりすると、時短に',
      '先にタオルとブロワーで、水分を飛ばす。これで時短になります。', 'clock',
      svg(box(60, 150, 300, 300, '#eef5f0') + t(210, 280, '🧺', 90) + t(210, 400, 'タオルドライ', 40) + arrow(390, 300, 470, 300) + dryer(500, 120, 1.0) + t(690, 480, 'ブロワーで水分を飛ばす', 36) + box(220, 560, 480, 90, G, r=45) + t(460, 620, '乾かす時間が短くなる', 40, Y))),
 card(4, 'ムラが出やすい所から', HL('短い所・内側') + 'を<br>先に乾かす', 'ひじ・股・耳の裏・毛量が多い子の根元',
      '短い所は縮れるので先に。ひじ、股、耳の裏も、先に乾かします。', 'table',
      svg(D(150, 60, 1.05) + f"<circle cx='300' cy='300' r='44' fill='none' stroke='{R}' stroke-width='8'/><circle cx='420' cy='520' r='44' fill='none' stroke='{R}' stroke-width='8'/><circle cx='560' cy='480' r='44' fill='none' stroke='{R}' stroke-width='8'/>" + box(640, 120, 260, 300, '#fff7dc', '#d9b440', 5) + t(770, 190, '先に乾かす', 36, R) + t(770, 260, '① 短い所', 36) + t(770, 320, '② ひじ・股', 36) + t(770, 380, '③ 耳の裏', 36))),
 card(5, '教えるときは、ひと言', '「とにかく' + HL('根元') + '」', '新人さんは迷わず、教える人も楽に',
      '新人さんに教えるときは、とにかく根元、のひと言。教える人も楽になります。', 'note',
      svg(bubble(160, 80, 600, 150, 'とにかく根元！', 60, G) + box(90, 400, 350, 190) + t(265, 475, '新人さん', 40) + t(265, 545, '迷わない', 40, LG) + box(480, 400, 350, 190) + t(655, 475, '教える人', 40) + t(655, 545, '言うことが1つ', 40, LG))),
])
# ───── 11/24（火）経営・集客（新規）：紹介 ─────
R6['2026-11-24'] = dict(kind='biz', cat='new', head='紹介は、お願いしなくても、体験した人の感想から生まれる。', gift=('shoukai_kit', '紹介が生まれる 感想メモ表'), scenes=[
 title('「紹介って、どう増やすの？」', 'お願いはゼロ', '紹介は「感想」から生まれる', '紹介って、どう増やすの。お願いはゼロ。紹介は、感想から生まれます。', 'search', 132),
 card(1, '紹介のきっかけ', '使った人の<br>' + HL('「良かった」'), '紹介した人の感想を聞いて、来てくれる',
      '紹介のきっかけは、使った人の、良かった、という感想です。', 'search',
      svg(box(60, 200, 260, 260) + t(190, 320, '🐶', 90) + t(190, 420, '使った方', 38) + bubble(340, 70, 480, 120, '良かったよ！', 52, G) + arrow(330, 330, 560, 330) + box(590, 200, 270, 260, '#fff7dc') + t(725, 320, '🐕', 90) + t(725, 420, '新しい方', 38) + t(460, 600, '感想 → 紹介', 54, LG))),
 card(2, 'よく紹介してくれる方は', '「' + HL('長持ちする') + '」<br>「他とは違う」', '「体験すると、ここから離れられない」',
      'よく紹介してくれる人は、長持ちする、他とは違う、と言ってくれます。', 'search',
      svg(bubble(60, 60, 400, 130, '長持ちする', 50) + bubble(480, 170, 390, 130, '他とは違う', 50) + bubble(110, 340, 700, 130, 'ここから離れられない', 48) + t(460, 640, '飼い主さんの言葉', 40, GR))),
 card(3, '感想が出るのは', '強みが<br>' + HL('はっきりしている'), 'うちの強みは、シャンプーの仕上がり',
      'うちの強みは、シャンプーの仕上がり。体験した人が、話してくれます。', 'table',
      svg(D(120, 60, 1.0) + "".join(f"<circle cx='{x}' cy='{y}' r='{r}' fill='#cfe8f7' stroke='#8bbad6' stroke-width='3'/>" for x, y, r in [(560, 160, 30), (620, 240, 22), (520, 300, 18), (660, 120, 16)]) + box(560, 380, 330, 200, '#fff7dc', '#d9b440', 5) + t(725, 455, 'うちの強み', 38) + t(725, 525, 'シャンプーの仕上がり', 30, R))),
 card(4, 'やっていること', '仕上がりの良さを<br>' + HL('SNSで伝え続ける'), '紹介された方も、見て確かめられる',
      '仕上がりの良さは、SNSで伝え続けます。紹介された人も確かめられます。', 'search',
      svg("".join(box(90 + i * 260, 120, 220, 300, '#fff', '#cfe0d4', 4) + t(200 + i * 260, 280, '✨', 80) + t(200 + i * 260, 380, f'{i+1}回目', 34, GR) for i in range(3)) + arrow(120, 520, 800, 520, LG, 12) + t(460, 620, '毎回、伝え続ける', 48, LG))),
 card(5, '良くなること', '紹介のお願いは<br>' + HL('しなくていい'), 'スタッフが声かけで気をつかわない',
      'お願いの声かけは、いりません。スタッフも、気をつかわずにすみます。', 'booking',
      svg(box(80, 120, 340, 300) + t(250, 230, '📣', 90) + t(250, 360, 'お願いの声かけ', 34, GR) + f"<line x1='110' y1='150' x2='390' y2='390' stroke='{R}' stroke-width='14'/><line x1='390' y1='150' x2='110' y2='390' stroke='{R}' stroke-width='14'/>" + box(500, 120, 340, 300, '#fff7dc') + t(670, 240, '😊', 90) + t(670, 360, 'スタッフも楽', 38, LG) + t(460, 560, '感想が、紹介になる', 50))),
])
# ───── 11/25（水）育成・スタッフ：何度言っても伝わらない ─────
R6['2026-11-25'] = dict(kind='reel', cat='staff', head='何度言っても伝わらないときは、一度、伝えない。', gift=('tokui_kit', '得意から増やす 育成メモ'), scenes=[
 title('「何度言っても、できない…」', '一度、伝えない', '得意から増やす', '何度言っても、できない。そんなときは、一度、伝えない。得意から増やします。', 'note', 132),
 card(1, '何度も言う所は', 'その人の<br>' + HL('不得意な所'), 'そこから直そうとすると、時間がかかる',
      '何度も言う所は、その人の不得意な所。そこから直すと、時間がかかります。', 'note',
      svg(bubble(80, 60, 400, 120, 'また同じ所…', 46, R, '#fff', R) + box(80, 300, 360, 300) + t(260, 400, '不得意', 56, R) + t(260, 480, '何度も言う所', 36, GR) + box(480, 300, 360, 300, '#eef5f0') + t(660, 400, '得意', 56, LG) + t(660, 480, 'できる所', 36, GR))),
 card(2, '伝わらない理由', '教える人と<br>' + HL('感覚がちがう'), '自分の感覚で教えても、すぐにはつかめない',
      '伝わらないのは、感覚がちがうから。自分の感覚で教えても、つかめません。', 'note',
      svg(f"<circle cx='280' cy='330' r='190' fill='{LG}' opacity='.25'/><circle cx='640' cy='330' r='190' fill='{Y}' opacity='.5'/>" + t(230, 340, '教える人', 44) + t(700, 340, '新人さん', 44) + t(280, 380, 'の感覚', 34, GR) + t(660, 380, 'の感覚', 34, GR) + t(460, 640, '感覚は、人によってちがう', 40))),
 card(3, '変えたこと', HL('できる所') + 'から<br>得意を増やす', '不得意は、慣れてきてから直す',
      'だから、できる所から得意を増やす。不得意は、慣れてから直します。', 'table',
      svg("".join(box(100 + i * 190, 560 - (i + 1) * 110, 170, (i + 1) * 110, LG if i < 3 else '#cfe0d4', r=16) for i in range(4)) + t(185, 600, 'できる所', 30, GR) + t(755, 600, '不得意', 30, GR) + arrow(140, 120, 700, 120, R, 10) + t(420, 90, '得意を先に増やす', 40, R))),
 card(4, 'やり方', 'マニュアルは最低限<br>' + HL('あとは数をやる'), '自由にやって、自分で見つけてもらう',
      'マニュアルは最低限。あとは自由に数をやって、自分で見つけてもらいます。', 'table',
      svg(box(70, 120, 260, 340, '#fff', '#cfe0d4', 5) + "".join(f"<rect x='110' y='{190+i*60}' width='180' height='18' rx='9' fill='#dfe7e1'/>" for i in range(4)) + t(200, 520, 'マニュアル', 38) + t(200, 570, '最低限', 34, GR) + t(470, 300, '＋', 90) + t(700, 230, '正正正', 90, LG) + t(700, 340, '数をやる', 46) + t(700, 410, '自分で見つける', 34, GR))),
 card(5, '伝えるのは', '経験が上がったら<br>' + HL('もう一度伝える'), '教える人も、言い続けなくていい',
      '経験が上がったら、もう一度伝える。教える人も、言い続けなくてすみます。', 'clock',
      svg(f"<polyline points='100,560 300,470 500,360 700,220' fill='none' stroke='{LG}' stroke-width='12'/>" + "".join(f"<circle cx='{x}' cy='{y}' r='16' fill='{LG}'/>" for x, y in [(100, 560), (300, 470), (500, 360)]) + f"<circle cx='700' cy='220' r='26' fill='{Y}' stroke='{G}' stroke-width='6'/>" + bubble(560, 40, 320, 110, 'ここで伝える', 40) + t(400, 640, '経験 →', 40, GR))),
])
# ───── 11/26（木）経営・集客（リピート）：初めての方への一言 ─────
R6['2026-11-26'] = dict(kind='biz', cat='repeat', head='初めての方には「帰ってからの様子を教えてください」。', gift=('hajimete_kit', '初めての方への ひとことメモ'), scenes=[
 title('「初めての方に、なんて言う？」', '帰ったあとの様子', 'を聞いて次に生かす', '初めてのかたに、なんて言う。帰ったあとの様子を聞いて、次に生かします。', 'booking', 120),
 card(1, '初めてのサロンは', 'ワンコにとって<br>' + HL('はじめての場所'), '帰ってからの体調が、気になる',
      '初めてのサロンは、ワンコにとって、はじめての場所。帰ってからの体調が気になります。', 'booking',
      svg(D(140, 70, 1.0) + bubble(560, 80, 300, 120, 'はじめて', 46) + t(700, 380, '🏠', 110) + t(700, 480, '帰ってからは？', 40, R))),
 card(2, '見えないこと', 'お店からは<br>' + RD('帰ってからが見えない'), 'お家の様子は、飼い主さんしか分からない',
      'でも、帰ってからの様子は、お店からは見えません。分かるのは、飼い主さんだけ。', 'booking',
      svg(box(60, 160, 340, 340, '#eef5f0') + t(230, 300, '✂', 90) + t(230, 420, 'お店', 44) + f"<line x1='460' y1='120' x2='460' y2='560' stroke='{R}' stroke-width='10' stroke-dasharray='20 14'/>" + box(520, 160, 340, 340, '#fff7dc') + t(690, 300, '🏠', 90) + t(690, 420, 'お家', 44) + t(460, 630, 'ここから先は見えない', 40, R))),
 card(3, 'お迎えのとき', '「様子を見て<br>' + HL('何かあれば教えて') + '」', '体調の変化があれば、言ってもらう',
      'だから、様子を見て、何かあれば教えてください、と伝えます。', 'booking',
      svg(bubble(70, 60, 780, 200, '何かあれば、教えてください', 48) + box(110, 380, 300, 220) + t(260, 470, '🐶', 80) + t(260, 560, '様子を見る', 36) + arrow(430, 490, 510, 490) + box(530, 380, 300, 220, '#fff7dc') + t(680, 470, '📞', 80) + t(680, 560, 'お店に伝える', 36))),
 card(4, '聞いたことは', '次の美容の<br>' + HL('注意点') + 'に生かす', '次に気をつける所にする',
      '聞いたことを、次の美容の、注意点として生かします。', 'note',
      svg(box(200, 80, 520, 500, '#fff', '#cfe0d4', 5) + t(460, 160, '次の注意点', 46) + "".join(f"<rect x='250' y='{220+i*90}' width='50' height='50' rx='10' fill='#eef5f0' stroke='{LG}' stroke-width='4'/>" + t(275, 260 + i * 90, '✓', 40, LG) + f"<rect x='330' y='{236+i*90}' width='320' height='20' rx='10' fill='#dfe7e1'/>" for i in range(3)))),
 card(5, '良くなること', '気をつける所が<br>' + HL('先に分かる'), 'スタッフも、迷わずに準備できる',
      '次に気をつける所が先に分かるので、担当のスタッフも、迷わず準備できます。', 'booking',
      svg(box(80, 140, 360, 380, '#eef5f0') + t(260, 280, '📋', 100) + t(260, 420, '先に分かる', 44, LG) + box(480, 140, 360, 380, '#fff7dc') + t(660, 280, '😊', 100) + t(660, 420, '迷わず準備', 44, LG))),
])
# ───── 11/27（金）育成・スタッフ：感覚ではなく言葉に ─────
R6['2026-11-27'] = dict(kind='reel', cat='staff', head='仕上がりがバラバラなのは、感覚で教えているから。', gift=('kotoba_kit', '作業を言葉にする マニュアル下書きシート'), scenes=[
 title('「人によって仕上がりがちがう」', '感覚で教えてた', '言葉にすればそろう', '人によって、仕上がりがちがう。原因は、感覚で教えていたこと。言葉にすれば、そろいます。', 'note', 132),
 card(1, 'よくあること', '同じスタイルでも<br>' + RD('仕上がりがバラバラ'), 'スタッフごとに、長さや形がちがう',
      '同じスタイルでも、スタッフごとに、仕上がりが、バラバラになる。', 'table',
      svg(D(20, 150, .7) + D(310, 190, .62) + D(580, 120, .78) + t(460, 80, '同じオーダーなのに…', 44, R))),
 card(2, '原因', '作業を<br>' + HL('感覚で') + '教えていた', '「このくらい」は、人によって受け取り方がちがう',
      '原因は、感覚で教えていたから。このくらい、は、人によって受け取り方がちがいます。', 'note',
      svg(bubble(220, 60, 480, 130, 'このくらい', 56) + box(60, 340, 240, 220) + t(180, 470, '1cm?', 50, R) + box(340, 340, 240, 220) + t(460, 470, '2cm?', 50, R) + box(620, 340, 240, 220) + t(740, 470, '3cm?', 50, R))),
 card(3, 'アタッチメントで', '長さを<br>' + HL('ミリ数で統一'), 'ハサミは、仕上げだけ',
      'アタッチメントで、長さをミリ数で統一。ハサミは、仕上げだけです。', 'table',
      svg(clipper(100, 240, -20, 1.0) + box(380, 110, 480, 120) + t(620, 190, '背中　◯mm', 50, LG) + box(380, 260, 480, 120) + t(620, 340, '足　◯mm', 50, LG) + box(380, 410, 480, 120, '#fff7dc') + t(620, 490, '仕上げ　ハサミ', 50, R))),
 card(4, 'やり方', '全部の作業を<br>' + HL('言葉にする'), 'マニュアルにして、だれでも同じに',
      'そして全部の作業を、言葉にして、マニュアルにします。', 'note',
      svg(box(70, 150, 280, 360, '#fff7dc') + t(210, 300, '💭', 100) + t(210, 440, '感覚', 48) + arrow(380, 330, 520, 330, G, 12) + box(550, 110, 300, 440, '#fff', '#cfe0d4', 5) + t(700, 180, 'マニュアル', 40) + "".join(t(590, 260 + i * 75, s, 32, LG, 'start') for i, s in enumerate(['① 背中 ◯mm', '② 足 ◯mm', '③ 顔 ◯mm', '④ ハサミ'])))),
 card(5, '変わったこと', '成長が早まり<br>' + HL('安心して作業できる'), '仕上がりがそろい、教える人の負担も減る',
      '成長が早まり、仕上がりもそろう。やり方が分かるので、新人さんも安心です。', 'clock',
      svg(D(20, 160, .7) + D(310, 160, .7) + D(600, 160, .7) + t(460, 80, '仕上がりがそろう', 48, LG) + box(250, 600, 420, 80, G, r=40) + t(460, 655, '新人さんも安心', 40, Y))),
])
# ───── 11/28（土）経営・集客（数字）：分かれ目 ─────
R6['2026-11-28'] = dict(kind='biz', cat='num', head='売り上げは、そのまま使えるお金ではありません。', gift=('wakareme_kit', '分かれ目が分かる 計算シート'), scenes=[
 title('「売り上げはあるのに…」', '利益とはちがう', '分かれ目を知る', '売り上げはあるのに、余裕がない。利益とはちがいます。分かれ目を知りましょう。', 'clock', 132),
 card(1, 'よくある思いこみ', '売り上げ＝<br>' + RD('そのまま使えるお金'), '家賃や材料など、お店を続ける分がある',
      '売り上げには、家賃や材料など、お店を続けるための分が入っています。', 'clock',
      svg(box(120, 100, 680, 140, '#eef5f0') + t(460, 190, '売り上げ', 56) + box(120, 280, 420, 120, '#fde3de') + t(330, 360, 'お店を続ける分', 40, R) + box(560, 280, 240, 120, '#fff7dc') + t(680, 360, '使える', 40, LG) + t(460, 520, '家賃・材料・道具など', 40, GR))),
 card(2, '分かれ目（例）', '30万円 ÷ 6,000円<br>＝' + HL('50頭'), '毎月かかるお金 ÷ 1頭の料金（例の数字）',
      'たとえば、毎月30万円かかり、1頭6000円なら、50頭でトントンです。', 'clock',
      svg(t(460, 130, '毎月かかるお金（例）', 40, GR) + t(460, 220, '30万円', 80, R) + t(460, 330, '÷ 1頭 6,000円', 56) + box(280, 400, 360, 160, G, r=30) + t(460, 510, '50頭', 90, Y))),
 card(3, 'アタッチメントで時短', '1日 ' + HL('2頭→3頭') + '<br>（例）', '形はアタッチメントで、ハサミは仕上げだけ',
      'アタッチメントで形を作り、ハサミは仕上げだけ。時短で1日2頭が3頭になれば。', 'table',
      svg(clipper(110, 240, -20, 1.0) + t(570, 140, '1日の頭数（例）', 40, GR) + "".join(t(430 + i * 110, 300, '🐶', 80) for i in range(2)) + t(480, 400, '2頭', 40, GR) + "".join(t(430 + i * 110, 520, '🐶', 80) for i in range(3)) + t(540, 620, '3頭', 44, LG))),
 card(4, '分かれ目をこえる日（例）', '25日目 → ' + HL('17日目'), '1日2頭なら25日目、3頭なら17日目',
      '1日2頭なら25日目。3頭なら、17日目から、ゆとりが始まります。', 'clock',
      svg(bar(220, 180, 25 * 18, '#c9c9c9', '2頭', '25日目') + bar(220, 340, 17 * 18, LG, '3頭', '17日目') + f"<line x1='220' y1='140' x2='220' y2='440' stroke='#888' stroke-width='4'/>" + t(460, 560, '早くこえるほど、月の後半にゆとり', 36))),
 card(5, '良くなること', '月の後半に<br>' + HL('気持ちの余裕'), '時短で増やすので、残業はふえない',
      '月の後半に、気持ちの余裕が出ます。時短で増やすので、残業も増えません。', 'clock',
      svg("".join(box(140 + (i % 7) * 92, 60 + (i // 7) * 92, 80, 80, (LG if i >= 16 else '#eef5f0'), r=14) for i in range(31)) + t(460, 620, '17日目から、ゆとり（例）', 42, LG))),
])

def write_all():
    names = []
    for date, r in R6.items():
        sc = list(r['scenes']); n = sum(1 for s in sc if s.get('num')) + 1
        sc.append(giftcard(n, date, r['gift'][0], r['gift'][1], sc[-1]['bg']['file'].split('/')[-1][:-4]))
        name = f"{date}_fta_w1123"
        cfg = {'out': f'FTA_{date}_w1123.mp4', 'tts': os.path.join(ROOT, 'tools/voicevox/tts_voices.py'), 'voiceName': 'aoyama', 'speed': 1.2, 'crf': 14,
               'brand': 'FUJIWARA TRIMMING ACADEMY', 'tag': 'トリミングサロンの生産性',
               'color': {'card': 'rgba(36,64,47,.86)', 'pill': 'rgba(61,107,79,.95)', 'lab': '#f6d77a', 'labfg': '#24402f', 'hl': '#f6d77a', 'hlfg': '#24402f'},
               'scenes': sc, 'noAnim': True, 'meta': {k: v for k, v in r.items() if k != 'scenes'}}
        json.dump(cfg, open(os.path.join(HERE, name + '.json'), 'w'), ensure_ascii=False, indent=1); names.append(name)
    return names
if __name__ == '__main__':
    print(write_all())
