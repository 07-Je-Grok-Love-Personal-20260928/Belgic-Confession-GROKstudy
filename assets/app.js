(function(){
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

/* v4：重点标记悬停/长按提示其含义（与图例一致），首次悬停时才设置，零开销 */
(function(){var M={'mk-hl':'必背·荧光（核心句）','mk-core':'必背·荧光（核心句）','mk-u':'重点·金实线','mk-x':'难点·红波浪','mk-w':'误读·橙双线','mk-d':'年代·青点线','mk-a':'应用·绿底','mk-k':'术语·领域色','mk-ref':'经文·蓝虚线'};
document.addEventListener('pointerover',function(e){var t=e.target;if(!t.classList||t.title)return;for(var k in M){if(t.classList.contains(k)){t.title=M[k];break}}},{passive:true})})();
