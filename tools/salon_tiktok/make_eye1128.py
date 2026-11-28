# 11/28 藤原さん「眼がしょぼしょぼネタを試しに作って。動画は顔を洗っているシーン」→ 生産性（育成）版の試し
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'zagaku'))
src = open(os.path.join(HERE, 'make_trial1128.py')).read().split('CFG = {}')[0]
sys.argv = ['x', '/tmp/claude-0/-home-claude/ce93028b-f2d3-5a2d-b5c7-9abb29c3fbe8/scratchpad/eye']
exec(src)
def eye(x, y, kind):
    lid = "<path d='M{a} {b} q 70 -60 140 0 q -70 60 -140 0z' fill='#fff' stroke='#24402f' stroke-width='8'/>".format(a=x-70, b=y)
    if kind == 'sad': lid = "<path d='M{a} {b} q 70 -20 140 0' fill='none' stroke='#24402f' stroke-width='10' stroke-linecap='round'/>".format(a=x-70, b=y) + "<path d='M{a} {b} q 8 30 0 50' fill='none' stroke='#7fb3d9' stroke-width='8' stroke-linecap='round'/>".format(a=x+40, b=y+14)
    else: lid += f"<circle cx='{x}' cy='{y}' r='24' fill='#24402f'/>"
    return lid
def illus(kind):
    base = box(60, 60, 800, 600, '#fff7dc')
    if kind == 'hook':
        return svg(base + eye(330, 300, 'sad') + eye(590, 300, 'sad') + t(460, 520, '目が、しょぼしょぼ…', 54, R))
    if kind == 'heat':
        return svg(base + eye(620, 330, 'open') + "<rect x='120' y='280' width='210' height='110' rx='40' fill='#4b6b8a'/><rect x='170' y='380' width='60' height='130' rx='16' fill='#4b6b8a'/>"
                   + ''.join(f"<path d='M350 {300+k*28} q40 -12 80 0 t80 0' fill='none' stroke='#e0412f' stroke-width='8' stroke-linecap='round'/>" for k in range(3))
                   + t(460, 600, '熱い風を、目に当て続けない', 44, R))
    if kind == 'pin':
        pins = ''.join(f"<line x1='{250+k*26}' y1='230' x2='{250+k*26}' y2='300' stroke='#7a7a7a' stroke-width='6' stroke-linecap='round'/>" for k in range(9))
        return svg(base + "<rect x='230' y='200' width='250' height='40' rx='10' fill='#3d6b4f'/>" + pins + eye(560, 360, 'open')
                   + "<circle cx='490' cy='310' r='40' fill='none' stroke='#e0412f' stroke-width='6' stroke-dasharray='8 6'/>" + t(460, 600, '知らないうちに、ピンが当たる', 44, R))
    if kind == 'guard':
        return svg(base + eye(460, 300, 'open') + "<path d='M330 400 q130 -40 260 0' fill='none' stroke='#e8b48a' stroke-width='46' stroke-linecap='round'/>" + t(460, 560, '目の周りは、指でガード', 56, G))
CFG = [
 hookv('「目が開かない…」', '原因は<br>3つある', 'シャンプーだけじゃない', 'トリミングのあと、目がしょぼしょぼして開かない。原因は、シャンプーだけではありません。', P('w4838.mp4'), 0.5, 140),
 demo(1, '① シャンプー', '原液が目に入る', 'ひとつめは、よく言われる、シャンプーの原液。顔を洗うときは、目の周りに気をつけます。', P('w4838.mp4'), 9.0, 1, '🧴', True),
 demo(2, '② ドライヤー', '熱が目に当たる', 'ふたつめは、ドライヤーの熱。顔を乾かすとき、熱い風が、目に当たり続けていることがあります。', P('d4749.mp4'), 0.5, 1, '💨', True),
 demo(3, '③ ピン', 'スリッカー・コーム', 'みっつめは、スリッカーやコームのピン。知らないうちに、目の近くに当たっていることがあります。', P('d4749.mp4'), 7.0, 1, '🪮', True),
 card(4, '新人さんに', '目の周りは<br>' + HL('指でガード'), '顔を洗う・乾かす・とかすとき',
      '新人さんには、目の周りは、指でガード、とひと言。顔を洗う、乾かす、とかす、どれも同じです。', 'note', __import__('importlib').import_module('eye_guard_svg').guard_svg(850, 718), 5.0),
 endcard(5, '原因は<br>' + HL('3つ'), 'シャンプー、ドライヤー、ピン。保存して、新人さんと見返してね。'),
]
base = {k: v for k, v in json.load(open(os.path.join(HERE, '2026-11-28_fta_trial_ikusei.json'))).items() if k not in ('scenes', 'out')}
json.dump(dict(base, out='FTA_2026-11-28_trial_eye.mp4', scenes=CFG), open(os.path.join(HERE, '2026-11-28_fta_trial_eye.json'), 'w'), ensure_ascii=False, indent=1)
print('ok')
