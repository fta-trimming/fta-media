# 11/23 の週の生産性リールのプレゼント（6本・A4 3ページ）。使い方: python3 gift_w1123.py
# gift/<日付>/<名前>.pdf と kit_1.jpg〜 を作る（fta-gift-pdf の形・ログイン無しのPDF）。
import os, subprocess
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CSS = """@page{size:A4;margin:0}*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Noto Sans CJK JP',sans-serif;color:#333}
.page{width:210mm;height:297mm;padding:16mm 15mm;position:relative;page-break-after:always;overflow:hidden}
.top{display:flex;justify-content:space-between;font-size:9pt;color:#6b6b6b;letter-spacing:1px}
.tag{display:inline-block;background:#3d6b4f;color:#fff;font-weight:700;font-size:11pt;padding:2mm 5mm;border-radius:20mm;margin-top:8mm}
h1{font-size:25pt;color:#24402f;font-weight:900;margin-top:5mm;line-height:1.3}
.lead{font-size:12pt;margin-top:4mm;line-height:1.7}
.row{display:flex;align-items:center;gap:5mm;border-bottom:1px solid #e0e8e3;padding:4.6mm 2mm;font-size:13.5pt;font-weight:700;color:#24402f}
.bx{flex:0 0 11mm;height:11mm;border:2.5px solid #3d6b4f;border-radius:2.5mm}
.y{background:linear-gradient(transparent 60%,#f6d77a 60%)}
.hint{margin-top:7mm;background:#e8f2ec;border-radius:4mm;padding:5mm 6mm;font-size:12pt;line-height:1.7}
table{width:100%;border-collapse:collapse;margin-top:6mm;font-size:11pt}
th{background:#3d6b4f;color:#fff;padding:3mm 1mm;font-weight:700;border:1px solid #3d6b4f}
td{border:1px solid #b9cdc0;height:13mm;text-align:center}
tr.ex td{background:#fdf6e3;color:#8a6d1d;font-weight:700}
.foot{position:absolute;bottom:10mm;left:15mm;right:15mm;font-size:8.5pt;color:#6b6b6b;display:flex;justify-content:space-between}
.steps{display:flex;gap:3mm;margin-top:6mm}
.st{flex:1;background:#e8f2ec;border-radius:3mm;padding:3mm;text-align:center;font-size:10.5pt;font-weight:700;color:#24402f;line-height:1.5}
.st b{display:block;font-size:16pt;color:#3d6b4f}
.big{font-size:20pt;font-weight:900;color:#c8700a}
.cal{display:grid;grid-template-columns:repeat(7,1fr);gap:1.6mm;margin-top:6mm}
.cal div{border:1px solid #b9cdc0;height:17mm;border-radius:2mm;font-size:10pt;font-weight:700;color:#24402f;padding:1.2mm 2mm}
"""
def top(name, i, n):
    return f"<div class='top'><span>FUJIWARA TRIMMING ACADEMY</span><span>{i} / {n}</span></div>"
def checks(items): return "<div style='margin-top:6mm'>" + "".join(f"<div class='row'><span class='bx'></span>{t}</div>" for t in items) + "</div>"
def table(heads, ex=None, rows=7, widths=None):
    h = "".join(f"<th{(' style=width:'+widths[i]) if widths else ''}>{x}</th>" for i, x in enumerate(heads))
    e = ("<tr class='ex'>" + "".join(f"<td>{x}</td>" for x in ex) + "</tr>") if ex else ""
    b = "".join("<tr>" + "<td></td>" * len(heads) + "</tr>" for _ in range(rows))
    return f"<table><tr>{h}</tr>{e}{b}</table>"
def foot(l): return f"<div class='foot'><span>{l}</span><span>@fujiwara__trimming</span></div>"

