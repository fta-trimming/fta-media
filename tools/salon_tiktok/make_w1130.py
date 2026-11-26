# 11/30 の週の生産性リール（v5 やさしい言い回し：6場面・40秒以内・1場面目は実際の作業の映像）の設定を作る。
# 使い方: python3 make_w1130.py <素材のフォルダ> → 2026-1X-XX_fta_w1130.json を6つ書く → python3 build_fta.py <名前>
# 素材（720×1280 の縦の元の動画）は GitHub に置かないので、作るたびにドライブ FTA元素材 から取ってくる。
import json, os, sys, base64, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
from make_w1123 import svg, t, D, box, arrow, bubble, clipper, B, HL, RD, BK, G, Y, R, LG, GR
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '_src')

def gift_illus(date):
    d = os.path.join(ROOT, 'gift', date); out = []
    for i in (2, 1):
        sm = os.path.join(HERE, f'_g{date}_{i}.jpg')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(d, f'kit_{i}.jpg'), '-vf', 'scale=840:-1:flags=lanczos', '-q:v', '2', sm], check=True)
        out.append(base64.b64encode(open(sm, 'rb').read()).decode()); os.remove(sm)
    imgs = ''.join(f"<img src='data:image/jpeg;base64,{b}' style='position:absolute;height:600px;left:{360+o*80}px;top:{40+o*10}px;transform:rotate({r}deg);box-shadow:0 8px 24px rgba(0,0,0,.25);border-radius:6px'>" for b, o, r in zip(out, (1, 0), (5, -2)))
    return f"<div style='position:relative;width:920px;height:668px'>{imgs}<div style='position:absolute;left:20px;top:170px;font-family:Noto Sans CJK JP;font-weight:900;font-size:120px'>🎁</div><div style='position:absolute;left:10px;top:330px;width:340px;text-align:center;font-family:Noto Sans CJK JP;font-weight:700;font-size:40px;color:{G};line-height:1.4'>A4・2ページ<br><span style='background:{Y};padding:0 10px;border-radius:8px'>DMでお届け</span></div></div>"

def hook(top, big, red, voice, clip, start, bigsize=132, note=''):
    html = (f"<div style='font-family:Noto Sans CJK JP;font-size:72px;font-weight:900;color:#fff;-webkit-text-stroke:3px #000;paint-order:stroke'>{top}</div>"
            f"<div style='font-family:Noto Sans CJK JP;font-size:{bigsize}px;font-weight:900;line-height:1.15;margin-top:18px;color:#f6d77a;-webkit-text-stroke:6px #1b2e22;paint-order:stroke'>{big}</div>"
            f"<div style='display:inline-block;margin-top:24px;background:#e0412f;color:#fff;font-family:Noto Sans CJK JP;font-weight:900;font-size:56px;padding:8px 30px;border-radius:14px'>{red}</div>"
            + (f"<div style='margin-top:18px;font-family:Noto Sans CJK JP;font-size:36px;font-weight:700;color:#fff;-webkit-text-stroke:2px #000;paint-order:stroke'>{note}</div>" if note else ''))
    return {'type': 'title', 'y': 600, 'min': 3.2, 'pad': 0.35, 'html': html, 'bg': {'kind': 'video', 'file': os.path.join(SRC, clip), 'start': start, 'speed': 1.0}, 'voice': voice, 'pop': True, 'punch': True}
def card(num, lab, text, sm, voice, bg, illus, mn=4.2, pad=0.7):
    return {'type': 'card', 'num': num, 'y': 1070, 'lab': lab, 'text': text, 'sm': sm, 'bg': B(bg), 'voice': voice, 'min': mn, 'pad': pad, 'pop': True, 'punch': True, 'illus': illus, 'iy': 290, 'ih': 720}
def giftcard(num, date, gname, bg):
    return card(num, '🎁 プレゼント', gname.replace(' ', '<br>', 1), "コメントに「やってみる」と書いてね",
                f"{gname}がほしい方は、コメントで、やってみる、と書いてね。", bg, gift_illus(date), 3.6, 0.8)
