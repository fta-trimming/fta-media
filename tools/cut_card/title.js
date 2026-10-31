// カット中心リール：はじめの縦書きタイトルカード（表紙）
// 10/31 藤原さんの指示「タイトルカードを前回（10/30）と同じ位置に。カードの大きさは変えずに、空白ができない様に文字を作る」
// 位置・大きさは毎回同じ：左 341px・上 438px・幅 398px・高さ 1026px（10/30 アタッチメントの回と同じ）
// 文字は列ごとにカードの高さいっぱいまで（上下の余白をそろえて）並べ、列はカードの幅いっぱいに広げる。
// 使い方: node tools/cut_card/title.js title.json
// title.json の例: {"label":"足先バリカン","cols":["手の甲の境目から","<y>爪まで</y>を刈る"],"out":"title.png","bg":"背景.png(任意)"}
//   <y>…</y> は黄色。label は右はしの小さい列（黄色）。cols は右から左の順。
const {chromium}=require('playwright');const fs=require('fs');
const c=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const BOX={left:341,top:438,w:398,h:1026};
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
const col=(t,cls)=>`<div class="col ${cls}">${t.replace(/<y>/g,'<span class="y">').replace(/<\/y>/g,'</span>')}</div>`;
const bg=c.bg?`background:url('data:image/png;base64,${fs.readFileSync(c.bg).toString('base64')}') 0 0/1080px 1920px;`:'background:transparent;';
const html=`<html><head><style>
body{margin:0;width:1080px;height:1920px;position:relative;${bg}font-family:'Noto Sans CJK JP';}
.box{position:absolute;left:${BOX.left}px;top:${BOX.top}px;width:${BOX.w}px;height:${BOX.h}px;border-radius:24px;background:rgba(36,23,19,.84);
 display:flex;flex-direction:row-reverse;justify-content:space-evenly;align-items:stretch;padding:44px 6px;box-sizing:border-box}
.col{writing-mode:vertical-rl;text-orientation:upright;font-weight:900;color:#fff;line-height:1;white-space:nowrap;height:100%}
.lab{color:#f2d06b;font-weight:700}
.y{color:#f2d06b}
</style></head><body><div class="box">${col(c.label,'lab')}${c.cols.map(t=>col(t,'main')).join('')}</div></body></html>`;
await p.setContent(html);await p.waitForTimeout(300);
await p.evaluate(()=>{
 const box=document.querySelector('.box');const H=box.clientHeight-88;const W=box.clientWidth-12;
 const len=e=>[...e.textContent].length;
 const mains=[...document.querySelectorAll('.main')];const lab=document.querySelector('.lab');
 const maxc=Math.max(...mains.map(len));
 let lf=Math.min(62,Math.floor(H/len(lab)*0.92));
 let F=Math.floor(Math.min(H/maxc, (W-lf*1.15)/(mains.length*1.12)));
 lab.style.fontSize=lf+'px';mains.forEach(m=>m.style.fontSize=F+'px');
 // 列ごとに字の間を広げて、高さいっぱいにそろえる（空白を作らない）
 for(const e of [lab,...mains]){const n=len(e);const fs=parseFloat(e.style.fontSize);
   const gap=(H-n*fs)/Math.max(n-1,1);e.style.letterSpacing=gap+'px';e.style.height='auto';
   // 最後の字の後ろの空きを消す
   e.style.marginBottom=(-gap)+'px';}
});
await p.waitForTimeout(150);
await p.screenshot({path:c.out,omitBackground:!c.bg});await b.close();})();
