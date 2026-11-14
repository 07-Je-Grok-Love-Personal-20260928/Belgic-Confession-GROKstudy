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
    if(k==='open')items.forEach(function(li){setOpen(li,1,false)});
    else if(k==='close')items.forEach(function(li){setOpen(li,0,false)});
    else if(k==='cur'){reveal(true)}
    persist();return}
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
window.TK={act:act,show:show,hide:hide,isOpen:isOpen,setWidth:function(v){return apply(v,false)},limits:lim,
  expandAll:function(){items.forEach(function(li){setOpen(li,1,false)});persist()},collapseAll:function(){items.forEach(function(li){setOpen(li,0,false)});persist()}};
})();
