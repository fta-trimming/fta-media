# YouTube ショート用：元の動画（インスタと同じ）の最後に、共通の終わりの画面（2.5秒・動きなし）を足す。
# 使い方: python3 make_yt.py <元の動画> <account: cut|fta> <出力> [gift:0|1]
import sys, subprocess, json, os, tempfile
src, acc, out = sys.argv[1], sys.argv[2], sys.argv[3]
gift = (sys.argv[4] == '1') if len(sys.argv) > 4 else True
tmp = tempfile.mkdtemp()
def run(c): subprocess.run(c, shell=True, check=True)
info = json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate','-of','json',src]))['streams'][0]
W, H = info['width'], info['height']; fps = info['r_frame_rate']
IG = {'cut':'@naohide_fujiwara','fta':'@fujiwara__trimming'}[acc]
on = {'cut':0,'fta':1}[acc]
chip = lambda i,txt,bg,fg: f"<div style='padding:14px 34px;border-radius:999px;font-size:42px;font-weight:900;background:{bg if on==i else '#ffffff'};color:{fg if on==i else '#8a8a8a'};border:4px solid {bg}'>{txt}</div>"
giftline = (f"<div style='margin-top:70px;background:#fff;border-radius:28px;padding:34px 40px;font-size:44px;font-weight:900;color:#24402f;line-height:1.5;box-shadow:0 8px 24px rgba(0,0,0,.08)'>🎁 プレゼントの受け取りは<br>インスタ <span style='color:#e0412f'>{IG}</span> の<br>リールに「やってみる」とコメント</div>") if gift else ""
html = f"""<html><body style='margin:0'><div style='width:1080px;height:1920px;background:#fbf7ec;font-family:"Noto Sans CJK JP",sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;position:relative'>
<div style='position:absolute;top:0;left:0;right:0;height:26px;background:linear-gradient(90deg,#2a1b14 0 50%,#24402f 50% 100%)'></div>
<div style='position:absolute;bottom:0;left:0;right:0;height:26px;background:linear-gradient(90deg,#2a1b14 0 50%,#24402f 50% 100%)'></div>
<div style='font-size:46px;letter-spacing:.12em;font-weight:900;color:#3b2418'>FUJIWARA TRIMMING ACADEMY</div>
<div style='font-size:64px;font-weight:900;color:#24402f;margin-top:30px;line-height:1.4'>カットの手順と、<br>サロンの生産性</div>
<div style='display:flex;gap:24px;margin-top:60px'>{chip(0,'✂ アタッチメントカット','#2a1b14','#f2d06b')}{chip(1,'📈 サロンの生産性','#24402f','#f6d77a')}</div>
{giftline}
<div style='margin-top:70px;font-size:48px;font-weight:900;color:#3b2418'>チャンネル登録で、毎日の続きが見られます</div>
</div></body></html>"""
open(f'{tmp}/e.html','w').write(html)
run(f"cd {tmp} && node -e \"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1080,height:1920}}}});await p.goto('file://{tmp}/e.html');await p.waitForTimeout(400);await p.screenshot({{path:'{tmp}/e.png'}});await b.close()}})()\"")
# 元の動画＋終わりの画面を1回だけ高画質で書き出す（音が無い動画は無音を足す）
has_a = subprocess.run(['ffprobe','-v','error','-select_streams','a','-show_entries','stream=index','-of','csv=p=0',src],capture_output=True,text=True).stdout.strip()!=''
a0 = "[0:a]aresample=48000,aformat=channel_layouts=stereo[a0]" if has_a else f"anullsrc=r=48000:cl=stereo,atrim=duration=0.1[a0x];[a0x]apad[a0p];[a0p]atrim=end=999[a0]"
dur = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]))
if not has_a: a0 = f"anullsrc=r=48000:cl=stereo,atrim=duration={dur}[a0]"
run(f"ffmpeg -v error -y -i '{src}' -loop 1 -t 2.5 -framerate {fps} -i {tmp}/e.png -f lavfi -t 2.5 -i anullsrc=r=48000:cl=stereo "
    f"-filter_complex \"[0:v]setsar=1,format=yuv420p[v0];[1:v]scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p,fps={fps}[v1];{a0};[2:a]aformat=channel_layouts=stereo[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]\" "
    f"-map '[v]' -map '[a]' -c:v libx264 -crf 12 -preset slow -profile:v high -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart '{out}'")
print('done', out, os.path.getsize(out))
