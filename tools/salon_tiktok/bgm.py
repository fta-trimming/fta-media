# -*- coding: utf-8 -*-
"""OLLIE MAGIC 用のオリジナルBGM（自作・著作権なし・アコースティック）。
11/20 13:47 藤原さん「両方アコースティックで少しニュアンス変えて」「音が少し大きくて音声と被るのが気になる」
python3 bgm.py <style: dogs|spa|spa2|heal|orgel> <秒> <out.wav> [seed]
dogs = 明るいアコギのストローク＋口笛風メロディ（100BPM・C）
spa  = ゆったりしたナイロンギターの指弾き（76BPM・F）
seed で毎日少しずつ変わる（メロディの並び・コードの順・テンポ±3）。"""
import sys, numpy as np, wave
from scipy.signal import lfilter
SR = 48000
style, L, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
rng = np.random.default_rng(seed)
BPM = (100 if style == 'dogs' else 132 if style == 'spa2' else 58 if style == 'heal' else 66 if style == 'orgel' else 76) + int(rng.integers(-3, 4))
beat = 60 / BPM
N = int(SR * (L + 3))
mix = np.zeros((N, 2))

def hz(m): return 440 * 2 ** ((m - 69) / 12)

def add(sig, t, pan=0.0, g=1.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if i >= N or i < 0: return
    s = sig[:j - i] * g
    mix[i:j, 0] += s * (1 - pan * 0.8); mix[i:j, 1] += s * (1 + pan * 0.8)

def guitar(m, d=1.5, bright=0.5, decay=0.996):
    """ギターの弦（カープラス・ストロング）。bright が小さいほどナイロン弦のやわらかい音。"""
    f = hz(m); p = int(SR / f); n = int(SR * d)
    burst = rng.uniform(-1, 1, p)
    burst = lfilter([1 - bright], [1, -bright], burst)  # はじく強さ（やわらかさ）
    x = np.zeros(n); x[:p] = burst
    a = np.zeros(p + 2); a[0] = 1; a[p] = -0.5 * decay; a[p + 1] = -0.5 * decay
    y = lfilter([1], a, x)
    y = lfilter([0.6, 0.3], [1], y)  # 胴の響きの代わりの軽いこもり
    return y * np.minimum(1, np.arange(n) / 30)

def orgel(m, d=2.6):  # オルゴール（金属の櫛。倍音が早く消え、基音がやさしく長く残る）
    t = np.arange(int(SR * d)) / SR; f = hz(m)
    s = (np.sin(2*np.pi*f*t) * np.exp(-t*1.6) + 0.28*np.sin(2*np.pi*f*2.0*t)*np.exp(-t*4) + 0.12*np.sin(2*np.pi*f*3.0*t)*np.exp(-t*8)
         + 0.05*np.sin(2*np.pi*f*5.4*t)*np.exp(-t*20))
    return s * np.minimum(1, t / 0.003)

def whistle(m, d):  # 口笛風（やわらかい正弦波＋ゆれ）
    t = np.arange(int(SR * d)) / SR; f = hz(m)
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.2 * t) * np.minimum(1, t / 0.3)
    s = np.sin(2 * np.pi * f * np.cumsum(vib) / SR)
    return s * np.minimum(1, t / 0.06) * np.minimum(1, (d - t) / 0.12).clip(0)

if style == 'dogs':
    root = 60
    progs = [[(0, 'M'), (9, 'm'), (5, 'M'), (7, 'M')], [(0, 'M'), (7, 'M'), (9, 'm'), (5, 'M')], [(5, 'M'), (7, 'M'), (0, 'M'), (9, 'm')]]
else:
    root = 62 if style == 'spa2' else 64 if style == 'heal' else 67 if style == 'orgel' else 65
    progs = [[(0, 'M7'), (-3, 'm7'), (-7, 'M7'), (-5, '7')], [(0, 'M7'), (-7, 'M7'), (-3, 'm7'), (-5, 'sus')], [(-7, 'M7'), (-5, '7'), (0, 'M7'), (-3, 'm7')]]
prog = progs[seed % 3]
SH = {'M': [0, 4, 7, 12, 16], 'm': [0, 3, 7, 12, 15], 'M7': [0, 7, 11, 16, 19], 'm7': [0, 7, 10, 15, 19], '7': [0, 7, 10, 16, 19], 'sus': [0, 7, 12, 17, 19]}
scale = [0, 2, 4, 5, 7, 9, 11]

def melody_bar(r, q):
    """コードの音を中心に、短い口ずさむようなフレーズを作る。"""
    tones = [root + 12 + r + i for i in SH[q][:3]]
    rhythm = [[0, 1, 2, 3], [0, 1.5, 2, 3], [0, .5, 1, 2], [0, 2, 2.5, 3]][int(rng.integers(0, 4))]
    notes = []
    for k, bt in enumerate(rhythm):
        m = tones[int(rng.integers(0, 3))] + (12 if rng.random() < 0.25 else 0)
        while m > root + 31: m -= 12
        nxt = rhythm[k + 1] if k + 1 < len(rhythm) else 4
        notes.append((bt, m, (nxt - bt)))
    return notes

