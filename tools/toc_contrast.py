"""v4：目录文字对比度（6 主题；含当前项 a.on 与一级徽章）。"""
import os
from playwright.sync_api import sync_playwright
JS='''()=>{function rgb(s){const m=s.match(/[\\d.]+/g);return m?m.map(Number):null}
function lum(c){const a=c.slice(0,3).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*a[0]+.7152*a[1]+.0722*a[2]}
function bg(el){for(let e=el;e;e=e.parentElement){const c=getComputedStyle(e);const bi=c.backgroundImage;if(bi&&bi!=='none'){const m=bi.match(/rgba?\\([^)]+\\)|hsla?\\([^)]+\\)/);if(m){const t=document.createElement('i');t.style.color=m[0];document.body.appendChild(t);const v=rgb(getComputedStyle(t).color);t.remove();if(v&&(v[3]===undefined||v[3]>.5))return v}}
 const b=rgb(c.backgroundColor);if(b&&(b[3]===undefined||b[3]>.5))return b}return [0,0,0]}
const out=[];document.querySelectorAll('#toc .tk-t, #toc .tk-n, #toc .tk-head button, #toc .tk-home').forEach(el=>{if(!el.offsetParent)return;const f=rgb(getComputedStyle(el).color),b=bg(el);
 const L1=lum(f),L2=lum(b),r=(Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05);if(r<4.5)out.push((el.className+':'+el.textContent.trim().slice(0,8)+' '+r.toFixed(2)))});return out}'''
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for th in ('night','dawn','jade','ocean','grape','parch'):
        ctx=b.new_context(viewport={'width':1280,'height':900}); ctx.add_init_script("localStorage.setItem('ui.theme','%s')"%th)
        pg=ctx.new_page(); pg.goto('file://'+os.path.abspath('bc.html')); pg.wait_for_timeout(700); pg.evaluate("TK.expandAll(true)")
        pg.evaluate("document.getElementById('bx-3').scrollIntoView()"); pg.wait_for_timeout(800)
        r=pg.evaluate(JS); print(th,len(r),r[:6]); ctx.close()
    b.close()
