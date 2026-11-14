/* v4：锚点精确跳转。content-visibility 让远处区块只有估计高度，原生跳转会落偏；
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
