# 11/28 藤原さん「他の集客や数字、育成も試しに作ってください」→ 手順・技術の新しい形（最初の2秒に答え・実演）の試し3本（予約しない）
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from make_w1123 import svg, t, box, B, HL, RD, G, Y, R, LG, GR
SRC = sys.argv[1]; P = lambda f: os.path.join(SRC, f)
def hookv(top, big, red, voice, clip, start, bs=150):
    html = (f"<div style='font-family:Noto Sans CJK JP;font-size:70px;font-weight:900;color:#fff;-webkit-text-stroke:3px #000;paint-order:stroke'>{top}</div>"
            f"<div style='font-family:Noto Sans CJK JP;font-size:{bs}px;font-weight:900;line-height:1.1;margin-top:16px;color:#f6d77a;-webkit-text-stroke:7px #1b2e22;paint-order:stroke'>{big}</div>"
            f"<div style='display:inline-block;margin-top:22px;background:#e0412f;color:#fff;font-family:Noto Sans CJK JP;font-weight:900;font-size:58px;padding:8px 30px;border-radius:14px'>{red}</div>")
    return {'type': 'title', 'y': 380, 'min': 3.4, 'pad': 0.35, 'html': html, 'bg': {'kind': 'video', 'file': clip, 'start': start, 'speed': 1.0}, 'voice': voice, 'pop': True, 'punch': True}
def demo(num, step, text, voice, clip, start, speed, icon='', badge=True):
    html = (f"<div style='display:inline-flex;align-items:center;gap:26px;background:rgba(36,64,47,.9);border-radius:28px;padding:22px 36px;box-shadow:0 10px 30px rgba(0,0,0,.3)'>"
            + (f"<div style='font-size:110px;line-height:1'>{icon}</div>" if icon else '') +
            f"<div style='text-align:left'><div style='font-family:Noto Sans CJK JP;font-size:52px;font-weight:900;color:#f6d77a'>{step}</div>"
            f"<div style='font-family:Noto Sans CJK JP;font-size:78px;font-weight:900;color:#fff;line-height:1.2'>{text}</div></div></div>"
            + (f"<div style='margin-top:16px'><span style='background:#fff;color:#24402f;font-family:Noto Sans CJK JP;font-weight:900;font-size:32px;padding:4px 18px;border-radius:999px'>実際の作業{' ×'+str(speed)+'倍速' if speed!=1 else ''}</span></div>" if badge else ''))
    return {'type': 'big', 'num': num, 'y': 300, 'html': html, 'bg': {'kind': 'video', 'file': clip, 'start': start, 'speed': speed}, 'voice': voice, 'min': 4.4, 'pad': 0.6, 'pop': True, 'punch': False}
def card(num, lab, text, sm, voice, bg, illus, mn=4.2, pad=0.6):
    return {'type': 'card', 'num': num, 'y': 1070, 'lab': lab, 'text': text, 'sm': sm, 'bg': B(bg), 'voice': voice, 'min': mn, 'pad': pad, 'pop': True, 'punch': True, 'illus': illus, 'iy': 290, 'ih': 720}
def endcard(num, text, voice, bg='note'):
    return card(num, '💾 保存して見返してね', text, '明日の1頭で、試してみてください', voice, bg,
                svg(t(460, 300, '💾', 200) + t(460, 520, '保存して、明日の1頭で', 52, G) + t(460, 600, '試してみてね', 52, LG)), 3.6, 0.6)
def calc(lines, big):
    out = ''
    for i, (a, b) in enumerate(lines):
        y = 90 + i * 150
        out += box(40, y, 840, 120, '#fff', LG, 4) + t(80, y + 78, a, 46, G, 'start') + t(860, y + 80, b, 56, R, 'end')
    return svg(out + box(140, 560, 640, 110, Y) + t(460, 636, big, 58, G))
def dry_ill(kind):
    if kind == 'towel':
        return svg(box(80, 120, 340, 420, '#eef5f0') + t(250, 200, 'タオル', 52) + "<rect x='150' y='250' width='200' height='140' rx='20' fill='#fff' stroke='#3d7a55' stroke-width='6'/>" + t(250, 470, '水分を取る', 40, LG)
                   + box(500, 120, 340, 420, '#eef5f0') + t(670, 200, 'ブロワー', 52) + "<path d='M560 320 h120 m0 -40 q40 40 0 80' fill='none' stroke='#4b6b8a' stroke-width='24' stroke-linecap='round'/>"
                   + "".join(f"<path d='M720 {290+k*30} q30 -10 60 0 t60 0' fill='none' stroke='#9cc3e6' stroke-width='8' stroke-linecap='round'/>" for k in range(3)) + t(670, 470, '水を飛ばす', 40, LG) + t(460, 630, '乾かす時間が短くなる', 46, R))
    return svg(box(60, 80, 800, 520, '#fff7dc') + t(460, 160, '縮れやすい「短い所」から', 50, G)
               + "".join(box(110 + i * 250, 240, 200, 200, '#fff', LG, 5) + t(210 + i * 250, 360, s, 52, LG) for i, s in enumerate(['ひじ', '股', '耳の裏']))
               + t(460, 540, '長い所は、あとから伸ばせる', 44, GR))
