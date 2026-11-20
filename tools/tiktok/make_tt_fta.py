# 生産性研究部門（@fta_trimming）の TikTok 用の動画を作る。
# 11/20 21:31 藤原さん「やってみるなどは出さずにティックトック用として作ってください」
#  - 「やってみる」「プレゼント」「コメントで」は入れない（元は YouTube 用の『保存の呼びかけ』の版＝ytPub を使う）
#  - YouTube の終わりの画面（チャンネル登録）は切り落とし、TikTok 用の終わりの画面（保存／フォロー @fta_trimming）を2.5秒足す
# 使い方: python3 make_tt_fta.py <元の動画> <出力> [最後から切り落とす秒数（ytPub なら 2.5、YouTube 前の版なら 0）]
import sys, subprocess, json, os, tempfile
src, out = sys.argv[1], sys.argv[2]
cut = float(sys.argv[3]) if len(sys.argv) > 3 else 2.6  # 11/20 21:40 YouTube の終わりの画面は約2.53秒。2.5だと1コマ残ったので2.6
tmp = tempfile.mkdtemp()
def run(c): subprocess.run(c, shell=True, check=True)
info = json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate','-of','json',src]))['streams'][0]
W, H, fps = info['width'], info['height'], info['r_frame_rate']
dur = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]))
keep = dur - cut
html = """<html><body style='margin:0'><div style='width:1080px;height:1920px;background:#24402f;font-family:"Noto Sans CJK JP",sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:#fff'>
<div style='margin-top:-220px;font-size:40px;letter-spacing:.12em;font-weight:900;color:#f6d77a'>FUJIWARA TRIMMING ACADEMY</div>
<div style='font-size:72px;font-weight:900;margin-top:46px;line-height:1.45'>💾 保存して、<br>見返してね</div>
<div style='margin-top:70px;background:#f6d77a;color:#24402f;border-radius:28px;padding:30px 50px;font-size:48px;font-weight:900;line-height:1.5'>フォローで<br>サロンの生産性を毎日</div>
<div style='margin-top:50px;font-size:46px;font-weight:900'>@fta_trimming</div>
</div></body></html>"""
open(f'{tmp}/e.html','w').write(html)
run(f"cd {tmp} && node -e \"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1080,height:1920}}}});await p.goto('file://{tmp}/e.html');await p.waitForTimeout(400);await p.screenshot({{path:'{tmp}/e.png'}});await b.close()}})()\"")
has_a = subprocess.run(['ffprobe','-v','error','-select_streams','a','-show_entries','stream=index','-of','csv=p=0',src],capture_output=True,text=True).stdout.strip()!=''
a0 = f"[0:a]atrim=0:{keep},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[a0]" if has_a else f"anullsrc=r=48000:cl=stereo,atrim=duration={keep}[a0]"
run(f"ffmpeg -v error -y -i '{src}' -loop 1 -t 2.5 -framerate {fps} -i {tmp}/e.png -f lavfi -t 2.5 -i anullsrc=r=48000:cl=stereo "
    f"-filter_complex \"[0:v]trim=0:{keep},setpts=PTS-STARTPTS,setsar=1,format=yuv420p[v0];[1:v]scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p,fps={fps}[v1];{a0};[2:a]aformat=channel_layouts=stereo[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]\" "
    f"-map '[v]' -map '[a]' -c:v libx264 -crf 14 -preset slow -profile:v high -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart '{out}'")
print('done', out, os.path.getsize(out), round(keep+2.5,2))
