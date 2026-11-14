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
})();