G = {}
# 11/23 月 育成：ドライ
G['2026-11-23'] = dict(file='dry_kit', name='根元から乾かす ドライのチェック表', pages=[
 f"<div class='tag'>🎁 根元から乾かす ドライのチェック表</div><h1>乾かす前と乾かすときに<br><span class='y'>できているか ○×</span></h1><p class='lead'>×の所から、1つだけ直してください。</p>" + checks([
  'タオルドライを、しっかりしてから始めている', 'ブロワーで、先に水分をしっかり飛ばしている', 'スリッカーブラシの力が弱すぎない（毛玉が取り切れる）',
  'ブラシを当てる距離が浅すぎない（根元まで届く）', '毛が短い所を、先に乾かしている', 'ひじ・股・耳の裏を、意識して乾かしている', '毛量が多い子は、根元を意識している']) +
 "<div class='hint'><b>新人さんへのひと言：「とにかく根元」</b><br>ブロワーをしっかり根元から当てる。根元が乾けば、先もあとから伸びます。</div>" + foot('2ページ目：乾かす順番 ／ 3ページ目：練習の記録'),
 "<div class='tag'>乾かす順番</div><h1>ムラが出やすい所から<br><span class='y'>先に乾かす</span></h1>" +
 "<div class='steps'><div class='st'><b>①</b>タオルドライ<br>をしっかり</div><div class='st'><b>②</b>ブロワーで<br>水分を飛ばす</div><div class='st'><b>③</b>毛が短い所<br>（すぐ縮れる）</div><div class='st'><b>④</b>内側<br>ひじ・股・耳の裏</div><div class='st'><b>⑤</b>毛量が多い所<br>の根元</div></div>" +
 table(['順番', '場所', '気をつけること', 'できた ○'], ['（例）③', '顔まわり', '縮れる前に先に', '○'], 6, ['12%', '28%', '44%', '16%']) +
 "<div class='hint'>力が弱いと、もつれや毛玉が取り切れません。<br>距離が浅いと、根元まで届かず、根元が伸び切りません。</div>" + foot('お店の順番に書きかえて使ってください'),
 "<div class='tag'>練習の記録</div><h1>ムラが出た所を書いて<br><span class='y'>次に先に乾かす</span></h1><p class='lead'>乾かし終わったら、ムラが出た所を1つ書きます。次の子では、そこを先に乾かします。</p>" +
 table(['日付', 'ワンコ（犬種）', 'かかった時間', 'ムラが出た所', '次に先に乾かす所'], ['（例）', 'トイプードル', '◯分', '耳の裏', '耳の裏'], 8) + foot('保存して、練習のたびに見返してね')])
# 11/24 火 経営・集客（新規）：紹介
G['2026-11-24'] = dict(file='shoukai_kit', name='紹介が生まれる 感想メモ表', pages=[
 f"<div class='tag'>🎁 紹介が生まれる 感想メモ表</div><h1>紹介は、お願いより<br><span class='y'>体験した人の感想</span>から</h1><p class='lead'>あてはまる所に ○。×の所から1つだけ始めてください。</p>" + checks([
  'お店の強みを、1つの文で言える', '強みの仕上がりを、SNSで伝え続けている', 'お客様の「良かった」の言葉を、メモしている',
  'どこが良かったのか（長持ち・他とちがう など）まで聞いている', '紹介で来た方に、どなたの紹介かを聞いている', 'スタッフ全員が、お店の強みを同じ言葉で言える']) +
 "<div class='hint'><b>よく紹介してくれる方の言葉（藤原さんのお店）</b><br>「美容の効果が長持ちする」「体験すると、ここから離れられない」「他とは違う」</div>" + foot('2ページ目：感想メモ ／ 3ページ目：強みの1文'),
 "<div class='tag'>感想メモ</div><h1>飼い主さんの言葉を<br><span class='y'>そのまま書く</span></h1><p class='lead'>言いかえずに、聞いた言葉のまま書きます。SNSで仕上がりを伝えるときの言葉にもなります。</p>" +
 table(['日付', 'ワンコ', '飼い主さんの言葉', 'どこが良かった？'], ['（例）', 'マルチーズ', '「前より長持ちする」', 'シャンプーの仕上がり'], 8, ['13%', '17%', '40%', '30%']) + foot('1か月ためると、お店の強みが言葉で見えてきます'),
 "<div class='tag'>強みの1文</div><h1>お店の強みを<br><span class='y'>1つの文にする</span></h1><p class='lead'>感想メモで多かった言葉を使って、強みを1文にします。スタッフ全員で同じ文を使います。</p>" +
 "<div class='hint' style='font-size:13pt'>（例）うちの強みは、<b>シャンプーの仕上がり</b>です。<br>　　　飼い主さんからは「<b>長持ちする</b>」と言われます。</div>" +
 table(['うちの強みは', '飼い主さんからは、なんと言われる？'], None, 3, ['45%', '55%']) +
 "<div class='hint'>この1文を、SNSで仕上がりを見せるたびに書きます。紹介で来た方も、同じことを見て確かめられます。</div>" + foot('保存して見返してね')])
