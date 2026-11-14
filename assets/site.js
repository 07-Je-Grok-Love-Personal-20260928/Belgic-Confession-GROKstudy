/* v4 目录：三级折叠（记忆状态）、拖宽（鼠标/触摸/笔，记忆宽度）、搜索过滤、滚动高亮、移动端抽屉 */
(function(){
var d=document,de=d.documentElement,nav=d.getElementById('toc');if(!nav)return;
var $=function(s,r){return (r||d).querySelector(s)},$$=function(s,r){return [].slice.call((r||d).querySelectorAll(s))};
var body=$('#tkbody'),grip=$('#tocgrip'),back=$('#tkback'),q=$('#tkq'),qn=$('#tkn'),none=$('.tk-none',nav);
var LS=window.localStorage,KO='tk4.open',KW='tk4.w',KM='tk4.wm',KH='tk4.hide';
function ld(k){try{return LS.getItem(k)}catch(e){return null}}function sv(k,v){try{if(v==null)LS.removeItem(k);else LS.setItem(k,v)}catch(e){}}
var wide=function(){return innerWidth>=1100};
function sidOf(li){var a=li.firstChild.lastChild;return a.getAttribute('data-s')}
/* ---------- 开合（每一级都可折叠，状态按 id 记忆） ---------- */
var open={};try{(JSON.parse(ld(KO))||[]).forEach(function(i){open[i]=1})}catch(e){}
var first=ld(KO)==null;
var items=$$('.tk-i.has',nav);
function setOpen(li,on,save){li.classList.toggle('open',!!on);var b=li.firstChild.firstChild;if(b&&b.tagName==='BUTTON')b.setAttribute('aria-expanded',on?'true':'false');var id=sidOf(li);if(on)open[id]=1;else delete open[id];if(save!==false)persist()}
var pt=0;function persist(){clearTimeout(pt);pt=setTimeout(function(){sv(KO,JSON.stringify(Object.keys(open)))},120)}
items.forEach(function(li){var id=sidOf(li);var on=first?li.classList.contains('is-cur'):!!open[id];if(on){li.classList.add('open');li.firstChild.firstChild.setAttribute('aria-expanded','true')}});
if(first){var c=$('.tk1.is-cur',nav);if(c)open[sidOf(c)]=1}
nav.addEventListener('click',function(e){
  var t=e.target.closest('.tk-tg');if(t){var li=t.closest('.tk-i');setOpen(li,!li.classList.contains('open'));e.preventDefault();return}
  var bt=e.target.closest('[data-tk]');if(bt){var k=bt.getAttribute('data-tk');
    if(k==='open')TK.expandAll();else if(k==='close')TK.collapseAll();else if(k==='cur')reveal(true);
    return}
  var a=e.target.closest('a');if(a&&!wide())hide();
});
/* ---------- 显示 / 隐藏 ---------- */
function isOpen(){return wide()?!de.classList.contains('tk-hide'):de.classList.contains('tk-open')}
function show(){if(wide()){de.classList.remove('tk-hide');sv(KH,null)}else{de.classList.add('tk-open');back.setAttribute('aria-hidden','false')}reveal(false)}
function hide(){if(wide()){de.classList.add('tk-hide');sv(KH,'1')}else{de.classList.remove('tk-open');back.setAttribute('aria-hidden','true')}}
function toggle(){isOpen()?hide():show()}
var tb=$('#tocbtn');if(tb)tb.addEventListener('click',toggle);$('#tocx').addEventListener('click',hide);back.addEventListener('click',hide);
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&!wide()&&de.classList.contains('tk-open'))hide()});
/* ---------- 拖宽 ---------- */
function lim(){return wide()?[240,Math.max(240,Math.min(760,innerWidth-420))]:[260,Math.max(260,innerWidth-12)]}
function curW(){return Math.round(nav.getBoundingClientRect().width)}
function clamp(v){var l=lim();return Math.max(l[0],Math.min(l[1],Math.round(v)))}
function aria(v){var l=lim();grip.setAttribute('aria-valuemin',l[0]);grip.setAttribute('aria-valuemax',l[1]);grip.setAttribute('aria-valuenow',v)}
function apply(v,save){v=clamp(v);de.style.setProperty(wide()?'--tkw':'--tkwm',v+'px');aria(v);if(save)sv(wide()?KW:KM,v);return v}
function reset(){de.style.removeProperty(wide()?'--tkw':'--tkwm');sv(wide()?KW:KM,null);aria(curW())}
var drag=null,raf=0,want=0;
grip.addEventListener('pointerdown',function(e){if(e.button>0)return;drag={x:e.clientX,w:curW(),id:e.pointerId};try{grip.setPointerCapture(e.pointerId)}catch(x){}de.classList.add('tk-drag');nav.style.width=drag.w+'px';e.preventDefault()});
grip.addEventListener('pointermove',function(e){if(!drag)return;want=clamp(drag.w+e.clientX-drag.x);if(!raf)raf=requestAnimationFrame(function(){raf=0;nav.style.width=want+'px';aria(want)})});
function end(){if(!drag)return;var v=want||drag.w;drag=null;cancelAnimationFrame(raf);raf=0;nav.style.width='';apply(v,true);de.classList.remove('tk-drag');want=0}
grip.addEventListener('pointerup',end);grip.addEventListener('pointercancel',end);grip.addEventListener('lostpointercapture',end);
grip.addEventListener('dblclick',reset);
grip.addEventListener('keydown',function(e){var st=e.shiftKey?64:16,v=curW(),l=lim();
  if(e.key==='ArrowLeft')v-=st;else if(e.key==='ArrowRight')v+=st;else if(e.key==='Home')v=l[0];else if(e.key==='End')v=l[1];else if(e.key==='Enter'){reset();return}else return;e.preventDefault();apply(v,true)});
