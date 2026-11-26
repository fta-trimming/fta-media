import sys,asyncio
from playwright.async_api import async_playwright
from PIL import Image
async def main(src,out,h):
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1080,'height':h},device_scale_factor=2)
        await pg.goto('file://'+src); await pg.wait_for_timeout(500)
        await pg.screenshot(path=out+'.png',full_page=(h<1920))
        await b.close()
    im=Image.open(out+'.png').convert('RGB'); im.save(out,quality=95,subsampling=0)
    s=im.copy(); s.thumbnail((540,960)); s.save(out.replace('.jpg','_sm.jpg'))
asyncio.run(main(sys.argv[1],sys.argv[2],int(sys.argv[3]) if len(sys.argv)>3 else 1920))
