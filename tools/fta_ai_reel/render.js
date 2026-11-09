const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const T=fs.readFileSync('timing.json','utf8');let h=fs.readFileSync('reel.html','utf8').replace('__TIMING__',T);fs.writeFileSync('r.html',h);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+process.cwd()+'/r.html');await p.waitForTimeout(500);
const mode=process.argv[2];
if(mode==='preview'){const ts=JSON.parse(process.argv[3]);for(const t of ts){await p.evaluate(t=>setT(t),t);await p.screenshot({path:`pv_${t}.jpg`,type:'jpeg',quality:80})}}
else{fs.mkdirSync('fr',{recursive:true});const tot=JSON.parse(T).scenes.slice(-1)[0][1];const n=Math.ceil(tot*30);for(let i=0;i<n;i++){await p.evaluate(t=>setT(t),i/30);await p.screenshot({path:`fr/${String(i).padStart(5,'0')}.png`})}}
await b.close()})();
