# 11/30 の週の生産性リールのプレゼント（6本・A4 2ページ）。使い方: python3 gift_w1130.py [日付...]
# gift/<日付>/<名前>.pdf と kit_1.jpg〜 を作る（fta-gift-pdf の形・ログイン無しのPDF）。形は gift_w1123.py と同じ。
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gift_w1123 import CSS, top, checks, table, foot, ROOT
from playwright.sync_api import sync_playwright

G = {}
# 11/30 月 育成（技術）：嫌がる作業は一人で押さえる経験
G['2026-11-30'] = dict(file='hitori_kit', name='一人でできる？ 嫌がる作業チェック表', pages=[
 "<div class='tag'>🎁 一人でできる？ 嫌がる作業チェック表</div><h1>爪切り・耳そうじ・顔カット<br><span class='y'>一人で最後までできるか ○×</span></h1><p class='lead'>ワンコが嫌がる作業は、押さえ方（保定）に慣れていないと時間がかかります。×の所から1つだけ練習してください。</p>" + checks([
  '爪切りを、一人で押さえて最後までできる', '耳そうじを、一人で押さえて最後までできる', '顔カットを、一人で押さえて最後までできる',
  'ワンコが動いたとき、一人でなだめて続けられる', '「押さえてください」と、だれかにたのまずに進められる', 'カットの形はアタッチメントで作り、ハサミは仕上げだけにしている']) +
 "<div class='hint'><b>学校では2人で1頭。サロンでは1人。</b><br>押さえるのも、切るのも、なだめるのも自分。だから「とにかく一人でやる経験」を増やします。</div>" + foot('2ページ目：一人でできた記録'),
 "<div class='tag'>一人でできた記録</div><h1>嫌がる作業を<br><span class='y'>一人で最後まで</span></h1><p class='lead'>一人で最後までできたら ○。かかった時間も書くと、短くなっていくのが見えます。</p>" +
 table(['日付', 'ワンコ（犬種）', '作業', '一人でできた ○', 'かかった時間'], ['（例）', 'トイプードル', '爪切り', '○', '◯分'], 10, ['14%', '24%', '20%', '20%', '22%']) + foot('保存して、練習のたびに見返してね')])
# 12/1 火 経営・集客（リピート）：空いた枠はリピーターさんの月1回で
G['2026-12-01'] = dict(file='shuuki_kit', name='空いた枠を埋める 来店の周期メモ', pages=[
 "<div class='tag'>🎁 空いた枠を埋める 来店の周期メモ</div><h1>時短で空いた枠は<br><span class='y'>まずリピーターさん</span>で</h1><p class='lead'>新規を待つより、すぐにできるのは、リピーターさんの周期を短くすること。あてはまる所に ○。</p>" + checks([
  '時短で、空いた枠がどれくらいあるか知っている', 'リピーターさんの、今の来店の周期を知っている', 'スタイルを保つには、最低でも月1回とお伝えしている',
  'お迎えのとき、その場で次の時期を提案している', '無理にはすすめず、飼い主さんの周期に合わせている', '空いた時間の一部を、スタッフの練習に使っている']) +
 "<div class='hint'><b>うちのおすすめは、基本1か月に1回</b><br>間があきすぎると、頭の毛が割れたり、毛玉になったりします。</div>" + foot('2ページ目：来店の周期メモ'),
 "<div class='tag'>来店の周期メモ</div><h1>今の周期と<br><span class='y'>次にすすめる時期</span></h1><p class='lead'>周期が2か月以上のワンコから、月1回のケアをすすめます。</p>" +
 table(['ワンコ（お名前）', '前の来店', '今の周期', '次にすすめる時期', '予約 ○'], ['（例）◯◯ちゃん', '◯月◯日', '2か月', '1か月後', '○'], 10, ['26%', '18%', '16%', '24%', '16%']) + foot('保存して見返してね')])
# 12/2 水 育成（スタッフ）：時間の目安を決める
G['2026-12-02'] = dict(file='meyasu_kit', name='終わりが見える 1頭の時間の目安シート', pages=[
 "<div class='tag'>🎁 終わりが見える 1頭の時間の目安シート</div><h1>コースごとに<br><span class='y'>時間の目安を決める</span></h1><p class='lead'>終わりどころが決まっていないと、全部をきれいにしようとして終わりません。まず目安の時間を決めます。</p>" +
 "<table><tr><th style='width:40%'>コース</th><th>うちの目安</th><th>あなたのお店</th></tr><tr class='ex'><td>シャンプーコース</td><td>60分</td><td></td></tr><tr class='ex'><td>カットコース</td><td>120分</td><td></td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td></tr></table>" +
 checks(['コースごとに、時間の目安を決めている', 'スタッフ全員が、同じ目安を知っている', '形はアタッチメントで作り、ハサミは仕上げだけにしている', 'なんとなくの作業をやめ、やることを決めている']) +
 "<div class='hint'>目安があると、やることがはっきりして、むだな作業がへります。</div>" + foot('2ページ目：時間の記録'),
 "<div class='tag'>時間の記録</div><h1>目安と<br><span class='y'>かかった時間</span>をくらべる</h1><p class='lead'>目安をこえたときは、時間がかかった作業を1つだけ書きます。</p>" +
 table(['日付', 'ワンコ', 'コース', '目安', 'かかった時間', '時間がかかった作業'], ['（例）', 'トイプードル', 'カット', '120分', '◯分', '顔カット'], 10, ['12%', '18%', '14%', '12%', '16%', '28%']) + foot('保存して見返してね')])
