// node render.js <dir> preview "[t1,t2]" | node render.js <dir> full [start] [end]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const d=process.argv[2],mode=process.argv[3];
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+process.cwd()+'/'+d+'/r.html');await p.waitForTimeout(500);
if(mode==='preview'){const ts=JSON.parse(process.argv[4]);for(const t of ts){await p.evaluate(t=>setT(t),t);await p.screenshot({path:`${d}/pv_${t}.jpg`,type:'jpeg',quality:80})}}
else{fs.mkdirSync(d+'/fr',{recursive:true});const tot=JSON.parse(fs.readFileSync(d+'/timing.json')).scenes.slice(-1)[0][1];const n=Math.ceil(tot*30);
const a=+(process.argv[4]||0),e=Math.min(n,+(process.argv[5]||n));
for(let i=a;i<e;i++){await p.evaluate(t=>setT(t),i/30);await p.screenshot({path:`${d}/fr/${String(i).padStart(5,'0')}.png`})}}
await b.close()})();