CFG = {}
# ───── 育成：新人さんのドライの順番 ─────
CFG['trial_ikusei'] = [
 hookv('「新人さんのドライが遅い…」', '短い所→根元', 'この順で乾かす', '新人さんのドライが遅い。短い所から、根元から、の順で乾かします。', P('IMG_1924.mp4'), 0.5, 140),
 card(1, '① 先に', 'タオルとブロワーで<br>' + HL('水分を飛ばす'), 'ここを飛ばすと、ずっと乾かない',
      'まず、タオルとブロワーで、水分を先に飛ばします。', 'table', dry_ill('towel')),
 card(2, '② 次に', '縮れやすい<br>' + HL('短い所') + 'から', 'ひじ・股・耳の裏',
      '次に、縮れやすい短い所から。ひじ、股、耳の裏です。', 'note', dry_ill('short')),
 demo(3, '③ 最後に', '根元から伸ばす', 'ブラシは、根元まで届く深さで。先は、あとから伸びます。', P('IMG_1924.mp4'), 0.5, 1, '🪮'),
 endcard(4, '新人さんには<br>' + HL('「とにかく根元」'), '新人さんには、とにかく根元、のひと言。保存して、明日の1頭で試してね。'),
]
# ───── 集客：予約につながる動画の撮り方 ─────
CFG['trial_shukyaku'] = [
 hookv('「見られるのに予約が来ない」', '最初の1秒は<br>仕上がりの顔', '撮り方を変えるだけ', '見られているのに、予約が来ない。最初の1秒は、仕上がりの顔にします。', P('IMG_2961.mp4'), 6.0, 120),
 card(1, 'なぜ？', '最初が作業中だと<br>' + RD('すぐ離れる'), '「どうなるか」が先に見えないから',
      '最初が作業中の場面だと、どうなるかが見えず、すぐ離れます。', 'table',
      svg(box(40, 80, 400, 540, '#fff2ef') + t(240, 160, '作業から始まる', 44, R) + "<rect x='130' y='210' width='220' height='280' rx='20' fill='#ddd'/>" + t(240, 370, '✂', 110, GR) + t(240, 580, 'すぐ離れる ✕', 44, R)
          + box(480, 80, 400, 540, '#eef5f0') + t(680, 160, '仕上がりから始まる', 44, LG) + "<rect x='570' y='210' width='220' height='280' rx='20' fill='#fff' stroke='#3d7a55' stroke-width='6'/>" + t(680, 380, '🐩', 130) + t(680, 580, '見てもらえる ○', 44, LG))),
 demo(2, '① 目線の高さで', '正面から寄る', 'ワンコの目の高さで、正面から、顔に寄って撮ります。', P('IMG_2961.mp4'), 0.0, 1, '📱', False),
 demo(3, '② いちばん最初に', '仕上がりの顔', 'その顔を、動画のいちばん最初に置きます。作業の場面は、そのあとです。', P('IMG_2961.mp4'), 8.0, 1, '✨', False),
 card(4, '③ 最後に', 'どこで予約できるか<br>' + HL('1行で書く'), '「プロフィールのLINEから予約できます」',
      '最後に、どこで予約できるかを、1行で書きます。', 'note',
      svg(box(110, 120, 700, 420, '#fff', LG, 5) + t(460, 230, '🐩 仕上がりの顔', 50, G) + t(460, 330, '✂ 作業の場面', 50, GR) + box(170, 390, 580, 100, Y) + t(460, 458, '予約はプロフィールのLINEから', 40, G) + t(460, 630, 'この順番で並べる', 46, LG))),
 endcard(5, '最初の1秒は<br>' + HL('仕上がりの顔'), '最初の1秒は、仕上がりの顔。保存して、次の投稿で試してね。'),
]
# ───── 数字：トントンの頭数の出し方 ─────
CFG['trial_suuji'] = [
 hookv('「毎月、何頭でトントン？」', '30万÷6,000<br>＝50頭', '（例）割り算1回で分かる', '毎月、何頭でトントンか。割り算1回で分かります。', P('v1.mp4'), 100.0, 130),
 card(1, '① 出す', '毎月かかるお金を<br>' + HL('ざっくり足す'), '家賃・材料・光熱費・人件費など（例）',
      'まず、毎月かかるお金を、ざっくり足します。例えば、30万円。', 'table',
      calc([('家賃', '12万'), ('材料・光熱費', '6万'), ('人件費など', '12万')], '合計 30万円（例）')),
 card(2, '② 割る', '1頭の料金で<br>' + HL('割る'), '30万円 ÷ 6,000円 ＝ 50頭（例）',
      '次に、1頭の料金で割ります。30万円わる6000円で、50頭です。', 'note',
      calc([('毎月かかるお金', '30万円'), ('1頭の料金', '6,000円'), ('30万 ÷ 6,000', '50頭')], '50頭でトントン（例）')),
 card(3, '③ 1日に直す', '営業日で<br>' + HL('割る'), '50頭 ÷ 25日 ＝ 1日2頭（例）',
      '最後に、営業日で割ります。25日なら、1日2頭でトントンです。', 'table',
      calc([('トントンの頭数', '50頭'), ('営業日', '25日'), ('50 ÷ 25', '1日2頭')], '1日3頭なら17日目でこえる')),
 endcard(4, '割り算<br>' + HL('2回') + 'でOK', '割り算2回で、トントンの頭数が分かります。保存して、自分のお店の数字で試してね。'),
]
base = {'tts': '/home/claude/fta-media/tools/voicevox/tts_voices.py', 'voiceName': 'aoyama', 'speed': 1.2, 'crf': 14, 'size': [720, 1280],
        'brand': 'FUJIWARA TRIMMING ACADEMY', 'tag': 'トリミングサロンの生産性',
        'color': {'card': 'rgba(36,64,47,.86)', 'pill': 'rgba(61,107,79,.95)', 'lab': '#f6d77a', 'labfg': '#24402f', 'hl': '#f6d77a', 'hlfg': '#24402f'}}
for k, sc in CFG.items():
    json.dump(dict(base, out=f'FTA_2026-11-28_{k}.mp4', scenes=sc), open(os.path.join(HERE, f'2026-11-28_fta_{k}.json'), 'w'), ensure_ascii=False, indent=1)
print('ok')
