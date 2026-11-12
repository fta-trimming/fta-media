const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:794,height:1123},deviceScaleFactor:2160/794});
await p.goto('file://'+process.cwd()+'/kit.html');await p.waitForTimeout(400);
await p.pdf({path:'zangyo_kit.pdf',format:'A4',printBackground:true});
const pages=await p.$$('.page');for(let i=0;i<pages.length;i++){await pages[i].screenshot({path:`kit_${i+1}.png`})}
await b.close()})();
