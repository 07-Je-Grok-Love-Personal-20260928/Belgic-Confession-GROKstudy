/* v3：本地 Leaflet + 多底图切换与自动回退；离线示意 SVG 始终可见 */
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
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){io.unobserve(e.target);go(e.target)}})},{rootMargin:'700px'});
  els.forEach(function(el){io.observe(el.closest('.mapduo,.livemap,section.l2')||el)});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',watch);else watch();
})();