bar = (3 if style == 'spa2' else 4) * beat; nb = int(L / bar) + 2
mel = [melody_bar(*prog[b % 4]) for b in range(8)]
for b in range(nb):
    t0 = b * bar; r, q = prog[b % 4]; ch = [root - 12 + r + i for i in SH[q]]
    if style == 'dogs':
        # 明るいストローク（ダウン・ダウンアップ・アップダウンアップ）
        for off, down, g in [(0, 1, .9), (1, 1, .6), (1.5, 0, .45), (2.5, 0, .5), (3, 1, .6), (3.5, 0, .45)]:
            order = ch if down else ch[::-1]
            for k, m in enumerate(order):
                add(guitar(m, 1.0, bright=0.62, decay=0.993), t0 + off * beat + k * 0.011, -0.3, 0.10 * g)
        add(guitar(root - 24 + r, 1.6, 0.4, 0.995), t0, 0, 0.22)
        add(guitar(root - 24 + r + 7, 1.2, 0.4, 0.995), t0 + 2 * beat, 0, 0.16)
        if b >= 1:
            for (bt, m, ln) in mel[b % 8]: add(whistle(m, ln * beat * 0.92), t0 + bt * beat, 0.35, 0.085)
    elif style == 'orgel':
        # 11/20 15:47 藤原さん「この音楽は使わないでオルゴール系など」→ ゆっくりのオルゴール（櫛の音）＋とても薄い和音
        t = np.arange(int(SR * (bar + 2.5))) / SR; padsig = 0
        for m in [root - 12 + r + i for i in SH[q][1:4]]:
            f = hz(m); padsig = padsig + np.sin(2*np.pi*f*t) + 0.4*np.sin(2*np.pi*f*1.003*t)
        add(padsig * np.minimum(1, t / 1.8) * np.clip((bar + 2.5 - t) / 2.2, 0, 1) / 3, t0, 0, 0.035)
        for k, s in enumerate([0, 2, 3, 4, 2, 3]):
            add(orgel(ch[s] + 12, 2.6), t0 + k * beat * 2 / 3 + rng.uniform(0, .015), -0.35 + 0.12 * k, 0.11)
        for (bt, m, ln) in mel[b % 8][:3]: add(orgel(m + 12, 3.0), t0 + bt * beat, 0.15, 0.24)
    elif style == 'heal':
        # 11/20 15:09 藤原さん「もっと癒し系の音楽で」→ とてもゆっくり・音数少なめのナイロンギター＋やわらかい空気のような和音＋ときどき小さな鈴
        t = np.arange(int(SR * (bar + 2.5))) / SR; padsig = 0
        for m in [root - 12 + r + i for i in SH[q][1:4]]:
            f = hz(m); padsig = padsig + np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*f*1.004*t) + 0.25*np.sin(2*np.pi*f*2*t)
        env = np.minimum(1, t / 1.6) * np.clip((bar + 2.5 - t) / 2.0, 0, 1)
        add(padsig * env / 3, t0, 0, 0.05)
        add(guitar(root - 24 + r, 3.5, 0.22, 0.9985), t0, 0, 0.22)
        for k, s in enumerate([2, 3, 4, 3]):
            add(guitar(ch[s], 3.0, bright=0.2, decay=0.9985), t0 + (k + 1) * beat * 0.98 + rng.uniform(0, .02), -0.3 + 0.15 * k, 0.12)
        if b % 2 == 1:
            for (bt, m, ln) in mel[b % 8][:2]: add(guitar(m + 12, 3.0, bright=0.25, decay=0.999), t0 + bt * beat, 0.35, 0.13)
        if b % 4 == 3:
            tt = np.arange(int(SR * 2.5)) / SR; f = hz(root + 36 + SH[q][2])
            add(np.sin(2*np.pi*f*tt) * np.exp(-tt * 1.8) * np.minimum(1, tt / 0.01), t0 + 2.5 * beat, 0.5, 0.035)
    elif style == 'spa2':
        # 11/20 15:04「オプションの音楽を変えて」→ 3拍子のやさしいワルツ（低音＋2拍目3拍目に和音、上へ流れるアルペジオ）
        add(guitar(root - 24 + r, 2.4, 0.3, 0.997), t0, 0, 0.26)
        for k, bt in enumerate([1, 2]):
            for q2, m in enumerate(ch[2:5]): add(guitar(m, 1.4, 0.28, 0.996), t0 + bt * beat + q2 * 0.018, -0.3, 0.09)
        for k, s in enumerate([1, 2, 3, 4, 3, 2]):
            add(guitar(ch[s] + 12, 1.6, 0.25, 0.997), t0 + k * beat / 2 + 0.02, 0.35, 0.07)
        if b >= 2:
            for (bt, m, ln) in mel[b % 8][:3]:
                if bt < 3: add(guitar(m + 12, 2.2, 0.32, 0.998), t0 + bt * beat, 0.1, 0.17)
    else:
        # ナイロンギターの指弾き（低音→上の弦へ、8分音符のアルペジオ）
        pat = [0, 2, 3, 4, 1, 3, 2, 4]
        for k, s in enumerate(pat):
            add(guitar(ch[s], 2.2, bright=0.30, decay=0.9975), t0 + k * beat / 2 + rng.uniform(0, .012), -0.25 + 0.12 * s, 0.17 if k % 4 else 0.22)
        if b % 2 == 1 or b >= 4:  # 2本目のギターがやさしくメロディ
            for (bt, m, ln) in mel[b % 8][:3]: add(guitar(m + 12, 2.0, bright=0.35, decay=0.998), t0 + bt * beat, 0.4, 0.16)

# 部屋の響き（短い残響）
rev = np.zeros_like(mix)
for k, (ms, g) in enumerate([(23, .28), (41, .22), (67, .16), (97, .11), (139, .07), (191, .045)]):
    d = int(SR * ms / 1000); rev[d:] += mix[:-d][:, ::-1 if k % 2 else 1] * g
mix = mix + rev
mix = mix[:int(SR * L)]
t = np.arange(len(mix)) / SR
mix *= np.minimum(1, t / 0.8)[:, None] * np.clip((L - t) / 2.0, 0, 1)[:, None]
mix = mix / np.max(np.abs(mix)) * 0.89
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
print('ok', out, L, 'bpm', BPM)