def scissors(x, y, rot=0, s=1):
    return (f"<g transform='translate({x},{y}) rotate({rot}) scale({s})'><circle cx='0' cy='0' r='34' fill='none' stroke='#555' stroke-width='12'/><circle cx='0' cy='90' r='34' fill='none' stroke='#555' stroke-width='12'/>"
            f"<polygon points='28,20 300,40 290,52 26,38' fill='#bbb'/><polygon points='28,72 300,46 290,34 26,56' fill='#999'/></g>")
def clock(x, y, r, label, col=G):
    return f"<circle cx='{x}' cy='{y}' r='{r}' fill='#fff' stroke='{col}' stroke-width='12'/><line x1='{x}' y1='{y}' x2='{x}' y2='{y-r*.65}' stroke='{col}' stroke-width='10' stroke-linecap='round'/><line x1='{x}' y1='{y}' x2='{x+r*.5}' y2='{y}' stroke='{col}' stroke-width='10' stroke-linecap='round'/>" + t(x, y + r + 60, label, 44, col)
def row(y, heads, money, col, lab, labfg='#fff'):
    return box(40, y, 840, 130, '#fff') + t(90, y + 88, heads, 64, G, 'start') + t(560, y + 86, money, 54, col if col != '#c9c9c9' else GR, 'end') + box(600, y + 20, 240, 90, col, r=45) + t(720, y + 82, lab, 46, labfg)
def person(x, y, col=LG, s=1):
    return f"<g transform='translate({x},{y}) scale({s})'><circle cx='0' cy='0' r='46' fill='{col}'/><rect x='-60' y='56' width='120' height='150' rx='50' fill='{col}'/></g>"