var rt=0;addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){var v=curW(),c=clamp(v);if(c!==v)apply(c,false);else aria(v)},120)},{passive:true});
aria(curW());
/* ---------- 搜索过滤 ---------- */
var all=$$('.tk-i',nav).map(function(li){var t=li.firstChild.textContent;return {li:li,t:t.toLowerCase().replace(/\s+/g,'')}});
var qt=0;if(q)q.addEventListener('input',function(){clearTimeout(qt);qt=setTimeout(filter,90)});
function filter(){var s=(q.value||'').toLowerCase().replace(/\s+/g,'');
  if(!s){nav.classList.remove('tk-filter');all.forEach(function(o){o.li.classList.remove('m','mh')});qn.textContent='';none.hidden=true;return}
  nav.classList.add('tk-filter');var n=0;
  all.forEach(function(o){o.li.classList.remove('m','mh')});
  all.forEach(function(o){if(o.t.indexOf(s)>=0){n++;o.li.classList.add('m','mh');var p=o.li.parentElement.closest('.tk-i');while(p){p.classList.add('m');p=p.parentElement.closest('.tk-i')}}});
  qn.textContent=n?n+' 项':'0';none.hidden=n>0}
/* ---------- 滚动高亮（由 app.js 的观察器调用） ---------- */
var page=d.body.getAttribute('data-page'),links={};
$$('.tk1.is-cur a[data-s]',nav).forEach(function(a){links[a.getAttribute('data-s')]=a});
var cur=null;
function act(id){var a=links[id];if(!a||a===cur)return;
  if(cur){cur.classList.remove('on');cur.removeAttribute('aria-current')}
  $$('.tk-i.on-p',nav).forEach(function(x){x.classList.remove('on-p')});
  a.classList.add('on');a.setAttribute('aria-current','location');cur=a;
  var p=a.closest('.tk-i').parentElement.closest('.tk-i');while(p){p.classList.add('on-p');p=p.parentElement.closest('.tk-i')}
  if(isOpen())reveal(false)}
function visibleTarget(){if(!cur)return null;var t=cur,li=cur.closest('.tk-i');var p=li.parentElement.closest('.tk-i');
  while(p){if(!p.classList.contains('open'))t=p.querySelector('a');p=p.parentElement.closest('.tk-i')}return t}
var rv=0;function reveal(force){if(!cur)return;
  if(force){var p=cur.closest('.tk-i').parentElement.closest('.tk-i');while(p){setOpen(p,1,false);p=p.parentElement.closest('.tk-i')}persist()}
  cancelAnimationFrame(rv);rv=requestAnimationFrame(function(){var t=visibleTarget();if(!t)return;var br=body.getBoundingClientRect(),r=t.getBoundingClientRect();
    if(force||r.top<br.top+8||r.bottom>br.bottom-8)body.scrollTop+=r.top-br.top-br.height*0.35})}
var xa=0;window.TK={act:act,show:show,hide:hide,isOpen:isOpen,setWidth:function(v){return apply(v,false)},limits:lim,
  expandAll:function(sync){var q=items.filter(function(li){return li.classList.contains('has')&&!li.classList.contains('open')});cancelAnimationFrame(xa);
    if(sync||q.length<60){q.forEach(function(li){setOpen(li,1,false)});persist();return}
    var i=0;(function step(){var e=Math.min(q.length,i+48);for(;i<e;i++)setOpen(q[i],1,false);if(i<q.length)xa=requestAnimationFrame(step);else persist()})()},
  collapseAll:function(){cancelAnimationFrame(xa);items.forEach(function(li){setOpen(li,0,false)});persist()}};
})();

