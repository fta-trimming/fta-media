import os, asyncio
from playwright.async_api import async_playwright
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
C = 'file://' + D + '/crop/'
COL = {'13': '#ea6a1e', '10': '#1aa892', '19': '#9a62d8', '6': '#3a2fd0', '2': '#e8508a', 'h': '#e6b400'}

def chip(t, c):
    return f'<span class="chip" style="background:{c}">{t}</span>'

def mark(shapes, label):
    # shapes: list of (cx,cy,rx,ry) in crop coords 870x970
    el = ''.join(f'<ellipse cx="{a}" cy="{b}" rx="{c}" ry="{d}" />' for a, b, c, d in shapes)
    return (f'<svg viewBox="0 0 870 970" preserveAspectRatio="none" class="ov">{el}</svg>'
            f'<div class="mk">{label}</div>') if shapes else ''

def fig(num, name, chips, photo, plabel, shapes, mlabel, tiles, note):
    t = ''
    for x in tiles:
        n, _, cap = x.partition('|')
        t += f'<div class="tile" style="background-image:url({C}{n}.png)">' + (f'<span class="cap">{cap}</span>' if cap else '') + '</div>'
    cls = {1: 'one', 2: 'two'}.get(len(tiles), 'many')
    return f'''<div class="fig" id="f{num}">
  <div class="hd"><span class="no">{num}</span><b>{name}</b>{chips}</div>
  <div class="row">
    <div class="ph" style="background-image:url({C}{photo})"><span class="lb">{plabel}</span>{mark(shapes, mlabel)}</div>
    <div class="td {cls}"><span class="lb">3D｜刈る場所</span>{t}</div>
  </div>
  <div class="nt">{note}</div>
</div>'''

F = [
    fig('①', '頭', chip('13mm', COL['13']), 'c30.5.png', '実際｜頭を刈った後',
        [(410, 150, 300, 125)], '頭＝黄色の線の中', ['tile_r1_1'], '頭全体を13mmで刈ります。'),
    fig('②', '輪郭サイド・顎下サイド', chip('13mm', COL['13']), 'c24.5.png', '実際｜輪郭サイドと顎下サイドを刈った後',
        [(95, 360, 85, 200), (705, 360, 85, 200)], '左右の横＝黄色の線', ['tile_r1_2|輪郭サイド 13mm', 'tile_r1_3|顎下サイド 13mm'],
        '耳の前（輪郭サイド）と、あごの横（顎下サイド）。左右とも13mm。'),
    fig('③', '顎下', chip('10mm', COL['10']), 'c24.5.png', '実際｜顎下を刈った後',
        [(400, 565, 200, 60)], 'あごの下＝黄色の線', ['tile_r1_4'], 'あごの下は10mm。首は刈りません。'),
    fig('④', 'マズルの上', chip('19mm', COL['19']), 'c30.5.png', '実際｜マズルの上を刈った後',
        [(390, 520, 210, 95)], 'マズルの上＝黄色の線', ['tile_r2_1'], 'マズルの上は19mmで残します。左右とも。'),
    fig('⑤', '目周り・ストップ周り', chip('6mm', COL['6']) + chip('2mm', COL['2']), 'c74.5.png', '実際｜目周りとストップ周りを刈った後',
        [(480, 215, 290, 80)], '目の横と、目と目の間＝黄色の線', ['tile_r2_2|目周り 6mm', 'tile_r2_3|ストップ周り 2mm'],
        '目の横は6mm、目と目の間（ストップ）は2mm。'),
    fig('⑥', 'ハサミで揃える', chip('仕上げ', COL['h']), 'c76.0.png', '実際｜ハサミで揃えた後',
        [], '', ['tile_sc_1', 'tile_sc_2', 'tile_sc_3', 'tile_sc_4'],
        'アタッチメントで刈った後、出ている毛だけを揃えます。'),
]

BA = f'''<div class="fig ba" id="fBA">
  <div class="hd"><b>刈る前 → 仕上がり</b></div>
  <div class="row">
    <div class="ph" style="background-image:url({C}c4.0.png)"><span class="lb dk">刈る前</span></div>
    <div class="arr">▶</div>
    <div class="ph" style="background-image:url({C}c76.0.png)"><span class="lb">仕上がり</span></div>
  </div>
  <div class="nt">13・10・19・6・2mm で刈って、ハサミで揃えた仕上がりです。</div>
</div>'''

