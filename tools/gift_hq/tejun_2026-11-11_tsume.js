let pw; try{pw=require('playwright')}catch(e){pw=require('/home/claude/fta-media/node_modules/playwright')}
const D='#231714', Y='#f2d06b';
const fs=require('fs');const U=f=>'data:image/jpeg;base64,'+fs.readFileSync(f).toString('base64');
const css=`*{box-sizing:border-box}body{margin:0;width:1080px;height:1920px;background:${D};font-family:'Noto Sans CJK JP';color:#fff;position:relative;overflow:hidden}
.y{color:${Y}} .ph{position:absolute;border-radius:22px;overflow:hidden} .ph img{width:100%;height:100%;object-fit:cover;display:block}
.lb{position:absolute;padding:.25em .6em;border-radius:1em;background:rgba(36,23,19,.92);font-weight:900;white-space:nowrap}.tag{position:absolute;left:16px;top:16px;padding:6px 18px;border-radius:10px;font-weight:900;font-size:30px}`;

const R='#ff2d6f';
const annB=(s)=>`<svg viewBox="0 0 600 770" style="position:absolute;left:0;top:0;width:100%;height:100%"><defs><marker id="ah${s}" markerWidth="5" markerHeight="5" refX="2.5" refY="2.5" orient="auto-start-reverse" markerUnits="strokeWidth"><path d="M0,0 L5,2.5 L0,5 z" fill="${R}"/></marker></defs>
<line x1="20" y1="168" x2="600" y2="168" stroke="${Y}" stroke-width="8" stroke-dasharray="24 14"/>
<line x1="138" y1="252" x2="244" y2="174" stroke="${R}" stroke-width="10" stroke-linecap="round"/>
<path d="M 120 400 Q 150 300 186 222" fill="none" stroke="${R}" stroke-width="8" marker-end="url(#ah${s})"/></svg>
<div class="lb" style="left:${250*s}px;top:${88*s}px;font-size:${40*s}px;color:${Y}">パッドの高さ</div>
<div class="lb" style="left:${20*s}px;top:${400*s}px;font-size:${42*s}px;color:#ff8fb1">この分を切る</div>`;
const annA=(s)=>`<svg viewBox="0 0 600 770" style="position:absolute;left:0;top:0;width:100%;height:100%"><defs><marker id="ai${s}" markerWidth="5" markerHeight="5" refX="2.5" refY="2.5" orient="auto-start-reverse" markerUnits="strokeWidth"><path d="M0,0 L5,2.5 L0,5 z" fill="${R}"/></marker></defs>
<line x1="150" y1="242" x2="590" y2="242" stroke="${R}" stroke-width="9" marker-start="url(#ai${s})" marker-end="url(#ai${s})"/>
<circle cx="308" cy="300" r="46" fill="none" stroke="${Y}" stroke-width="7"/>
<line x1="230" y1="560" x2="290" y2="344" stroke="${Y}" stroke-width="7"/></svg>
<div class="lb" style="left:${250*s}px;top:${148*s}px;font-size:${40*s}px;color:#ff8fb1">パッドの高さ</div>
<div class="lb" style="left:${20*s}px;top:${560*s}px;font-size:${40*s}px;color:${Y}">爪の先は、この線より下</div>`;
const play=(x,y,r)=>`<div style="position:absolute;left:${x-r}px;top:${y-r}px;width:${2*r}px;height:${2*r}px;border-radius:50%;background:${Y};border:5px solid ${D}"><div style="position:absolute;left:${r*0.78}px;top:${r*0.55}px;width:0;height:0;border-left:${r*0.8}px solid ${D};border-top:${r*0.45}px solid transparent;border-bottom:${r*0.45}px solid transparent"></div></div>`;
const endcard=`<div style="position:absolute;left:30px;top:0;width:990px;height:8px;background:${Y}"></div>
<div style="position:absolute;top:262px;width:1080px;text-align:center;font-size:62px;font-weight:900;line-height:1.38">爪切りは<br><span class="y">パッドの高さ</span>が目安</div>
<div class="ph" style="left:70px;top:470px;width:440px;height:565px"><img src="${U("raw_before.jpg")}">${annB(440/600)}<div class="tag" style="background:#fff;color:${D}">BEFORE</div></div>
<div class="ph" style="left:570px;top:470px;width:440px;height:565px"><img src="${U("raw_after.jpg")}">${annA(440/600)}<div class="tag" style="background:${Y};color:${D}">AFTER</div></div>
${play(540,750,32)}
<div style="position:absolute;top:1092px;width:1080px;text-align:center;font-size:44px;font-weight:900">切ったら、<span class="y">角に電動ヤスリ</span>で丸く</div>
<div style="position:absolute;top:1180px;width:1080px;text-align:center;font-size:32px;font-weight:700;color:#e9e1d8">保存して、次のカットの前に見返してね</div>`;
const th=[['th1','50% 45%','切る面を<br>目で測る'],['th2','45% 42%','パッドより<br>気持ち短く'],['th3','50% 40%','切った面の<br>角を落とす'],['th4','62% 30%','電動ヤスリを<br>角に当てる'],['th5','72% 45%','指でさわって<br>丸いか確認']];
const gift=`<div style="position:absolute;left:62px;top:70px;font-size:31px;letter-spacing:.16em;font-weight:500">CUT TECHNIQUE ／ @naohide_fujiwara</div>
<div style="position:absolute;left:60px;top:116px;padding:6px 20px;border-radius:10px;background:#c9573b;font-size:32px;font-weight:900">保存版・手順まとめ</div>
<div style="position:absolute;left:60px;top:190px;font-size:96px;font-weight:900;line-height:1.16;letter-spacing:.01em"><span class="y">パッドの高さ</span>より<br>気持ち短めに切る</div>
<div style="position:absolute;left:62px;top:436px;font-size:30px;color:#d9cfc6;font-weight:500">爪切りの手順（爪切り → 角取り → 電動ヤスリ）</div>
<div class="ph" style="left:50px;top:494px;width:470px;height:603px"><img src="${U("raw_before.jpg")}">${annB(470/600)}<div class="tag" style="background:#fff;color:${D};font-size:34px">BEFORE</div></div>
<div class="ph" style="left:560px;top:494px;width:470px;height:603px"><img src="${U("raw_after.jpg")}">${annA(470/600)}<div class="tag" style="background:${Y};color:${D};font-size:34px">AFTER</div></div>
${play(540,794,30)}
<div style="position:absolute;top:1118px;width:1080px;text-align:center;font-size:36px;font-weight:900">目安は <span class="y">パッドの高さ</span>・床に付かないくらい</div>
${th.map(([n,pos,t],i)=>`<div class="ph" style="left:${30+i*210}px;top:1180px;width:200px;height:240px;border-radius:14px"><img src="${U(n+"_full.jpg")}" style="object-position:${pos}"><div style="position:absolute;left:10px;top:10px;padding:2px 10px;border-radius:8px;background:#c9573b;font-size:26px;font-weight:900">0${i+1}</div></div><div style="position:absolute;left:${32+i*210}px;top:1434px;font-size:28px;font-weight:700;line-height:1.45">${t}</div>`).join('')}
<div style="position:absolute;top:1570px;width:1080px;text-align:center;font-size:52px;font-weight:900;line-height:1.4">爪切りは、<span class="y">パッドの高さ</span>が目安<br>切ったら角に電動ヤスリ</div>
<div style="position:absolute;top:1735px;width:1080px;text-align:center;font-size:32px;color:#d9cfc6;font-weight:500">保存して、次のカットの前に見返してね</div>`;
(async()=>{const b=await pw.chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:2});
for(const [n,h] of [['tejun_tsume_hq',gift]]){await p.setContent(`<html><head><style>${css}</style></head><body>${h}</body></html>`);await p.waitForTimeout(400);await p.screenshot({path:n+'.png'});}
await b.close();})();
