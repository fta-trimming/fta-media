const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const P=JSON.parse(fs.readFileSync('pages.json'));const t=fs.readFileSync('car.html','utf8');const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(const x of P){fs.writeFileSync('_p.html',t.replace('__P__',JSON.stringify(x)));await p.goto('file://'+process.cwd()+'/_p.html');await p.waitForTimeout(300);await p.screenshot({path:`car_${x.n}.png`})}
await b.close()})();