# 11/25 水 育成：何度言っても伝わらない
G['2026-11-25'] = dict(file='tokui_kit', name='得意から増やす 育成メモ', pages=[
 f"<div class='tag'>🎁 得意から増やす 育成メモ</div><h1>何度言っても伝わらないときの<br><span class='y'>教え方チェック</span></h1><p class='lead'>あてはまる所に ○。×の所から1つだけ変えてください。</p>" + checks([
  '何度も言う所は、その人の不得意な所だと分かっている', '先に、できる所（得意）を増やしている', '不得意は、慣れてきてから直している',
  'マニュアルは最低限にして、あとは自由にやらせている', '伝わらないときは、しばらく伝えずに様子を見ている', '経験が上がったところで、もう一度伝えている']) +
 "<div class='hint'><b>伝わらないのは、感覚がちがうから</b><br>教える人の感覚で伝えても、すぐにはつかめません。数をやって、本人の感覚に当てはまるまで経験を上げます。</div>" + foot('2ページ目：得意・不得意の表 ／ 3ページ目：もう一度伝える日'),
 "<div class='tag'>得意・不得意の表</div><h1>作業ごとに<br><span class='y'>得意から ○ をつける</span></h1>" +
 table(['作業', '得意 ○', 'まだ △', '先に任せる？'], ['（例）シャンプー', '○', '', '任せる'], 9, ['40%', '18%', '18%', '24%']) +
 "<div class='hint'>○の作業から任せて、できる所を増やします。△は、慣れてきてから直します。</div>" + foot('月に1回、書き直してください'),
 "<div class='tag'>もう一度伝える日</div><h1>数をやってから<br><span class='y'>もう一度伝える</span></h1><p class='lead'>伝えない間に、何回やったかを数えます。経験が上がったところで、もう一度伝えます。</p>" +
 table(['不得意な作業', 'やった回数（正の字）', 'もう一度伝えた日', 'そのときの様子'], ['（例）顔カット', '正正', '◯月◯日', '自分で気づいた'], 7, ['25%', '27%', '20%', '28%']) + foot('保存して見返してね')])
# 11/26 木 経営・集客（リピート）：初めての方への一言
G['2026-11-26'] = dict(file='hajimete_kit', name='初めての方への ひとことメモ', pages=[
 f"<div class='tag'>🎁 初めての方への ひとことメモ</div><h1>お迎えのとき<br><span class='y'>このひと言を伝える</span></h1>" +
 "<div class='hint' style='font-size:15pt;line-height:1.8'>「はじめてのサロンなので、<br>　お家に帰ってからの様子を見てあげてください。<br>　何かあれば、教えてください。」</div>" +
 "<p class='lead'>聞いたことは、次の美容の注意点として生かします。</p>" + checks([
  '初めての方に、帰ってからの様子を見てほしいと伝えている', '「何かあれば教えてください」と言っている', '聞いたことを、次の美容の前に見返している',
  'スタッフのだれが担当でも、同じひと言を伝えている']) + foot('2ページ目：様子メモ ／ 3ページ目：次の注意点'),
 "<div class='tag'>帰ってからの様子メモ</div><h1>飼い主さんから<br><span class='y'>聞いたことを書く</span></h1>" +
 table(['日付', 'ワンコ', '聞いたこと（帰ってからの様子）', '担当'], ['（例）', 'ポメラニアン', '帰ってから、よく寝ていた', '◯◯'], 9, ['13%', '18%', '52%', '17%']) + foot('電話・LINE・次の来店のときに聞いたことも書きます'),
 "<div class='tag'>次の注意点</div><h1>聞いたことを<br><span class='y'>次の美容に生かす</span></h1><p class='lead'>次の予約の前に見返して、気をつける所を書きます。</p>" +
 table(['ワンコ', '前に聞いたこと', '次に気をつける所'], ['（例）ポメラニアン', '帰ってから、よく寝ていた', '休けいを入れながら進める'], 7, ['20%', '40%', '40%']) + foot('保存して見返してね')])
# 11/27 金 育成：感覚ではなく言葉にする
G['2026-11-27'] = dict(file='kotoba_kit', name='作業を言葉にする マニュアル下書きシート', pages=[
 f"<div class='tag'>🎁 作業を言葉にする マニュアル下書きシート</div><h1>仕上がりがバラバラなら<br><span class='y'>感覚を言葉にする</span></h1><p class='lead'>あてはまる所に ○。×の所から1つだけ始めてください。</p>" + checks([
  'スタイルごとに、アタッチメントのミリ数を決めている', '刈る順番を、だれでも同じにしている', 'ハサミは、仕上げだけに使っている',
  '「このくらい」「いい感じに」を使わずに教えている', '作業を、マニュアルに書いて残している', '新人さんが、マニュアルを見て一人で進められる']) +
 "<div class='hint'><b>感覚で教えると、人によって仕上がりがバラバラに</b><br>全部の作業を言葉にすると、分かりやすく、同じ仕上がりをくり返せます。</div>" + foot('2ページ目：言葉にする表 ／ 3ページ目：言いかえ表'),
 "<div class='tag'>言葉にする表</div><h1>工程ごとに<br><span class='y'>ミリ数・順番を書く</span></h1>" +
 table(['順番', '場所', '道具・ミリ数', '気をつけること'], ['（例）①', '背中', 'アタッチメント◯mm', '毛流を見て刈る'], 9, ['12%', '22%', '30%', '36%']) + foot('スタイルごとに1枚ずつ作ります'),
 "<div class='tag'>言いかえ表</div><h1>感覚の言葉を<br><span class='y'>数字と場所にする</span></h1><p class='lead'>ふだん使っている感覚の言葉を書き出して、数字や場所の言葉に言いかえます。</p>" +
 table(['感覚の言葉', '言いかえた言葉'], ['（例）「短めに」', '「アタッチメント◯mmで」'], 8, ['45%', '55%']) + foot('保存して見返してね')])
