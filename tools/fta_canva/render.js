const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const L=JSON.parse(fs.readFileSync('items.json'));const t=fs.readFileSync('tpl.html','utf8');const b=await chromium.launch();
for(const x of L){const p=await b.newPage({viewport:{width:x.w,height:x.h}});fs.writeFileSync('_p.html',t.replace(/__W__/g,x.w).replace(/__H__/g,x.h).replace('__P__',JSON.stringify(x)));await p.goto('file://'+process.cwd()+'/_p.html');await p.waitForTimeout(250);await p.screenshot({path:x.out,type:x.out.endsWith('.jpg')?'jpeg':'png',quality:x.out.endsWith('.jpg')?95:undefined});await p.close()}
await b.close()})();