R6 = {}
# ───── 11/30（月）育成・技術：嫌がる作業で時間がかかる ─────
R6['2026-11-30'] = dict(kind='reel', cat='tech', head='爪切りで手が止まるのは、押さえ方に慣れていないから。', gift=('hitori_kit', '一人でできる？ 嫌がる作業チェック表'),
 footage=('a261106_5.mp4', 8.0, '足先をハサミで整える手元（ワンコの足を片手で押さえている）・LINE_ALBUM_SNS素材_261106_5（11/6撮影）'), scenes=[
 hook('「爪切りで手が止まる…」', '押さえ方', 'に慣れていないだけ', '爪切りで、手が止まる。押さえ方に、慣れていないだけです。', 'a261106_5.mp4', 8.0),
 card(1, 'よくあること', '爪切り・顔カットで<br>' + RD('時間がかかる'), 'ワンコが嫌がる作業で、止まる',
      '爪切り、耳そうじ、顔カット。ワンコが嫌がる作業で、時間がかかります。', 'table',
      svg(D(250, 150, .75) + bubble(60, 30, 260, 110, '爪切り', 46) + bubble(330, 30, 280, 110, '耳そうじ', 46) + bubble(620, 30, 280, 110, '顔カット', 46) + t(460, 640, 'ここで手が止まる', 48, R))),
 card(2, 'なぜ？', '学校では<br>' + HL('押さえてもらっていた'), 'サロンでは、押さえるのも切るのも一人',
      '学校では、2人で1頭。押さえるのは、相手がしてくれていました。', 'note',
      svg(box(40, 120, 400, 420, '#eef5f0') + t(240, 190, '学校', 50) + person(170, 300) + person(310, 300, Y) + t(240, 600, '2人で1頭', 44) + box(480, 120, 400, 420, '#fff7dc') + t(680, 190, 'サロン', 50) + person(680, 300) + t(680, 600, '1人で1頭', 44, R))),
 card(3, 'こうする', '一人で最後まで<br>' + HL('やる経験') + 'を増やす', '押さえる・切る・なだめるを、自分で',
      'だから、一人で最後までやる経験を、増やします。', 'table',
      svg(person(160, 200, LG, 1.2) + "".join(box(330, 110 + i * 150, 540, 120, '#fff', LG, 5) + t(380, 190 + i * 150, s, 46, G, 'start') for i, s in enumerate(['① 押さえる', '② 切る', '③ なだめる']))
          + t(600, 620, 'ぜんぶ一人で', 48, LG))),
 card(4, 'すると', '1頭の時間が<br>' + HL('短くなる'), '形はアタッチメント、ハサミは仕上げだけ',
      '嫌がる作業で、止まらなくなります。形はアタッチメントで作れば、もっと短くなります。', 'clock',
      svg(clipper(130, 260, -20, 1.0) + clock(620, 260, 150, '1頭の時間が短く') + t(460, 640, '教える人も、横で押さえなくていい', 38, GR))),
])
# ───── 12/1（火）経営・集客（リピート）：空いた枠はリピーターさんで ─────
R6['2026-12-01'] = dict(kind='biz', cat='repeat', head='時短で空いた枠は、まずリピーターさんの月1回で埋める。', gift=('shuuki_kit', '空いた枠を埋める 来店の周期メモ'),
 footage=('img3006.mp4', 5.5, '仕上がったトイプードルの全身と顔・IMG_3006（10/27届いた素材）'), scenes=[
 hook('「時短で空いた枠…」', 'リピーターさん', 'の月1回で埋める', '時短で空いた枠。まず、リピーターさんの、月1回で埋めます。', 'img3006.mp4', 5.5, 120),
 card(1, 'よくあること', '空いた枠を<br>' + RD('新規で埋めようとする'), '予約がなければ、空いたまま',
      '時短で空いた枠を、新規で埋めようとする。でも、予約が入らなければ、空いたままです。', 'booking',
      svg("".join(box(80 + (i % 4) * 200, 90 + (i // 4) * 170, 170, 140, '#eef5f0' if i not in (2, 5, 6) else '#fde3de', r=18) + t(165 + (i % 4) * 200, 175 + (i // 4) * 170, '空き' if i in (2, 5, 6) else '🐶', 44 if i in (2, 5, 6) else 70, R if i in (2, 5, 6) else G) for i in range(8)) + t(460, 520, '時短で空いた枠', 48, R) + t(460, 610, '予約がないと、空いたまま', 40, GR))),
 card(2, 'なぜ？', 'すぐできるのは<br>' + HL('リピーターさん'), '来てくれる周期を、短くするだけ',
      'すぐにできるのは、リピーターさん。来てくれる周期を、短くするだけです。', 'booking',
      svg(t(230, 110, '今', 50, GR) + box(80, 150, 300, 120, '#fde3de') + t(230, 230, '2か月に1回', 44, R) + arrow(410, 210, 510, 210) + t(690, 110, 'これから', 50, LG) + box(540, 150, 300, 120, '#eef5f0') + t(690, 230, '月1回', 52, LG) + D(300, 320, .6))),
 card(3, 'こうする', '月1回のケアを<br>' + HL('おすすめする'), 'スタイルを保つなら、最低でも月1回',
      '月1回のケアを、おすすめします。スタイルを保つなら、最低でも1か月に1回です。', 'booking',
      svg(box(150, 60, 620, 520, '#fff', '#cfe0d4', 5) + t(460, 140, 'カレンダー', 44, GR) + "".join(box(200 + (i % 7) * 76, 180 + (i // 7) * 76, 64, 64, '#eef5f0', r=10) for i in range(28)) + f"<circle cx='{232}' cy='{212}' r='40' fill='none' stroke='{R}' stroke-width='8'/>" + t(460, 640, '月に1回、同じころに', 44, LG))),
 card(4, 'すると', '空いた枠が<br>' + HL('埋まっていく'), '空いた時間の一部は、スタッフの練習にも',
      '空いた枠が、埋まっていきます。空いた時間の一部は、スタッフの練習にも使えます。', 'clock',
      svg("".join(box(80 + (i % 4) * 200, 90 + (i // 4) * 170, 170, 140, '#eef5f0' if i != 6 else '#fff7dc', r=18) + t(165 + (i % 4) * 200, 175 + (i // 4) * 170, '練習' if i == 6 else '🐶', 44 if i == 6 else 70, LG) for i in range(8)) + t(460, 560, '枠が埋まる', 52, LG))),
])
# ───── 12/2（水）育成・スタッフ：時間の目安を決める ─────
R6['2026-12-02'] = dict(kind='reel', cat='staff', head='終わりが見えないなら、時間の目安を決める。', gift=('meyasu_kit', '終わりが見える 1頭の時間の目安シート'),
 footage=('a261105_7.mp4', 1.5, '顔まわりをストレートのハサミで切る手元・LINE_ALBUM_SNS素材_261105_7（11/5撮影）'), scenes=[
 hook('「終わりが見えない…」', 'カット120分', 'と決めると迷わない', '終わりが見えない。カットは120分、と決めると、迷いません。', 'a261105_7.mp4', 1.5, 124, '（うちの目安）'),
 card(1, 'よくあること', '全部きれいにして<br>' + RD('終わらない'), '仕上げの手が、止まらない',
      '全部をきれいにしようとして、なかなか終わらない。', 'table',
      svg(scissors(150, 200, -10, 1.3) + clock(660, 260, 150, 'まだ終わらない', R))),
 card(2, 'なぜ？', '終わりどころが<br>' + HL('決まっていない'), 'なんとなくの作業は、むだが増える',
      '終わりどころが、決まっていないからです。なんとなくの作業は、むだが増えます。', 'note',
      svg(f"<path d='M120 380 C 220 120, 320 600, 420 300 S 620 120, 720 420' fill='none' stroke='{R}' stroke-width='12' stroke-dasharray='24 16'/>" + t(780, 480, '？', 120, R) + t(460, 640, 'ゴールが見えない', 48, R))),
 card(3, 'こうする', '時間の目安を<br>' + HL('決めておく'), '形はアタッチメント、ハサミは仕上げだけ',
      '時間の目安を、決めておきます。うちのカットは、120分が目安です。', 'clock',
      svg(clock(270, 220, 150, '120分') + box(520, 140, 340, 120, '#eef5f0') + t(690, 220, 'カット', 50) + box(520, 300, 340, 120, '#fff7dc') + t(690, 380, 'うちの目安', 44) + t(460, 620, '終わりが見える', 52, LG))),
 card(4, 'すると', 'むだな作業が<br>' + HL('へる'), '残業もへって、体も楽に',
      'やることがはっきりして、むだな作業がへります。残業もへり、体も楽になります。', 'clock',
      svg(box(80, 120, 340, 380, '#eef5f0') + t(250, 260, '✓', 120, LG) + t(250, 420, 'やることが', 40) + t(250, 470, 'はっきり', 40) + box(500, 120, 340, 380, '#fff7dc') + t(670, 260, '🏠', 110) + t(670, 420, '定時に', 40) + t(670, 470, '帰れる', 40, LG))),
])
# ───── 12/3（木）経営・集客（新規）：強みを1つにしぼる ─────
R6['2026-12-03'] = dict(kind='biz', cat='new', head='「だれでも来てほしい」をやめて、強みを1つにしぼる。', gift=('tsuyomi_kit', '強みを1つにしぼる メモ'),
 footage=('a261105_6.mp4', 1.0, 'シャンプーのすすぎの手元・LINE_ALBUM_SNS素材_261105_6（11/5撮影）'), scenes=[
 hook('「だれでも来てほしい…」', '強みは1つ', 'シャンプーの仕上がり', 'だれでも来てほしい、をやめる。うちの強みは1つ。シャンプーの仕上がりです。', 'a261105_6.mp4', 1.0),
 card(1, 'よくあること', 'だれにでも向けると<br>' + RD('伝わりにくい'), '何が良いお店か、分かりにくい',
      'だれにでも向けたお店は、何が良いのか、伝わりにくい。', 'search',
      svg("".join(bubble(60 + (i % 3) * 280, 80 + (i // 3) * 220, 240, 110, s, 40, GR, '#fff', '#ccc') for i, s in enumerate(['カット', 'シャンプー', 'ケア', '爪切り', '何でも', '？'])) + t(460, 640, '何が強みか、分からない', 44, R))),
 card(2, 'うちがしたこと', '来てほしい人を<br>' + HL('しぼった'), '強みは、シャンプーの仕上がり',
      'うちは、来てほしい人をしぼり、シャンプーの仕上がりを、強みにしました。', 'table',
      svg(f"<circle cx='460' cy='300' r='230' fill='none' stroke='{LG}' stroke-width='10'/><circle cx='460' cy='300' r='140' fill='none' stroke='{LG}' stroke-width='10'/><circle cx='460' cy='300' r='60' fill='{Y}'/>" + t(460, 315, '1つ', 40) + t(460, 640, 'シャンプーの仕上がり', 48, LG))),
 card(3, 'こうする', '仕上がりを<br>' + HL('SNSで伝え続ける'), '同じ強みを、毎回見せる',
      'その仕上がりを、SNSで、伝え続けます。', 'search',
      svg("".join(box(90 + i * 260, 120, 220, 300, '#fff', '#cfe0d4', 4) + t(200 + i * 260, 280, '✨', 80) + t(200 + i * 260, 380, 'シャンプー', 32, GR) for i in range(3)) + arrow(120, 520, 800, 520, LG, 12) + t(460, 620, '毎回、同じ強み', 48, LG))),
 card(4, 'すると', '新規の予約が<br>' + HL('変わった'), 'リピーターさんの周期も、変わった',
      '新規の予約も、リピーターさんの周期も、変わりました。', 'booking',
      svg(box(80, 140, 360, 380, '#eef5f0') + t(260, 280, '📅', 100) + t(260, 420, '新規の予約', 44, LG) + box(480, 140, 360, 380, '#fff7dc') + t(660, 280, '🔁', 100) + t(660, 420, '来店の周期', 44, LG))),
])
# ───── 12/4（金）育成・技術：新人さんは長めのミリ数から ─────
R6['2026-12-04'] = dict(kind='reel', cat='tech', head='新人さんは、長めのミリ数から。残った長さで決める。', gift=('nagame_kit', '長めから決める ミリ数メモ'),
 footage=('a261105_5.mp4', 7.5, 'カットのあとの体の長さを手でととのえる場面・LINE_ALBUM_SNS素材_261105_5（11/5撮影）'), scenes=[
 hook('「ミリ数が決められない…」', '長めから', '残った長さで決める', 'ミリ数が、決められない。新人さんは、長めから。残った長さを見て決めます。', 'a261105_5.mp4', 7.5),
 card(1, 'よくあること', 'いきなり短めで<br>' + RD('刈ってしまう'), '短く刈ると、もどせない',
      'いきなり、このくらい、と短めで刈ると、失敗につながります。', 'table',
      svg(clipper(140, 250, -20, 1.0) + box(420, 150, 420, 120, '#fde3de') + t(630, 230, 'いきなり短め', 46, R) + arrow(630, 290, 630, 380, R) + box(420, 400, 420, 120, '#fff') + t(630, 480, 'もどせない', 46, R))),
 card(2, 'なぜ？', 'ミリ数で長さが<br>' + HL('イメージできない'), 'ベテランは、残る長さが分かる',
      '新人さんは、ミリ数で、残る長さがイメージできません。ベテランは、分かります。', 'note',
      svg(box(60, 120, 380, 420, '#fff7dc') + t(250, 200, '新人さん', 46) + t(250, 360, '◯mm＝？', 64, R) + box(480, 120, 380, 420, '#eef5f0') + t(670, 200, 'ベテラン', 46) + t(670, 360, '◯mm＝分かる', 52, LG))),
 card(3, 'こうする', '長めの<br>' + HL('アタッチメントから'), '残った長さを見て、ミリ数を決める',
      'だから、長めのアタッチメントから始めて、残った長さを見て、ミリ数を決めます。', 'table',
      svg(clipper(120, 250, -20, 1.0) + "".join(box(400, 110 + i * 150, 460, 120, c, r=24) + t(630, 190 + i * 150, s, 44, G) for i, (s, c) in enumerate([('① 長めで刈る', '#eef5f0'), ('② 残った長さを見る', '#eef5f0'), ('③ ミリ数を決める', '#fff7dc')])))),
 card(4, 'すると', '失敗が<br>' + HL('へる'), '教える人の負担も、軽くなる',
      '失敗がへり、新人さんも安心。教える人の負担も、軽くなります。', 'clock',
      svg(D(60, 120, .75) + box(560, 140, 300, 380, '#eef5f0') + t(710, 270, '😊', 100) + t(710, 410, '新人さんも', 40) + t(710, 460, '安心', 44, LG))),
])
# ───── 12/5（土）経営・集客（数字）：早くなっても予約がないと赤字 ─────
R6['2026-12-05'] = dict(kind='biz', cat='num', head='早くなっても、予約が入らないと赤字のまま。', gift=('kuroji_kit', '何頭で黒字？ 頭数の計算シート'), akajiKuroji=True,
 footage=('a261105_14.mp4', 2.0, '顔まわりをハサミで整える手元・LINE_ALBUM_SNS素材_261105_14（11/5撮影）'), scenes=[
 hook('「早くなったのに…」', '59頭まで赤字', '予約が入って黒字', '早くなったのに、余裕がない。59頭までは、赤字です。', 'a261105_14.mp4', 2.0, 118, '月36万円・1頭6,000円なら（例）'),
 card(1, 'よくあること', '早くなっても<br>' + RD('空き時間が増えるだけ'), '予約が入らないと、売り上げは同じ',
      '時短で早くなっても、予約が入らないと、空き時間が増えるだけです。', 'clock',
      svg(clock(250, 260, 160, '早くなった', LG) + box(520, 150, 340, 260, '#fde3de') + t(690, 270, '空き時間', 50, R) + t(690, 340, '予約なし', 40, R) + t(460, 640, '売り上げは、同じまま', 44, GR))),
 card(2, '何頭で黒字？（例）', '60頭で<br>' + HL('トントン'), '毎月36万円かかり、1頭6,000円のとき',
      '毎月36万円、1頭6000円なら、60頭でトントン。59頭までは、赤字です。', 'clock',
      svg(row(30, '50頭', '−6万円', R, '赤字') + row(200, '60頭', '±0', '#c9c9c9', 'トントン', G) + row(370, '75頭', '＋9万円', '#111', '黒字') + t(460, 600, '月36万円・1頭6,000円（例）', 36, GR))),
 card(3, 'こうする', '空いた時間に<br>' + HL('予約を入れる'), '形はアタッチメント、ハサミは仕上げだけ',
      '形はアタッチメントで作り、時短した分の時間に、予約を入れます。', 'table',
      svg(clipper(130, 250, -20, 1.0) + arrow(330, 300, 450, 300) + "".join(box(480 + (i % 2) * 190, 120 + (i // 2) * 170, 170, 140, '#eef5f0', r=18) + t(565 + (i % 2) * 190, 215 + (i // 2) * 170, '🐶', 70) for i in range(4)) + t(460, 640, '空いた時間に予約', 48, LG))),
 card(4, '1か月だと（25日・例）', '1日3頭なら<br>' + HL('9万円の黒字'), '1日3頭×25日＝75頭',
      '1日3頭、25日で75頭なら、9万円の黒字です。', 'clock',
      svg(t(460, 70, '1か月25日（例）', 40, GR) + t(40, 200, '1日2頭', 44, G, 'start') + box(260, 145, 420, 90, '#e0412f', r=45) + t(470, 205, '50頭 −6万円', 44, '#fff') + t(40, 380, '1日3頭', 44, G, 'start') + box(260, 325, 600, 90, '#111', r=45) + t(560, 385, '75頭 ＋9万円', 44, '#fff') + t(460, 560, '予約が入って、はじめて黒字', 44, LG))),
])

def write_all():
    names = []
    for date, r in R6.items():
        sc = list(r['scenes']); n = sum(1 for s in sc if s.get('num')) + 1
        sc.append(giftcard(n, date, r['gift'][1], sc[-1]['bg']['file'].split('/')[-1][:-4]))
        name = f"{date}_fta_w1130"
        cfg = {'out': f'FTA_{date}_w1130.mp4', 'tts': os.path.join(ROOT, 'tools/voicevox/tts_voices.py'), 'voiceName': 'aoyama', 'speed': 1.2, 'crf': 14,
               'size': [720, 1280],
               'brand': 'FUJIWARA TRIMMING ACADEMY', 'tag': 'トリミングサロンの生産性',
               'color': {'card': 'rgba(36,64,47,.86)', 'pill': 'rgba(61,107,79,.95)', 'lab': '#f6d77a', 'labfg': '#24402f', 'hl': '#f6d77a', 'hlfg': '#24402f'},
               'scenes': sc, 'noAnim': True, 'meta': {k: v for k, v in r.items() if k != 'scenes'}}
        json.dump(cfg, open(os.path.join(HERE, name + '.json'), 'w'), ensure_ascii=False, indent=1); names.append(name)
    return names
if __name__ == '__main__':
    print(write_all())