# 11/28 土 経営・集客（数字）：分かれ目
G['2026-11-28'] = dict(file='wakareme_kit', name='分かれ目が分かる 計算シート', pages=[
 f"<div class='tag'>🎁 分かれ目が分かる 計算シート</div><h1>売り上げは、そのまま<br><span class='y'>使えるお金ではない</span></h1><p class='lead'>ざっくりでいいので、月の分かれ目（トントンになる頭数）を出してみます。</p>" +
 "<div class='steps'><div class='st'><b>①</b>毎月かかるお金<br>（家賃・材料など）</div><div class='st'><b>②</b>1頭の料金</div><div class='st'><b>③</b>① ÷ ②<br>＝分かれ目の頭数</div><div class='st'><b>④</b>③ ÷ 1日の頭数<br>＝こえる日</div></div>" +
 "<table><tr><th style='width:40%'></th><th>（例）</th><th>あなたのお店</th></tr><tr class='ex'><td style='width:40%'>① 毎月かかるお金</td><td>30万円</td><td></td></tr><tr><td>② 1頭の料金</td><td>6,000円</td><td></td></tr><tr class='ex'><td>③ 分かれ目の頭数</td><td>50頭</td><td></td></tr><tr><td>④ 1日2頭なら</td><td>25日目</td><td></td></tr><tr class='ex'><td>④ 1日3頭なら</td><td>17日目</td><td></td></tr></table>" +
 "<div class='hint' style='font-size:10.5pt'>※例の数字です（30万円 ÷ 6,000円 ＝ 50頭。50 ÷ 2 ＝ 25日目、50 ÷ 3 ＝ 16.7 → 17日目）。</div>" + foot('2ページ目：カレンダー ／ 3ページ目：チェック'),
 "<div class='tag'>分かれ目カレンダー</div><h1>分かれ目をこえる日に<br><span class='y'>印をつける</span></h1><p class='lead'>毎日、その日までの頭数を書きます。分かれ目の頭数をこえた日に ★ をつけます。</p>" +
 "<div class='cal'>" + "".join(f"<div>{d}</div>" for d in range(1, 32)) + "</div>" + foot('★の日が早くなるほど、月の後半にゆとりが出ます'),
 "<div class='tag'>チェック</div><h1>分かれ目を<br><span class='y'>早める</span>には</h1><p class='lead'>あてはまる所に ○。</p>" + checks([
  '毎月かかるお金を、ざっくり知っている', '分かれ目の頭数を、知っている', '1頭にかかる時間を、はかったことがある',
  'アタッチメントで形を作り、ハサミは仕上げにしている', '時短した分で、1日の頭数を見直している', '残業で頭数を増やしていない']) + foot('保存して見返してね')])

def build(date):
    g = G[date]; d = os.path.join(ROOT, 'gift', date); os.makedirs(d, exist_ok=True)
    n = len(g['pages'])
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>" + "".join(
        f"<div class='page'>{top(g['name'], i+1, n)}{p}</div>" for i, p in enumerate(g['pages'])) + "</body></html>"
    hp = os.path.join(d, '_kit.html'); open(hp, 'w').write(html)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg = b.new_page(viewport={'width': 794, 'height': 1123}, device_scale_factor=2160/794)
        pg.goto('file://' + hp); pg.wait_for_timeout(400)
        pg.pdf(path=os.path.join(d, g['file'] + '.pdf'), format='A4', print_background=True)
        for i, el in enumerate(pg.query_selector_all('.page')):
            png = os.path.join(d, f'kit_{i+1}.png'); el.screenshot(path=png)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', png, '-q:v', '1', os.path.join(d, f'kit_{i+1}.jpg')], check=True); os.remove(png)
        b.close()
    os.remove(hp)
    print(date, g['file'], 'ok')
if __name__ == '__main__':
    import sys
    for k in (sys.argv[1:] or G): build(k)