;(function(){
var d=document,b=d.body,rm=matchMedia('(prefers-reduced-motion: reduce)').matches,$=function(s,r){return (r||d).querySelector(s)},$$=function(s,r){return [].slice.call((r||d).querySelectorAll(s))};
var T=window.TEC||{pages:[]},PG=b.dataset.page,KEY='tfu1.read',QK='tfu1.quiz';
function ld(k,def){try{var v=JSON.parse(localStorage.getItem(k));return v==null?def:v}catch(e){return def}}
function sv(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
/* reveal */ /* v8 perf */
if(!rm&&'IntersectionObserver'in window){d.documentElement.classList.add('js');var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px'});$$('.reveal').forEach(function(el){io.observe(el)})}
/* toc：v4 见 toc4.js */
var wide=function(){return innerWidth>=1100};
var links={};$$('#toc .tk1.is-cur a[data-s]').forEach(function(a){links[a.getAttribute('data-s')]=a});
var secs=$$('section.l1[id],section.l2[id],section.l3[id]');
var rd=ld(KEY,{}),mine=rd[PG]||[];
function markRead(id){if(mine.indexOf(id)<0){mine.push(id);rd[PG]=mine;sv(KEY,rd);var a=links[id];if(a)a.classList.add('done');upd()}}
function upd(){var c=$('#pgread');if(c)c.textContent=mine.length}
mine.forEach(function(id){var a=links[id];if(a)a.classList.add('done')});
var cur=null,band=new Set(),order=new Map();secs.forEach(function(x,i){order.set(x,i)});
/* v4：跳过 content-visibility 尚未渲染的区块（位置是过期估计，会让高亮跳错） */
function live(x){return !x.checkVisibility||x.checkVisibility({contentVisibilityAuto:true})}
function setAct(id){if(id===cur)return;if(window.TK)TK.act(id);cur=id}
if('IntersectionObserver'in window){
 var ioA=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)band.add(e.target);else band.delete(e.target)});var best=null,bi=-1;var lim=Math.max(88,innerHeight*.14);band.forEach(function(x){var i=order.get(x);if(i>bi&&live(x)&&x.getBoundingClientRect().top<=lim){bi=i;best=x}});if(!best)band.forEach(function(x){var i=order.get(x);if(i>bi&&live(x)){bi=i;best=x}});if(best)setAct(best.id)},{rootMargin:'0px 0px -75% 0px'});
 var ioR=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){markRead(e.target.id);ioR.unobserve(e.target)}})},{rootMargin:'0px 0px -40% 0px'});
 secs.forEach(function(x){ioA.observe(x);if(x.classList.contains('l2'))ioR.observe(x)})}
var p=$('#prog'),H=0,de=d.documentElement;function measure(){H=Math.max(1,de.scrollHeight-innerHeight)}measure();
if('ResizeObserver'in window)new ResizeObserver(function(){measure();prog()}).observe(b);addEventListener('resize',measure,{passive:true});
var SDA=!rm&&window.CSS&&CSS.supports&&CSS.supports('animation-timeline: scroll()');function prog(){if(SDA)return;if(p)p.style.transform='scaleX('+Math.min(1,scrollY/H).toFixed(4)+')'}
var tk=0;addEventListener('scroll',function(){if(!tk){tk=1;requestAnimationFrame(function(){prog();tk=0})}},{passive:true});prog();upd();