TH = f'''<div id="th">
  <div class="l">
    <span class="tag">アタッチメントカット</span>
    <h1>プードルの顔<br>テディベアの輪郭</h1>
    <p>13・10・19・6・2mm<br>刈る順番とハサミの場所</p>
  </div>
  <div class="r">
    <div class="p" style="background-image:url({C}c4.0.png)"><span>BEFORE</span></div>
    <div class="p" style="background-image:url({C}c76.0.png)"><span class="a">AFTER</span></div>
  </div>
</div>'''

CSS = '''
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Noto Sans CJK JP",sans-serif;background:#fff}
.fig{width:900px;background:#f6f3ec;padding:26px 28px 22px}
.hd{display:flex;align-items:center;gap:12px;margin-bottom:16px;font-size:30px;color:#223a2c}
.no{display:inline-flex;width:46px;height:46px;border-radius:50%;background:#2f5a40;color:#fff;align-items:center;justify-content:center;font-size:28px;font-weight:700}
.chip{color:#fff;font-weight:700;font-size:22px;padding:4px 14px;border-radius:20px}
.row{display:flex;gap:14px;align-items:stretch}
.ph{position:relative;width:410px;height:457px;border-radius:18px;background-size:cover;background-position:center;overflow:hidden;flex:none}
.td{position:relative;width:420px;height:457px;border-radius:18px;background:#eee8dc;overflow:hidden;display:flex;flex-wrap:wrap;align-content:center;justify-content:center;gap:8px;padding:52px 8px 8px}
.td.one .tile{width:390px;height:312px;background-size:390px auto;background-position:center bottom}
.td.many .tile{width:196px;height:196px}
.td.two{flex-direction:column;flex-wrap:nowrap;align-items:center;gap:8px}
.td.two .tile{width:404px;height:194px;background-size:404px auto;background-position:center 62%;position:relative;flex:none}
.cap{position:absolute;right:8px;bottom:8px;background:#fff;color:#223a2c;font-weight:700;font-size:18px;padding:3px 10px;border-radius:8px}
.tile{background-size:cover;background-position:center;border-radius:10px}
.lb{position:absolute;left:12px;top:12px;z-index:3;background:#223a2c;color:#fff;font-size:19px;font-weight:700;padding:6px 12px;border-radius:9px}
.lb.dk{background:#555}
.ov{position:absolute;inset:0;width:100%;height:100%;z-index:2}
.ov ellipse{fill:none;stroke:#ffd400;stroke-width:7;stroke-dasharray:16 11;vector-effect:non-scaling-stroke}
.mk{position:absolute;left:12px;bottom:12px;z-index:3;background:#ffd400;color:#222;font-size:19px;font-weight:700;padding:5px 11px;border-radius:9px}
.nt{margin-top:14px;font-size:24px;color:#333;font-weight:500}
.ba .ph{width:400px;height:446px}
.arr{display:flex;align-items:center;font-size:30px;color:#2f5a40}
#th{width:1280px;height:670px;background:#231a17;display:flex;padding:56px 56px}
#th .l{width:560px;color:#fff;display:flex;flex-direction:column;justify-content:center}
#th .tag{align-self:flex-start;background:#f5d76e;color:#231a17;font-weight:700;font-size:26px;padding:6px 18px;border-radius:10px}
#th h1{font-size:64px;line-height:1.3;margin:26px 0 22px;font-weight:900}
#th p{font-size:30px;line-height:1.5;color:#e9dccb;font-weight:500}
#th .r{display:flex;gap:18px;margin-left:auto}
#th .p{position:relative;width:300px;height:558px;border-radius:20px;background-size:cover;background-position:center}
#th .p span{position:absolute;left:14px;top:14px;background:#555;color:#fff;font-weight:700;font-size:24px;padding:4px 14px;border-radius:8px}
#th .p span.a{background:#f5d76e;color:#231a17}
'''

HTML = f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{TH}{"".join(F)}{BA}</body></html>'
open(D + '/figs.html', 'w').write(HTML)

async def main():
    os.makedirs(D + '/out', exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(device_scale_factor=2, viewport={'width': 1400, 'height': 900})
        await pg.goto('file://' + D + '/figs.html'); await pg.wait_for_timeout(500)
        ids = [('th', '00'), ('f①', '01'), ('f②', '02'), ('f③', '03'), ('f④', '04'), ('f⑤', '05'), ('f⑥', '06'), ('fBA', '07')]
        for i, n in ids:
            await pg.locator(f'[id="{i}"]').screenshot(path=f'{D}/out/{n}.png')
        await b.close()
    for n in ['00', '01', '02', '03', '04', '05', '06', '07']:
        im = Image.open(f'{D}/out/{n}.png').convert('RGB')
        im.save(f'{D}/out/note_{n}.jpg', quality=95, subsampling=0)
        print(n, im.size)
asyncio.run(main())