# 12/3 木 経営・集客（新規）：強みを1つにしぼる
G['2026-12-03'] = dict(file='tsuyomi_kit', name='強みを1つにしぼる メモ', pages=[
 "<div class='tag'>🎁 強みを1つにしぼる メモ</div><h1>「だれでも来てほしい」を<br><span class='y'>やめてみる</span></h1><p class='lead'>うちは、来てほしいお客さまをしぼり、シャンプーの仕上がりを強みにしました。あてはまる所に ○。</p>" + checks([
  '来てほしいお客さま（ワンコ）を、1つの文で言える', 'お店の強みを、1つにしぼっている', 'その強みの仕上がりを、SNSで伝え続けている',
  'スタッフ全員が、同じ強みを言える', '強みに合うメニューを、いちばん上に出している']) +
 "<div class='hint'><b>うちの場合</b><br>強みは「シャンプーの仕上がり」。SNSでその魅力を伝え続けて、新規の予約もリピーターさんの周期も変わりました。</div>" + foot('2ページ目：しぼり込みメモ'),
 "<div class='tag'>しぼり込みメモ</div><h1>だれに・何を<br><span class='y'>1つずつ書く</span></h1>" +
 table(['来てほしいお客さま・ワンコ', 'うちの強み（1つ）', 'SNSで見せる場面'], ['（例）◯◯なワンコの飼い主さん', 'シャンプーの仕上がり', 'シャンプー後の仕上がり'], 4, ['36%', '30%', '34%']) +
 "<div class='hint'>書いた強みを、投稿のたびに同じ言葉で見せます。</div>" +
 table(['日付', '投稿した場面', '反応（コメント・予約）'], ['（例）', 'シャンプー後の仕上がり', 'コメント◯件'], 5, ['16%', '42%', '42%']) + foot('保存して見返してね')])
# 12/4 金 育成（技術）：新人さんは長めのミリ数から
G['2026-12-04'] = dict(file='nagame_kit', name='長めから決める ミリ数メモ', pages=[
 "<div class='tag'>🎁 長めから決める ミリ数メモ</div><h1>新人さんは<br><span class='y'>長めのミリ数から</span></h1><p class='lead'>新人さんは、ミリ数で残る長さがイメージできません。いきなり短めで刈ると、失敗につながります。</p>" +
 "<div class='steps'><div class='st'><b>①</b>長めの<br>アタッチメントで刈る</div><div class='st'><b>②</b>残った長さを<br>見る・さわる</div><div class='st'><b>③</b>使うミリ数を<br>決める</div><div class='st'><b>④</b>決めたミリ数を<br>書いておく</div></div>" +
 checks(['最初は、長めのアタッチメントから始めている', '刈ったあと、残った長さを見てからミリ数を決めている', 'ハサミは、仕上げだけにしている', '決めたミリ数を、紙に書いて残している']) + foot('2ページ目：ミリ数メモ'),
 "<div class='tag'>ミリ数メモ</div><h1>残った長さを見て<br><span class='y'>ミリ数を決める</span></h1><p class='lead'>同じワンコの次の回は、このメモから始めます。</p>" +
 table(['ワンコ', '場所', '最初のミリ数', '残った長さ', '次に使うミリ数'], ['（例）◯◯ちゃん', '背中', '◯mm（長め）', '少し長い', '◯mm'], 10, ['22%', '16%', '20%', '20%', '22%']) + foot('保存して見返してね')])
# 12/5 土 経営・集客（数字）：早くなっても、予約が入らないと赤字
G['2026-12-05'] = dict(file='kuroji_kit', name='何頭で黒字？ 頭数の計算シート', pages=[
 "<div class='tag'>🎁 何頭で黒字？ 頭数の計算シート</div><h1>早くなっても<br><span class='y'>予約が入らないと赤字</span></h1><p class='lead'>時短で空いた時間に予約が入って、はじめて黒字になります。まず、トントンの頭数を出します。</p>" +
 "<table><tr><th style='width:40%'></th><th>（例）</th><th>あなたのお店</th></tr><tr class='ex'><td>① 毎月かかるお金</td><td>36万円</td><td></td></tr><tr><td>② 1頭の料金</td><td>6,000円</td><td></td></tr><tr class='ex'><td>③ ① ÷ ② ＝ トントンの頭数</td><td>60頭</td><td></td></tr></table>" +
 "<table><tr><th>月の頭数（例）</th><th>のこるお金</th><th></th></tr>"
 "<tr><td>50頭（1日2頭×25日）</td><td>−6万円</td><td><span style='background:#e0412f;color:#fff;font-weight:700;padding:1mm 4mm;border-radius:6mm'>赤字</span></td></tr>"
 "<tr><td>60頭</td><td>±0</td><td><span style='background:#c9c9c9;color:#24402f;font-weight:700;padding:1mm 4mm;border-radius:6mm'>トントン</span></td></tr>"
 "<tr><td>75頭（1日3頭×25日）</td><td>＋9万円</td><td><span style='background:#111;color:#fff;font-weight:700;padding:1mm 4mm;border-radius:6mm'>黒字</span></td></tr></table>" +
 "<div class='hint' style='font-size:10.5pt'>※例の数字です（36万円 ÷ 6,000円 ＝ 60頭。59頭までは赤字、61頭から黒字）。</div>" + foot('2ページ目：空き時間の記録'),
 "<div class='tag'>空き時間の記録</div><h1>空いた時間に<br><span class='y'>予約が入ったか</span></h1><p class='lead'>時短で空いた時間と、そこに入った予約を書きます。月の頭数が、トントンの頭数をこえたか見ます。</p>" +
 table(['日付', '空いた時間', '入った予約', 'その日までの頭数'], ['（例）', '14時〜16時', 'リピーターさん1頭', '32頭'], 10, ['14%', '26%', '32%', '28%']) + foot('保存して見返してね')])

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
    for k in (sys.argv[1:] or G): build(k)
