// インスタの投稿ページ（https://www.instagram.com/p/<code>/、ブラウザの幅 1280x900）で javascript_tool に貼って実行する。
// 返り値：{url,date,n,other:[{u:名前,t:いつ,x:コメント,r:本人が返信ずみか}]}。other は合言葉（自動DM）以外のコメント。
// 11/14 藤原さん「やってみる以外にコメント来ているものに返信してないものには警告を指令室から出して」
const S=ms=>new Promise(z=>setTimeout(z,ms));await S(3500);
for(let k=0;k<6;k++){const m=[...document.querySelectorAll('svg[aria-label="さらにコメントを読み込む"]')];if(!m.length)break;(m[0].closest('button,[role=button]')||m[0].parentElement).click();await S(1500)}
for(let k=0;k<3;k++){const b=[...document.querySelectorAll('span,div,button')].filter(e=>e.childElementCount===0&&/返信を見る/.test(e.textContent));if(!b.length)break;for(const x of b){x.click();await S(700)}}
const L=[...document.querySelectorAll('main a[href^="/"]')].filter(a=>a.textContent.trim()&&a.getAttribute('href')==='/'+a.textContent.trim()+'/');
const C=new Set();for(const a of L){let p=a;for(let i=0;i<14&&p;i++){p=p.parentElement;if(p)C.add(p)}}
let B=null,bs=0;for(const el of C){const k=[...el.children].filter(ch=>ch.querySelector('a[href^="/"]')&&(ch.innerText||'').split('\n').length>=3).length;if(k>bs&&!el.querySelector('h1')){B=el;bs=k}}
const O=[];const own=['fujiwara__trimming','naohide_fujiwara'];
if(B)for(const ch of B.children){const l=(ch.innerText||'').split('\n').map(s=>s.trim()).filter(s=>s);if(l.length<3||own.includes(l[0]))continue;O.push({u:l[0],t:l[1],x:l[2],r:l.slice(3).some(s=>own.includes(s))})}
({url:location.pathname,date:document.querySelector('main time')?.getAttribute('datetime'),n:O.length,other:O.filter(o=>!/やってみ|ほし|欲し|くださ|下さ|お願い|チェック表|手順まとめ|キット|カレンダー/.test(o.x))})
