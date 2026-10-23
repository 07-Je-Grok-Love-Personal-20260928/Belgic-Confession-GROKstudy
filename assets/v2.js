/* v2：content-visibility 下的锚点校正（目标区块渲染后尺寸变化，自动对准） */
(function(){var tm=0,stop=0;
function fix(id){var el;try{el=document.getElementById(decodeURIComponent(id))}catch(x){}if(!el)return;clearInterval(tm);stop=0;var last=null,ok=0,n=0;
 tm=setInterval(function(){n++;var mt=parseFloat(getComputedStyle(el).scrollMarginTop)||0,t=el.getBoundingClientRect().top;
  if(stop||n>40){clearInterval(tm);return}
  if(last!==null&&Math.abs(t-last)<1){if(Math.abs(t-mt)>4){el.scrollIntoView({block:'start',behavior:'instant'});ok=0}else if(++ok>2)clearInterval(tm)}
  last=t},110)}
['wheel','touchstart','keydown'].forEach(function(e){addEventListener(e,function(){stop=1},{passive:true})});
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href*="#"]');if(!a)return;var u=new URL(a.href,location.href);
 if(u.pathname===location.pathname&&u.hash.length>1)setTimeout(function(){fix(u.hash.slice(1))},30)});
if(location.hash.length>1)addEventListener('load',function(){fix(location.hash.slice(1))});
})();