/* counters */
var cs=$$('[data-count]');if(!rm&&cs.length){cs.forEach(function(c){var n=+c.dataset.count,t0=null;c.textContent='0';function st(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/1400);c.textContent=Math.round(n*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(st);else c.textContent=n}requestAnimationFrame(st);setTimeout(function(){c.textContent=n},2500)})}
/* tabs: scroll active into view */
var ta=$('.ptabs a.on');if(ta&&ta.parentNode)ta.parentNode.scrollLeft=Math.max(0,ta.offsetLeft-20);
/* exegesis open/close */
$$('[data-open]').forEach(function(x){x.onclick=function(){x.parentNode.previousElementSibling.querySelectorAll('details').forEach(function(e){e.open=true})}});
$$('[data-close]').forEach(function(x){x.onclick=function(){x.parentNode.previousElementSibling.querySelectorAll('details').forEach(function(e){e.open=false})}});
/* readers */
$$('[data-reader]').forEach(function(r){var zs=$$('.zh',r);
$$('[data-mode]',r).forEach(function(btn){btn.onclick=function(){var m=btn.dataset.mode;$$('[data-mode]',r).forEach(function(o){o.classList.toggle('ghost',o!==btn)});zs.forEach(function(z){z.classList.remove('masked','cue');if(m==='hide')z.classList.add('masked');if(m==='cue')z.classList.add('cue')})}});
$$('.verses li',r).forEach(function(li){li.onclick=function(){var z=$('.zh',li);if(z.classList.contains('masked')||z.classList.contains('cue'))z.classList.remove('masked','cue');else z.classList.add('masked')}})});
/* flip cards */
var fc=$('#fc'),seen={};$$('.flip').forEach(function(f,i){f.onclick=function(){f.classList.toggle('on');f.setAttribute('aria-pressed',f.classList.contains('on'));seen[i]=1;if(fc)fc.textContent=Object.keys(seen).length}});
/* quiz */
var qs=$('#qs');function score(){var n=$$('.opt.ok.picked').length;if(qs)qs.textContent=n;if(qs)sv(QK,{s:n,t:$$('.qq').length,d:$$('.qq').filter(function(q){return q.dataset.done}).length})}
$$('.qq').forEach(function(q){var a=+q.dataset.ans;$$('.opt',q).forEach(function(o){o.onclick=function(){if(q.dataset.done)return;q.dataset.done=1;var i=+o.dataset.i;o.classList.add('picked',i===a?'ok':'no');$$('.opt',q)[a].classList.add('ok');score()}})});
var qr=$('#qreset');if(qr)qr.onclick=function(){$$('.qq').forEach(function(q){delete q.dataset.done;$$('.opt',q).forEach(function(o){o.classList.remove('ok','no','picked')})});score()};
/* layers slider */
$$('[data-layers]').forEach(function(w){var r=$('input[type=range]',w),o=$('output',w),g=$('.lyrgrid',w),names=['只看第1层：使徒信经','叠到第2层：加上尼西亚新增','三层全开'];
function ap(){var v=+r.value;$$('.lyi',w).forEach(function(i){i.classList.toggle('off',+i.dataset.l>v)});if(o)o.textContent=names[v-1];w.dataset.v=v}
r.addEventListener('input',ap);ap()});
/* venn */
$$('.venn .vr').forEach(function(g){function go(){var t=d.getElementById('vreg-'+g.dataset.r);if(!t)return;t.scrollIntoView({behavior:rm?'auto':'smooth',block:'center'});$$('.vreg.hl').forEach(function(x){x.classList.remove('hl')});t.classList.add('hl');setTimeout(function(){t.classList.remove('hl')},2200)}
g.addEventListener('click',go);g.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();go()}})});
/* dort layers tabs */
$$('[data-dl]').forEach(function(w){var ps=$$('.dpan',w),ns=$$('.dnav a',w);if(!ps.length)return;w.classList.add('dl-js');function show(id){var ok=false;ps.forEach(function(p){var on=p.id===id;p.classList.toggle('on',on);if(on)ok=true});ns.forEach(function(a){a.classList.toggle('on',a.dataset.p===id)});return ok}
ns.forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();show(a.dataset.p)})});
function hash(){var h=location.hash.slice(1);if(h&&d.getElementById(h)&&w.contains(d.getElementById(h))&&d.getElementById(h).classList.contains('dpan')){show(h);d.getElementById(h).scrollIntoView()}}
show(ps[0].id);hash();addEventListener('hashchange',hash)});
/* recite */
$$('[data-rtool]').forEach(function(tb){var rc=tb.nextElementSibling;if(!rc||!rc.hasAttribute('data-recite'))return;var ls=$$('.rls li',rc),timer=null,i=0,btn=$('[data-rplay]',tb);
function mode(m){rc.classList.remove('m-hide','m-cue');ls.forEach(function(l){l.classList.remove('show')});if(m==='hide')rc.classList.add('m-hide');if(m==='cue')rc.classList.add('m-cue');$$('[data-rm]',tb).forEach(function(x){x.classList.toggle('ghost',x.dataset.rm!==m)})}
$$('[data-rm]',tb).forEach(function(x){x.onclick=function(){stop();mode(x.dataset.rm)}});
ls.forEach(function(l){l.addEventListener('click',function(){if(rc.classList.contains('m-hide')||rc.classList.contains('m-cue'))l.classList.toggle('show')})});
function stop(){if(timer){clearInterval(timer);timer=null}ls.forEach(function(l){l.classList.remove('now')});if(btn)btn.textContent='▶ 跟读'}
function step(){ls.forEach(function(l){l.classList.remove('now')});if(i>=ls.length){stop();return}var l=ls[i++];l.classList.add('now');l.classList.add('show');var r=l.getBoundingClientRect();if(r.top<80||r.bottom>innerHeight-60)l.scrollIntoView({block:'center',behavior:rm?'auto':'smooth'})}
if(btn)btn.onclick=function(){if(timer){stop();return}i=0;var sp=+($('[data-rspeed]',tb).value)||1700;btn.textContent='■ 停止';step();timer=setInterval(step,sp)}});
/* mastery */
(function(){var MK='tfu1.mas',m=ld(MK,{});var items=$$('.mi[data-k]');if(!items.length&&!$$('.cseg').length)return;
function paint(){items.forEach(function(e){var k=e.dataset.k,on=!!m[k];e.classList.toggle('done',on);var c=$('input',e);if(c)c.checked=on});
$$('[data-mring]').forEach(function(r){var p=r.dataset.mring,all=items.filter(function(e){return e.dataset.k.indexOf(p)===0}),n=all.filter(function(e){return m[e.dataset.k]}).length;var a=$('.mn1',r),z=$('.mn2',r),f=$('.rf',r);if(a)a.textContent=n;if(z)z.textContent=all.length;if(f)f.setAttribute('stroke-dasharray',(all.length?n/all.length*100:0)+' 100')});
$$('.cseg').forEach(function(s){s.classList.toggle('done',!!m['hc'+s.dataset.n])})}
items.forEach(function(e){var c=$('input',e);if(c)c.onchange=function(){if(c.checked)m[e.dataset.k]=1;else delete m[e.dataset.k];sv(MK,m);paint()}});paint()})();
/* index progress */
var steps=$$('.step');if(steps.length){var tot=0,got=0;(T.pages||[]).forEach(function(p){var n=p.n,c=(rd[p.k]||[]).length;if(c>n)c=n;tot+=n;got+=c;var st=$('.step[data-pg="'+p.k+'"]');if(st){var i=$('.bar i',st),e=$('.pc',st);if(i)i.style.width=(n?c/n*100:0)+'%';if(e)e.textContent=c?(c>=n?'✓ 已读完':'已读 '+c+'/'+n):'未读';if(c>=n&&n)st.classList.add('done')}});
var pct=tot?Math.round(got/tot*100):0;var rf=$('#ringf'),rn=$('#ringn');if(rf)rf.setAttribute('stroke-dasharray',pct+' 100');if(rn)rn.textContent=pct+'%';var a=$('#readn'),z=$('#readt');if(a)a.textContent=got;if(z)z.textContent=tot;
var q=ld(QK,null),qe=$('#quizs');if(qe&&q)qe.textContent=q.s+' / '+q.t+(q.d<q.t?'（未答完）':'');
var rp=$('#resetp');if(rp)rp.onclick=function(){try{localStorage.removeItem(KEY);localStorage.removeItem(QK)}catch(e){}location.reload()}}

