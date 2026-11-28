import math
FUR='#e3a56c'; DARK='#9a5f35'; SKIN='#f3cfa2'; HAND='#f1c7a5'; HL='#b07a55'
def face(ox, oy, k):
    s=[f"<g transform='translate({ox} {oy}) scale({k})'>"]
    s+=[f"<ellipse cx='-215' cy='40' rx='80' ry='150' fill='{DARK}'/>",f"<ellipse cx='215' cy='40' rx='80' ry='150' fill='{DARK}'/>"]
    for i in range(20):
        a=i/20*2*math.pi; s.append(f"<circle cx='{205*math.cos(a):.0f}' cy='{-10+190*math.sin(a):.0f}' r='56' fill='{FUR}'/>")
    s+=[f"<ellipse cx='0' cy='-10' rx='215' ry='200' fill='{FUR}'/>",f"<ellipse cx='0' cy='95' rx='108' ry='82' fill='{SKIN}'/>","<ellipse cx='0' cy='65' rx='30' ry='23' fill='#2b1d16'/>",
        "<path d='M0 88 v20 m0 0 q-22 20 -44 4 m44 -4 q22 20 44 4' fill='none' stroke='#2b1d16' stroke-width='6' stroke-linecap='round'/>"]
    for x in (-95,95): s+=[f"<ellipse cx='{x}' cy='-30' rx='30' ry='27' fill='#2b1d16'/>",f"<circle cx='{x+9}' cy='-39' r='8' fill='#fff'/>"]
    s.append('</g>'); return ''.join(s)
def comb(x, y, rot, k=1):
    t=''.join(f"<rect x='{8+i*17}' y='20' width='7' height='52' rx='3' fill='#8a939c'/>" for i in range(9))
    return f"<g transform='translate({x} {y}) rotate({rot}) scale({k})'><rect x='0' y='0' width='165' height='24' rx='8' fill='#3d5a80'/>{t}</g>"
def burst(x, y, fill, stroke):
    return f"<path transform='translate({x} {y})' d='M0 -26 l8 16 l18 -6 l-8 16 l16 10 l-18 4 l2 18 l-14 -10 l-12 14 l-2 -18 l-18 -2 l14 -12 l-10 -16 l18 2z' fill='{fill}' stroke='{stroke}' stroke-width='3'/>"
def guard_svg(w=900, h=760):
    s=[f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 900 760'>"]
    # 左：ガードなし
    s.append("<rect x='14' y='14' width='428' height='600' rx='26' fill='#fff2ef' stroke='#e0412f' stroke-width='5'/>")
    s.append("<text x='228' y='76' font-size='42' font-weight='900' text-anchor='middle' fill='#e0412f' font-family='Noto Sans CJK JP'>✕ そのまま</text>")
    s.append("<defs><clipPath id='cl'><rect x='14' y='14' width='428' height='600' rx='26'/></clipPath><clipPath id='cr'><rect x='458' y='14' width='428' height='600' rx='26'/></clipPath></defs>")
    s.append("<g clip-path='url(#cl)'>"+face(228, 380, 0.68)+"</g>")
    s.append(comb(268, 262, 28, 0.9))  # 歯の先が右目に届く
    s.append(burst(298, 352, '#ffd0c8', '#e0412f'))
    s.append("<text x='228' y='585' font-size='34' font-weight='900' text-anchor='middle' fill='#e0412f' font-family='Noto Sans CJK JP'>ピンが目に当たる</text>")
    # 右：指でガード
    s.append("<rect x='458' y='14' width='428' height='600' rx='26' fill='#eef7f0' stroke='#2e9a5b' stroke-width='5'/>")
    s.append("<text x='672' y='76' font-size='42' font-weight='900' text-anchor='middle' fill='#2e9a5b' font-family='Noto Sans CJK JP'>○ 指でガード</text>")
    s.append("<g clip-path='url(#cr)'>"+face(672, 380, 0.68)+"</g>")
    # 手：右上から、人さし指を右目の上のふちに沿わせる
    s.append(f"<path d='M886 250 L820 262 Q796 270 794 300 L798 340 Q830 362 886 356 Z' fill='{HAND}' stroke='{HL}' stroke-width='4' stroke-linejoin='round'/>")
    s.append(f"<path d='M806 296 L700 304 Q680 306 680 322 Q680 338 700 338 L812 334 Z' fill='{HAND}' stroke='{HL}' stroke-width='4' stroke-linejoin='round'/>")
    s.append(f"<path d='M684 310 q2 -6 16 -6 q4 10 0 26 q-14 2 -16 -6z' fill='#fbe3d3' stroke='{HL}' stroke-width='3'/>")
    s.append(comb(705, 210, 28, 0.9))  # 歯の先は指で止まる
    s.append(burst(742, 300, '#f6d77a', '#e0a400'))
    s.append("<circle cx='737' cy='368' r='34' fill='none' stroke='#2e9a5b' stroke-width='6' stroke-dasharray='10 7'/>")
    s.append("<text x='672' y='585' font-size='34' font-weight='900' text-anchor='middle' fill='#2e9a5b' font-family='Noto Sans CJK JP'>ピンは指に当たる</text>")
    s.append("<text x='450' y='700' font-size='46' font-weight='900' text-anchor='middle' fill='#24402f' font-family='Noto Sans CJK JP'>人さし指を、目の上のふちに</text>")
    s.append("<text x='450' y='748' font-size='32' font-weight='700' text-anchor='middle' fill='#6b6b6b' font-family='Noto Sans CJK JP'>洗う・乾かす・とかす、どれも同じ</text>")
    s.append('</svg>'); return ''.join(s)
if __name__=='__main__':
    open('g.html','w').write("<html><body style='margin:0;background:#f7efe2'>"+guard_svg()+"</body></html>")
