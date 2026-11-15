const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
await p.goto('file://'+__dirname+'/nail.html');await p.waitForTimeout(500);
for(const i of [1,2,3,4]){await (await p.$('#p'+i)).screenshot({path:__dirname+`/nail_${i}.png`});}
await b.close()})();
