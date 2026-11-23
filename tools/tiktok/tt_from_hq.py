# 生産性研究部門のリールの本番（hqPub：最後にプレゼントの場面がある版）から TikTok 用を作る。
# 11/23 17:50 藤原さん「次からは自動で予約になる様に」：ttPub も ytPub も無い日は、これで作る。
#  - 最後の場面（プレゼント・「やってみる」）の始まり＝後ろ45%の中で最後の「はっきりした場面の切りかわり」を見つけて、そこから後ろを切る
#  - そのあと make_tt_fta.py で TikTok 用の終わりの画面（保存／フォロー @fta_trimming）を2.5秒足す
# 使い方: python3 tt_from_hq.py <hqPub の動画> <出力>
import sys, subprocess, os, numpy as np
src, out = sys.argv[1], sys.argv[2]
dur = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]))
raw = subprocess.run(['ffmpeg','-v','error','-i',src,'-vf','fps=30,scale=108:192,format=gray','-f','rawvideo','-'],capture_output=True,check=True).stdout
a = np.frombuffer(raw,dtype=np.uint8).reshape(-1,192,108).astype(np.int16)
d = np.abs(a[1:]-a[:-1]).mean(axis=(1,2))
start = int(len(d)*0.55)
cuts = [ (i+1)/30 for i in range(start,len(d)) if d[i] > 8 ]
if not cuts: sys.exit('場面の切りかわりが見つかりません（止めて知らせる）')
t = cuts[-1]
if dur - t > 12 or dur - t < 3: sys.exit(f'最後の場面の長さがおかしい（{dur-t:.2f}秒。止めて知らせる）')
print('cut at', round(t,2), 'remove', round(dur-t,2))
here = os.path.dirname(os.path.abspath(__file__))
subprocess.run(['python3', os.path.join(here,'make_tt_fta.py'), src, out, f'{dur-t:.3f}'], check=True)
