#!/usr/bin/env python3
"""その週の投稿の画像・動画・プレゼント・文章を、日付と時間のフォルダに分けて zip にまとめる。

使い方:
  python3 pack_week.py <週の月曜 YYYY-MM-DD> <postsのJSONフォルダ> <司令室の素材フォルダ> <fta-mediaのフォルダ> <出力zip>

- postsのJSONフォルダ: ArtifactData の query(out_dir) で保存した posts/*.json
- 司令室の素材フォルダ: Artifact read(path=<id>) で保存した <id>.<拡張子>（GitHub に無いファイル用）
- GitHub に置いてあるもの（files[].pub）は fta-media の中から取る（新しいほう）
"""
import json, os, re, sys, glob, shutil, zipfile, datetime

WD = '月火水木金土日'
PLAT = {'x': 'X', 'threads': 'Threads', 'instagram': 'インスタ', 'reel': 'リール', 'story': 'ストーリーズ', 'note': 'note'}
DEF_HM = {'story': '12:00', 'instagram': '18:00', 'reel': '18:00', 'x': '20:00', 'threads': '20:00'}
DM_MARK = '―――（ここから下は投稿しない）'
RAW = 'https://raw.githubusercontent.com/fta-trimming/fta-media/main/'


def hm(p):
    s = p.get('scheduledAt')
    ms = None
    if isinstance(s, (int, float)) and s:
        ms = s
    elif isinstance(s, str) and s:
        try:
            ms = datetime.datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp() * 1000
        except ValueError:
            ms = None
    if ms:
        d = datetime.datetime.fromtimestamp(ms / 1000 + 9 * 3600, datetime.timezone.utc)
        return f'{d.hour:02d}:{d.minute:02d}'
    if p.get('time'):
        h, m = (p['time'].split(':') + ['00'])[:2]
        return f'{int(h):02d}:{m[:2]}'
    return DEF_HM.get(p.get('platform'), '')


def safe(t, n=28):
    t = str(t or '').replace(':', '：').replace('/', '／')
    t = re.sub(r'[\\*?"<>|\n\r\t]', '', t).strip()
    t = re.sub(r'^(インスタ|Threads|X|ストーリーズ)\s*', '', t)
    return t[:n]


def main():
    week, pdir, adir, repo, out = sys.argv[1:6]
    mon = datetime.date.fromisoformat(week)
    sun = mon + datetime.timedelta(days=6)
    root = f'FTA_{mon:%Y-%m-%d}週（{mon.month}月{mon.day}日〜{sun.month}月{sun.day}日）'
    work = out + '.dir'
    shutil.rmtree(work, ignore_errors=True)
    base = os.path.join(work, root)
    os.makedirs(base)

    posts = []
    for f in glob.glob(os.path.join(pdir, '*.json')):
        d = json.load(open(f, encoding='utf8'))
        d = d.get('data', d)
        d['_id'] = os.path.basename(f)[:-5]
        if d.get('week') and d['week'] != week:
            continue
        if d.get('status') == 'skipped':
            continue
        posts.append(d)

    def key(p):
        t = hm(p) or ('07:00' if p.get('platform') == 'note' else '23:00')
        return (p.get('date', ''), t, p.get('order') or 0)
    posts.sort(key=key)

    assets = {os.path.splitext(os.path.basename(x))[0]: x for x in glob.glob(os.path.join(adir, '*'))}
    gifts, index, missing, count = set(), [], [], {}

    def src_of(fi):
        pub = (fi.get('pub') or '').split('?')[0]
        if pub.startswith(RAW):
            path = os.path.join(repo, pub[len(RAW):])
            if os.path.exists(path):
                return path
        if fi.get('id') in assets:
            return assets[fi['id']]
        for sub in ('', 'stories'):
            path = os.path.join(repo, week, sub, fi.get('name') or '-')
            if os.path.exists(path):
                return path
        return None

    for p in posts:
        d = datetime.date.fromisoformat(p['date'])
        t = hm(p)
        plat = PLAT.get(p.get('platform'), p.get('platform', ''))
        title = p.get('title') or ''
        if 'カルーセル' in title and p.get('platform') == 'instagram':
            plat = 'カルーセル②' if 'カルーセル②' in title or 'carousel2' in p['_id'] else 'カルーセル①'
        if p.get('platform') == 'instagram' and any(x.get('kind') == 'video' for x in p.get('files') or []):
            plat = 'リール'
        k = (p['date'], t, plat)
        count[k] = count.get(k, 0) + 1
        folder = f"{d:%m-%d}（{WD[d.weekday()]}）_{t.replace(':', '時') + '分' if t else '自分で公開'}_{plat}" + (f'_{count[k]}' if count[k] > 1 else '') + f"_{safe(title)}"
        fdir = os.path.join(base, folder)
        os.makedirs(fdir, exist_ok=True)
        text = p.get('text') or ''
        i = text.find(DM_MARK)
        pub_text, dm = (text[:i].strip(), text[i + len(DM_MARK):].strip()) if i >= 0 else (text.strip(), '')
        if p.get('dmText'):
            dm = p['dmText']
        open(os.path.join(fdir, '投稿文.txt'), 'w', encoding='utf8').write(pub_text + '\n')
        if dm:
            open(os.path.join(fdir, 'DMの返信文.txt'), 'w', encoding='utf8').write(dm + ('\n\nページ：' + p['dmUrl'] if p.get('dmUrl') else '') + '\n')
        nfile = 0
        for n, fi in enumerate(p.get('files') or [], 1):
            if 'DMプレゼント' in (fi.get('label') or ''):
                pub = (fi.get('pub') or '').split('?')[0]
                if pub.startswith(RAW):
                    gifts.add(os.path.dirname(pub[len(RAW):]))
                continue
            s = src_of(fi)
            if not s:
                missing.append(f"{folder}/{fi.get('name')}")
                continue
            name = fi.get('name') or os.path.basename(s)
            if not os.path.splitext(name)[1]:
                name += os.path.splitext(s)[1]
            shutil.copy(s, os.path.join(fdir, f'{n:02d}_{name}'))
            nfile += 1
        index.append(f"{d.month}/{d.day}（{WD[d.weekday()]}） {t or '自分で'}  {plat}  {title}  ［画像・動画 {nfile}点］")

    for g in sorted(gifts):
        gd = os.path.join(repo, g)
        if not os.path.isdir(gd):
            continue
        name = {'shinjin': '新人育成セルフチェック表', 'solo': '一人サロン任せる準備キット'}.get(os.path.basename(g), os.path.basename(g))
        dst = os.path.join(base, '00_DMプレゼント', name)
        os.makedirs(dst, exist_ok=True)
        for x in sorted(os.listdir(gd)):
            shutil.copy(os.path.join(gd, x), dst)

    head = [f'{root}', '', '投稿日・時間の順に、フォルダを分けています。', '各フォルダに「投稿文.txt」と、使った画像・動画が入っています。', 'DMで渡したプレゼントは「00_DMプレゼント」にあります。', '']
    if missing:
        head += ['見つからなかったファイル：'] + missing + ['']
    open(os.path.join(base, '00_一覧.txt'), 'w', encoding='utf8').write('\n'.join(head + index) + '\n')

    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for dp, _, fs in os.walk(work):
            for f in sorted(fs):
                full = os.path.join(dp, f)
                z.write(full, os.path.relpath(full, work))
    shutil.rmtree(work)
    print(out, os.path.getsize(out), 'posts', len(posts), 'missing', len(missing))


if __name__ == '__main__':
    main()
