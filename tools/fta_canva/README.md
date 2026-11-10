# 生産性（FTA本体）：Canvaは絵だけ・ほかはジャービス（11/10 藤原さんの決定）
- Canva の generate-design で「文字なし・絵だけ」を頼む → create-design-from-candidate → export-design(jpg, width 1080)。
- 画像の取りこみ：ビルトインブラウザで export-download.canva.com のURLを開き、javascript で fetch→base64（window.__imgs）→ 戻り値をファイルに保存 → dec.py で jpg に戻す。
- 絵の部分だけ切り出して k1〜k8.png。car.html（カルーセル 1080×1350）に pages.json の見出し・説明を入れ、node rc.js で car_N.png。
- リール：carr.html（ドット・スワイプなし）→ rr.js → 1枚ずつ濃い緑 1080×1920 の真ん中にゆっくり寄りで置き、vl.txt を VOICEVOX:青山龍星（tools/voicevox/tts.py … 1.1 aoyama）で読む。
- Canvaの文字は使わない（日本語が崩れる）。人物・実店舗は入れない。
