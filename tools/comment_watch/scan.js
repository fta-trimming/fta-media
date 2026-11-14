// インスタの投稿ページ（https://www.instagram.com/p/<code>/、ブラウザの幅 1280x900）で javascript_tool に貼って実行する。
// 返り値：{url,date,n,kw,other:[{u:名前,t:いつ,x:コメント,r:本人が自分で返信ずみか}]}
// other＝合言葉だけのコメント以外すべて（合言葉＋ほかの言葉も入っているものもふくむ）。kw＝合言葉だけのコメントの数。
// r は ManyChat の自動の返信（DMをお送りしました 等）を数えない。
// 11/14 藤原さん「やってみる以外にコメント来ているものに返信してないものには警告」「きた全てのコメントを出して、返信案も」「やってみると一緒にコメントしているものも全て」
const S=ms=>new Promise(z=>setTimeout(z,ms));await S(3500);
for(let k=0;k<6;k++){const m=[...document.querySelectorAll('svg[aria-label="さらにコメントを読み込む"]')];if(!m.length)break;(m[0].closest('button,[role=button]')||m[0].parentElement).click();await S(1500)}
for(let k=0;k<3;k++){const b=[...document.querySelectorAll('span,div,button')].filter(e=>e.childElementCount===0&&/返信を見る/.test(e.textContent));if(!b.length)break;for(const x of b){x.click();await S(700)}}
const L=[...document.querySelectorAll('main a[href^="/"]')].filter(a=>a.textContent.trim()&&a.getAttribute('href')==='/'+a.textContent.trim()+'/');
const C=new Set();for(const a of L){let p=a;for(let i=0;i<14&&p;i++){p=p.parentElement;if(p)C.add(p)}}
let B=null,bs=0;for(const el of C){const k=[...el.children].filter(ch=>ch.querySelector('a[href^="/"]')&&(ch.innerText||'').split('\n').length>=3).length;if(k>bs&&!el.querySelector('h1')){B=el;bs=k}}
const own=['fujiwara__trimming','naohide_fujiwara'];
const KW=/やってみる|やってみ|ほしい|欲しい|ください|下さい|お願いします|チェック表|手順まとめ|スタートキット|キット|カレンダー|メモキット/g;
const AUTO=/DMをお送りしました|DMをご確認ください|DMに送りました/;
const skip=s=>/^(返信|「いいね！」\d+件|\d+件すべての返信を見る|返信を非表示|.*前|\d+月\d+日|翻訳を見る|編集済み)$/.test(s);
const O=[];let kw=0;
if(B)for(const ch of B.children){const l=(ch.innerText||'').split('\n').map(s=>s.trim()).filter(s=>s);if(l.length<3||own.includes(l[0]))continue;
 const x=l[2];const rest=x.replace(KW,'').replace(/[\s\p{P}\p{S}\p{Emoji_Presentation}‍️]/gu,'');
 let real=false;for(let i=3;i<l.length;i++){if(own.includes(l[i])){for(let j=i+1;j<Math.min(l.length,i+4);j++){if(skip(l[j])||own.includes(l[j]))continue;if(!AUTO.test(l[j]))real=true;break}}}
 if(rest.length<2){kw++;continue}
 O.push({u:l[0],t:l[1],x,r:real})}
({url:location.pathname,date:document.querySelector('main time')?.getAttribute('datetime'),n:O.length+kw,kw,other:O})