/* v6 辅助区块：目录/链接/哈希跳转时自动展开所在的 <details>；全部展开/收起 */
(function(){function openFor(el){var o=false,p=el;while(p&&p!==d.body){if(p.tagName==='DETAILS'&&!p.open){p.open=true;o=true}p=p.parentElement}return o}
function tgt(h){if(!h)return null;try{h=decodeURIComponent(h)}catch(e){}return d.getElementById(h)}
function go(){var t=tgt(location.hash.slice(1));if(t&&openFor(t)){setTimeout(function(){t.scrollIntoView()},40);setTimeout(function(){t.scrollIntoView()},400)}}
addEventListener('hashchange',go);go();
d.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href*="#"]');if(!a)return;var h=a.getAttribute('href'),i=h.indexOf('#');if(i<0)return;var f=h.slice(0,i);if(f&&f!==location.pathname.split('/').pop())return;var t=tgt(h.slice(i+1));if(t)openFor(t)});
$$('[data-secall]').forEach(function(x){x.onclick=function(){var on=x.dataset.secall==='open';$$('details.secd').forEach(function(e){e.open=on})}});
})();
})();
/* ===== v7 START ===== */
(function(){var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
document.querySelectorAll('[data-sline]').forEach(function(box){var st=[].slice.call(box.querySelectorAll('.sl-st')),n=st.length,cur=-1,tm=null,bar=box.querySelector('.sl-bar i'),pos=box.querySelector('.sl-pos'),pb=box.querySelector('[data-sl=play]');
 function show(i){cur=(i+n)%n;st.forEach(function(s,j){s.classList.toggle('on',j===cur);s.classList.toggle('done',j<cur)});if(bar)bar.style.setProperty('--p',(n>1?cur/(n-1)*100:100)+'%');if(pos)pos.textContent=(cur+1)+' / '+n}
 function stop(){if(tm){clearInterval(tm);tm=null}if(pb)pb.textContent='▶ 播放'}
 function play(){stop();if(cur>=n-1)show(0);else show(cur+1);if(pb)pb.textContent='⏸ 暂停';tm=setInterval(function(){if(cur>=n-1){stop();return}show(cur+1)},rm?3200:2300)}
 box.classList.add('armed');show(0);
 box.addEventListener('click',function(e){var b=e.target.closest('[data-sl]');if(!b)return;var a=b.getAttribute('data-sl');if(a==='play'){tm?stop():play()}else{stop();show(cur+(a==='next'?1:-1))}});
 st.forEach(function(s,j){s.addEventListener('click',function(e){if(e.target.closest('a'))return;stop();show(j)})});
 if(!rm&&'IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){io.disconnect();play()}})},{threshold:.35});io.observe(box)}
});})();
/* ===== v7 END ===== */

/* v8 笔记标记开关（存于本机浏览器） */
(function(){var de=document.documentElement,K='mk.off';function paint(){var off=de.classList.contains('mkoff');document.querySelectorAll('[data-mktog]').forEach(function(b){b.setAttribute('aria-pressed',String(!off));b.textContent=off?'标记：关':'标记：开'})}
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-mktog]');if(!b)return;de.classList.toggle('mkoff');try{localStorage.setItem(K,de.classList.contains('mkoff')?'1':'0')}catch(x){}paint()});paint()})();

;/* t87：主题切换 + 背诵版全部展开/收起 */
(function(){var d=document,de=d.documentElement,K='ui.theme',C={night:'#070d22',dawn:'#f7f1e6',jade:'#03201e',ocean:'#04182b',grape:'#140a26',parch:'#f3e9d2'};
var box=d.getElementById('thm'),btn=d.getElementById('thmb');
function cur(){return de.getAttribute('data-theme')||'night'}
function mark(){[].forEach.call(d.querySelectorAll('[data-theme-set]'),function(b){b.setAttribute('aria-checked',b.getAttribute('data-theme-set')===cur())})}
function set(t){de.classList.add('thx');if(t==='night')de.removeAttribute('data-theme');else de.setAttribute('data-theme',t);try{localStorage.setItem(K,t)}catch(e){}var m=d.querySelector('meta[name="theme-color"]');if(m)m.setAttribute('content',C[t]);mark();clearTimeout(set._t);set._t=setTimeout(function(){var r=function(){de.classList.remove('thx')};if(window.requestIdleCallback)requestIdleCallback(r,{timeout:3000});else r()},600)}
if(box&&btn){btn.addEventListener('click',function(e){e.stopPropagation();var o=box.classList.toggle('open');btn.setAttribute('aria-expanded',o)});
 [].forEach.call(d.querySelectorAll('[data-theme-set]'),function(b){b.addEventListener('click',function(){set(b.getAttribute('data-theme-set'));box.classList.remove('open');btn.setAttribute('aria-expanded','false')})});
 d.addEventListener('click',function(e){if(!box.contains(e.target)){box.classList.remove('open');btn.setAttribute('aria-expanded','false')}});
 d.addEventListener('keydown',function(e){if(e.key==='Escape'){box.classList.remove('open');btn.setAttribute('aria-expanded','false')}});mark()}
[].forEach.call(d.querySelectorAll('[data-rx]'),function(b){b.addEventListener('click',function(){var o=b.getAttribute('data-rx')==='open';[].forEach.call(d.querySelectorAll('details.rfx'),function(x){x.open=o})})});
})();
;(function(){var de=document.documentElement,K='ui.core';try{if(localStorage.getItem(K)==='1')de.classList.add('coreonly')}catch(x){}
function paint(){var on=de.classList.contains('coreonly');document.querySelectorAll('[data-coreonly]').forEach(function(b){b.setAttribute('aria-pressed',String(on));b.textContent=on?'只看核心：开':'只看核心：关'})}
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-coreonly]');if(!b)return;de.classList.toggle('coreonly');try{localStorage.setItem(K,de.classList.contains('coreonly')?'1':'0')}catch(x){}paint();b.scrollIntoView({block:'center'})});paint()})();

;/* 比利时信条深读：朗读、填空、交互地图 */
(function(){
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
/* TTS */
var syn=window.speechSynthesis,curEl=null;
if(!syn||!window.SpeechSynthesisUtterance){document.documentElement.classList.add('nospeech')}
function stop(){if(syn)syn.cancel();if(curEl)curEl.classList.remove('speaking');curEl=null}
document.addEventListener('click',function(e){
  var b=e.target.closest&&e.target.closest('[data-speak]');
  if(b&&syn){var el=$(b.dataset.speak);if(!el)return;stop();var c=el.cloneNode(true);$$('sup,.fnref',c).forEach(function(x){x.remove()});
    var txt=c.textContent.replace(/\s+/g,' ').trim(),parts=txt.match(/[^。！？；]{1,180}[。！？；]?/g)||[txt];
    var d=el.closest('details');if(d)d.open=true;curEl=el;el.classList.add('speaking');
    var vs=syn.getVoices().filter(function(v){return /zh[-_]?CN|cmn|Chinese/i.test(v.lang+v.name)});
    parts.forEach(function(p,i){var u=new SpeechSynthesisUtterance(p);u.lang='zh-CN';u.rate=.95;if(vs[0])u.voice=vs[0];if(i===parts.length-1)u.onend=function(){if(curEl===el){el.classList.remove('speaking');curEl=null}};syn.speak(u)});return}
  if(e.target.closest&&e.target.closest('[data-stop]')){stop();return}
  var z=e.target.closest&&e.target.closest('button.cz');
  if(z){var on=z.classList.toggle('on');z.textContent=on?z.dataset.a:'＿'.repeat(z.dataset.a.length)}
});
var ca=$('#czall'),ch=$('#czhide');
if(ca)ca.onclick=function(){$$('button.cz').forEach(function(z){z.classList.add('on');z.textContent=z.dataset.a})};
if(ch)ch.onclick=function(){$$('button.cz').forEach(function(z){z.classList.remove('on');z.textContent='＿'.repeat(z.dataset.a.length)})};
})();

;/* v4：锚点精确跳转。content-visibility 让远处区块只有估计高度，原生跳转会落偏；
   这里先强制渲染目标及其祖先，再逐帧校正（瞬时滚动，直到目标稳定在顶部）；用户一滚动/触摸就停止。 */
(function(){var raf=0,stop=0,d=document;
function off(el){return parseFloat(getComputedStyle(el).scrollMarginTop)||0}
function fix(id){var el;try{el=d.getElementById(decodeURIComponent(id))}catch(x){}if(!el)return;cancelAnimationFrame(raf);stop=0;
 [].forEach.call(d.querySelectorAll('.cv-on'),function(x){x.classList.remove('cv-on')});for(var p=el;p&&p!==d.body;p=p.parentElement)p.classList.add('cv-on');
 var ok=0,n=0,m=off(el);
 (function f(){if(stop)return;var t=el.getBoundingClientRect().top-m;
  if(Math.abs(t)>1.5){window.scrollTo({top:window.scrollY+t,behavior:'instant'});ok=0}else ok++;
  if(ok<6&&++n<120)raf=requestAnimationFrame(f)})()}
['wheel','touchstart','keydown'].forEach(function(e){addEventListener(e,function(){stop=1},{passive:true})});
d.addEventListener('click',function(e){if(e.defaultPrevented||e.button||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
 var a=e.target.closest&&e.target.closest('a[href*="#"]');if(!a||a.target)return;var u=new URL(a.href,location.href);
 if(u.pathname!==location.pathname||u.hash.length<2)return;var id;try{id=decodeURIComponent(u.hash.slice(1))}catch(x){return}
 if(!d.getElementById(id))return;e.preventDefault();
 if(location.hash!==u.hash){history.pushState(null,'',u.hash);try{dispatchEvent(new HashChangeEvent('hashchange'))}catch(x){}}
 fix(id)});
addEventListener('popstate',function(){if(location.hash.length>1)fix(location.hash.slice(1))});
if(location.hash.length>1){fix(location.hash.slice(1));addEventListener('load',function(){fix(location.hash.slice(1))})}
})();

;/* v3：本地 Leaflet + 多底图切换与自动回退；离线示意 SVG 始终可见 */
(function(){
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var TILES=[
  {id:'osm',n:'OpenStreetMap',url:'https://tile.openstreetmap.org/{z}/{x}/{y}.png',a:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',max:19},
  {id:'osmde',n:'OSM 德国',url:'https://tile.openstreetmap.de/{z}/{x}/{y}.png',a:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',max:18},
  {id:'osmfr',n:'OSM France',url:'https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png',s:'abc',a:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> / OSM France',max:20},
  {id:'hot',n:'OSM HOT',url:'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',s:'abc',a:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, HOT',max:20},
  {id:'carto',n:'CARTO 浅色',url:'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',s:'abcd',a:'&copy; OSM &copy; <a href="https://carto.com/attributions">CARTO</a>',max:20},
  {id:'voyager',n:'CARTO Voyager',url:'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png',s:'abcd',a:'&copy; OSM &copy; <a href="https://carto.com/attributions">CARTO</a>',max:20},
  {id:'dark',n:'CARTO 深色',url:'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png',s:'abcd',a:'&copy; OSM &copy; <a href="https://carto.com/attributions">CARTO</a>',max:20},
  {id:'esri',n:'Esri 街道',url:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',a:'Tiles &copy; Esri',max:19},
  {id:'topo',n:'Esri 地形',url:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',a:'Tiles &copy; Esri',max:19},
  {id:'sat',n:'Esri 卫星',url:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',a:'Tiles &copy; Esri',max:19},
  {id:'otm',n:'OpenTopoMap',url:'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',s:'abc',a:'&copy; OSM, SRTM &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (CC-BY-SA)',max:17},
  {id:'gaode',n:'高德（中国备用，GCJ-02 有偏移）',url:'https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',s:'1234',a:'&copy; 高德地图（GCJ-02 火星坐标，欧洲位置会偏移；仅作网络备用）',max:18}
];
var KEY='ui.tiles', st={ready:0,q:[]};
function loadLib(cb){
  if(window.L){st.ready=2;return cb()}
  if(st.ready===1){st.q.push(cb);return}
  st.ready=1;st.q.push(cb);
  var l=document.createElement('link');l.rel='stylesheet';l.href='assets/leaflet/leaflet.css';document.head.appendChild(l);
  var s=document.createElement('script');s.src='assets/leaflet/leaflet.js';s.async=true;
  s.onload=function(){st.ready=2;st.q.forEach(function(f){try{f()}catch(e){}});st.q=[]};
  s.onerror=function(){st.ready=0;st.q.forEach(function(f){try{f()}catch(e){}});st.q=[]};
  document.head.appendChild(s);
}
function pref(){try{var v=localStorage.getItem(KEY);if(v){for(var i=0;i<TILES.length;i++)if(TILES[i].id===v)return i}}catch(e){}return 0}
function save(id){try{localStorage.setItem(KEY,id)}catch(e){}}
function layerOf(i){
  var t=TILES[i];
  return L.tileLayer(t.url,{maxZoom:t.max||18,attribution:t.a,subdomains:t.s||'abc',updateWhenIdle:true,keepBuffer:2,className:'tl-'+t.id});
}
function attach(map, sel, stat, start){
  var cur=-1, lyr=null, loaded=0, tmr=0, auto=1, tries=0;
  function use(i, fromUser){
    i=((i%TILES.length)+TILES.length)%TILES.length;
    if(i===cur&&lyr)return;
    if(lyr){map.removeLayer(lyr);lyr=null}
    cur=i;loaded=0;tries++;
    if(sel)sel.value=TILES[i].id;
    if(stat)stat.textContent='正在加载「'+TILES[i].n+'」…';
    lyr=layerOf(i);
    lyr.on('tileload',function(){loaded++;if(stat&&loaded===1){stat.textContent='底图：'+TILES[i].n;save(TILES[i].id)}});
    lyr.on('tileerror',function(){if(auto&&loaded===0){clearTimeout(tmr);tmr=setTimeout(function(){if(loaded===0)fail()},400)}});
    lyr.addTo(map);
    clearTimeout(tmr);
    tmr=setTimeout(function(){if(loaded===0)fail()}, fromUser?8000:5500);
  }
  function fail(){
    if(!auto||loaded>0){if(stat&&loaded===0)stat.textContent='底图暂时无法显示，请换一个来源，或看左侧/上方示意图。';return}
    if(tries>=TILES.length){if(stat)stat.textContent='所有在线底图都未能加载。示意图仍可阅读。';auto=0;return}
    use(cur+1,false);
  }
  if(sel){
    TILES.forEach(function(t){var o=document.createElement('option');o.value=t.id;o.textContent=t.n;sel.appendChild(o)});
    sel.addEventListener('change',function(){auto=0;tries=0;use(TILES.findIndex(function(t){return t.id===sel.value}),true)});
  }
  use(start,false);
  return {switch:function(id){var i=TILES.findIndex(function(t){return t.id===id});if(i>=0)use(i,true)}};
}
function boot(box){
  if(box.dataset.ok)return;
  var js=$(box.getAttribute('data-src')||('script.mapdata[data-map="'+box.getAttribute('data-map')+'"]'));
  var wrap=box.closest('.livemap')||box.parentElement;
  var fail=function(msg){box.innerHTML='<p class="lfail">'+(msg||'交互地图未能加载。请看示意图与地点表——无需网络。')+'</p>';box.dataset.ok='fail'};
  if(!window.L){return fail('Leaflet 未能从本站加载。示意图仍可阅读。')}
  if(!js){return fail()}
  var d;try{d=JSON.parse(js.textContent)}catch(e){return fail()}
  box.dataset.ok=1;box.innerHTML='';
  var m=L.map(box,{scrollWheelZoom:false,worldCopyJump:true,zoomControl:true,attributionControl:true});
  var pts=[];(d.p||[]).forEach(function(p){pts.push([p.la,p.lo])});
  (d.r||[]).forEach(function(x){if(x&&x.length===2&&typeof x[0]==='number')pts.push(x)});
  if(d.view){m.setView(d.view,d.z||5)}else if(pts.length){m.setView(pts[0],5)}else m.setView([50.2,4.2],5);
  var sel=wrap&&wrap.querySelector('.tilesel');
  var stat=wrap&&wrap.querySelector('.mapstat');
  attach(m,sel,stat,pref());
  (d.lines||[]).forEach(function(ln){
    L.polyline(ln.latlngs,{color:ln.c||'#d4af37',weight:ln.w||3,dashArray:ln.dash||'6 8',opacity:.9}).addTo(m);
  });
  if(d.r&&d.r.length>1&&!(d.lines&&d.lines.length)){
    L.polyline(d.r,{color:'#d4af37',weight:3,dashArray:'6 8',opacity:.9}).addTo(m);
  }
  (d.p||[]).forEach(function(p){
    var r=p.k==='core'?11:p.k==='hub'?10:8;
    var c=L.circleMarker([p.la,p.lo],{radius:r,color:'#fff',weight:2,fillColor:p.c||'#d4af37',fillOpacity:.95}).addTo(m);
    c.bindPopup('<b>'+p.n+'</b><br>'+p.t);
    if(p.k==='core'||p.k==='hub')c.bindTooltip((p.n.split(' ')[0]||p.n),{permanent:true,direction:'right',offset:[8,0],className:'mtip'});
  });
  if(pts.length>1)try{m.fitBounds(pts,{padding:[28,28],maxZoom:d.maxZ||8})}catch(e){}
  m.on('focus',function(){m.scrollWheelZoom.enable()});
  m.on('blur',function(){m.scrollWheelZoom.disable()});
  setTimeout(function(){m.invalidateSize()},200);
  box._map=m;
}
function watch(){
  var els=$$('.livebox');
  if(!els.length)return;
  var go=function(el){loadLib(function(){boot(el)})};
  if(!('IntersectionObserver' in window)){els.forEach(go);return}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){io.unobserve(e.target);
    var boxes=e.target.classList.contains('livebox')?[e.target]:e.target.querySelectorAll('.livebox');
    boxes.forEach(go);
  }})},{rootMargin:'1200px'});
  els.forEach(function(el){io.observe(el.closest('section.l2')||el.closest('.mapduo')||el)});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',watch);else watch();
})();
