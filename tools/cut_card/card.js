const {chromium}=require('playwright');const fs=require('fs');
const cards=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(const c of cards){
const html=`<html><body style="margin:0;background:transparent;width:1080px;height:1920px;position:relative;font-family:'Noto Sans CJK JP'">
<div style="position:absolute;left:45px;top:96px;width:798px;height:255px;border-radius:20px;background:rgba(36,23,19,${c.alpha})"></div>
<div style="position:absolute;left:80px;top:123px;font-size:30px;font-weight:700;color:#f2d06b;letter-spacing:.06em;line-height:1">${c.label}</div>
<div style="position:absolute;left:80px;top:167px;font-size:60px;font-weight:700;color:#fff;line-height:78px;letter-spacing:.01em">${c.lines.join('<br>')}</div>
</body></html>`;
await p.setContent(html);await p.waitForTimeout(200);await p.screenshot({path:c.out,omitBackground:true});}
await b.close();})();
