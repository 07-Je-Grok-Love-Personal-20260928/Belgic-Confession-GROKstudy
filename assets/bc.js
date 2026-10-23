/* 比利时信条深读：朗读、填空、交互地图 */
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
/* Leaflet */
function initMap(){var box=$('#lmap'),dj=$('#lmapdata');if(!box||!dj||box.dataset.ok)return;
  if(!window.L){box.innerHTML='<p class="lfail">交互地图未能加载（可能离线或网络受限）。请看下方 SVG 示意图与地点表。</p>';return}
  box.dataset.ok=1;var d=JSON.parse(dj.textContent);
  var m=L.map(box,{scrollWheelZoom:false,worldCopyJump:false}).setView([50.2,4.2],6);
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> 贡献者'}).addTo(m);
  L.polyline(d.r,{color:'#d4af37',weight:3,dashArray:'6 8',opacity:.9}).addTo(m);
  var b=[];d.p.forEach(function(p){var r=p.k==='core'?11:8;var c=L.circleMarker([p.la,p.lo],{radius:r,color:'#fff',weight:2,fillColor:p.c,fillOpacity:.95}).addTo(m);
    c.bindPopup('<b>'+p.n+'</b><br>'+p.t);c.bindTooltip(p.n.split(' ')[0],{permanent:p.k==='core',direction:'right',offset:[8,0]});b.push([p.la,p.lo])});
  m.fitBounds(d.r,{padding:[24,24]});m.on('focus',function(){m.scrollWheelZoom.enable()});m.on('blur',function(){m.scrollWheelZoom.disable()});
  setTimeout(function(){m.invalidateSize()},300)}
var Lq=0;function loadL(cb){if(window.L)return cb();if(Lq)return;Lq=1;var c=document.createElement('link');c.rel='stylesheet';c.href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';c.integrity='sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=';c.crossOrigin='';document.head.appendChild(c);
  var j=document.createElement('script');j.src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';j.integrity='sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=';j.crossOrigin='';j.onload=cb;j.onerror=cb;document.head.appendChild(j)}
if($('#lmap')){if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){loadL(initMap);io.disconnect()}})},{rootMargin:'600px'});var t=$('#lmap');io.observe(t.closest('.l2')||t.closest('figure')||t)}else loadL(initMap)}
})();
