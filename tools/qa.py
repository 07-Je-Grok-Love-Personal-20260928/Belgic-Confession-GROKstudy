"""Playwright QA：每页 × 5 个宽度。检查水平溢出、被裁切的文字、JS 错误、no-JS 与 reduced-motion 下内容可见。
用法：python3 tools/qa.py [--shots] [--nojs] [--rm] [页面...]  （file:// 打开）"""
import sys,os,glob,json
from playwright.sync_api import sync_playwright
args=sys.argv[1:]; shots='--shots' in args; nojs='--nojs' in args; rm='--rm' in args; opn='--open' in args; offt='--offline-tiles' in args; tocopen='--toc' in args
pages=[a for a in args if a.endswith('.html')] or sorted(glob.glob('*.html'))
W=[int(x) for x in os.environ['W'].split(',')] if os.environ.get('W') else [320,360,390,414,768,1024,1280,1440,1920]
JS_OVER='''()=>{
 const vw=document.documentElement.clientWidth, out=[];
 const sc=(el)=>{for(let p=el;p&&p!==document.body;p=p.parentElement){const o=getComputedStyle(p).overflowX; if((o==='auto'||o==='scroll')&&p.scrollWidth>p.clientWidth) return true;} return false};
 document.querySelectorAll('main *, #toc *').forEach(el=>{
   if(el.closest('svg')&&el.tagName!=='svg') return;
   if(el.closest('.leaflet-container')) return; // 地图瓦片由容器 overflow:hidden 裁切
   const r=el.getBoundingClientRect(); if(r.width===0||r.height===0) return;
   if(getComputedStyle(el).position==='fixed') return;
   if(r.right>vw+1||r.left<-1){ if(!sc(el)&&!el.closest('#toc')) out.push([el.tagName+'.'+(el.className&&el.className.baseVal===undefined?el.className:''),Math.round(r.left),Math.round(r.right)]); }
 });
 return {sw:document.documentElement.scrollWidth,vw:vw,over:out.slice(0,6),n:out.length};
}'''
JS_CLIP='''()=>{const out=[];document.querySelectorAll('main p,main li,main td,main th,main b,main a,main span,main h3,main h4,main small,main summary,main button').forEach(el=>{
 const cs=getComputedStyle(el); if(el.closest('svg')||el.closest('#toc')) return;
 if(el.scrollWidth>el.clientWidth+2&&(cs.overflowX==='hidden'||cs.overflowX==='clip')&&el.clientWidth>0&&getComputedStyle(el).display!=='inline') out.push(el.tagName+'.'+el.className+':'+(el.textContent||'').slice(0,20));
 });return out.slice(0,5)}'''
JS_VCLIP='''()=>{const out=[];document.querySelectorAll('main *').forEach(el=>{
 if(el.closest('svg')||el.closest('.leaflet-container')||el.closest('pre.mermaid')) return;
 const cs=getComputedStyle(el); if(!(cs.overflowY==='hidden'||cs.overflowY==='clip')) return;
 if(cs.webkitLineClamp&&cs.webkitLineClamp!=='none') return;
 if(el.clientHeight<4||el.scrollHeight<=el.clientHeight+3) return;
 if(el.closest('details:not([open])')) return;
 const r=el.getBoundingClientRect(); let bad=null;
 const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let n;
 while((n=w.nextNode())){ if(!n.textContent.trim()) continue; const p=n.parentElement; if(!p||getComputedStyle(p).visibility==='hidden') continue;
   const rg=document.createRange(); rg.selectNodeContents(n); for(const q of rg.getClientRects()){ if(q.height&&(q.bottom>r.bottom+2||q.top<r.top-2)){bad=n.textContent.trim().slice(0,16);break} } if(bad) break; }
 if(bad) out.push(el.tagName+'.'+String(el.className).slice(0,24)+':'+bad+' '+el.scrollHeight+'>'+el.clientHeight);
 });return out.slice(0,6)}'''
JS_TOC='''()=>{const nav=document.getElementById('toc');if(!nav)return ['无目录'];const out=[],N=nav.getBoundingClientRect();
 if(getComputedStyle(nav).visibility==='hidden')return ['目录未打开'];
 const bx=document.getElementById('tkbody').getBoundingClientRect();
 nav.querySelectorAll('.tk-head *, .tk-row, .tk-row > *, .tk-t, .tk-n').forEach(el=>{const r=el.getBoundingClientRect();if(!r.width||!r.height)return;
   if(r.right>N.right-1+1||r.left<N.left-1) out.push('横向越界:'+el.className+':'+(el.textContent||'').trim().slice(0,14)+' '+Math.round(r.right)+'>'+Math.round(N.right));
   const cs=getComputedStyle(el); if(el.scrollWidth>el.clientWidth+2&&(cs.overflowX==='hidden'||cs.overflowX==='clip')) out.push('裁切:'+(el.textContent||'').trim().slice(0,14));});
 const rows=[...nav.querySelectorAll('.tk-row')].filter(r=>r.offsetParent).map(r=>r.getBoundingClientRect());
 for(let i=1;i<rows.length;i++){ if(rows[i].top<rows[i-1].bottom-1.5) {out.push('行重叠@'+i);break} }
 const hs=[...nav.querySelectorAll('.tk-head > *, .tk-tools > *')].filter(e=>e.offsetParent).map(e=>e.getBoundingClientRect());
 for(let i=0;i<hs.length;i++)for(let j=i+1;j<hs.length;j++){const a=hs[i],b=hs[j];if(a.left<b.right-1&&b.left<a.right-1&&a.top<b.bottom-1&&b.top<a.bottom-1&&!(a.left<=b.left&&a.right>=b.right&&a.top<=b.top&&a.bottom>=b.bottom)&&!(b.left<=a.left&&b.right>=a.right&&b.top<=a.top&&b.bottom>=a.bottom))out.push('目录头部重叠 '+i+'/'+j)}
 if(innerWidth>=1100){const m=document.getElementById('main').getBoundingClientRect(); if(m.left<N.right-1) out.push('正文被目录压住 '+Math.round(m.left)+'<'+Math.round(N.right))}
 const all=nav.querySelectorAll('.tk-i.has').length, op=nav.querySelectorAll('.tk-i.has.open').length; if(all!==op) out.push('未全部展开 '+op+'/'+all);
 return out.slice(0,6)}'''
JS_VIS='''()=>{let n=0,bad=[];document.querySelectorAll('.reveal').forEach(e=>{const o=parseFloat(getComputedStyle(e).opacity);if(o<0.99){n++;if(bad.length<3)bad.push(e.className.slice(0,30))}});return {hidden:n,bad:bad,js:document.documentElement.classList.contains('js')}}'''
res=[];fail=0
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for f in pages:
        for w in W:
            ctx=b.new_context(viewport={'width':w,'height':900},java_script_enabled=not nojs,reduced_motion='reduce' if rm else 'no-preference')
            if os.environ.get('THEME'): ctx.add_init_script("try{localStorage.setItem('ui.theme','%s')}catch(e){}"%os.environ['THEME'])
            if offt:
                ctx.route('**/*', lambda route: route.abort() if any(x in route.request.url for x in ('tile.openstreetmap','basemaps.cartocdn','arcgisonline','opentopomap','openstreetmap.fr','openstreetmap.de','autonavi','webrd')) else route.continue_())
            pg=ctx.new_page(); errs=[]
            pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:errs.append(m.text) if m.type=='error' and not any(x in (m.text or '') for x in ('ERR_FAILED','ERR_CONNECTION','ERR_NAME_NOT_RESOLVED','ERR_BLOCKED','net::ERR')) else None)
            pg.goto('file://'+os.path.abspath(f)); pg.wait_for_timeout(300);
            if tocopen:
                pg.evaluate("m=>{TK.show();const l=TK.limits();TK.setWidth(m==='max'?l[1]:l[0]);TK.expandAll(true)}",os.environ.get('TOCW','min')); pg.wait_for_timeout(450)
            pg.evaluate("s=>{const e=document.createElement('style');e.textContent=s;document.head.appendChild(e)}",'*{content-visibility:visible!important}')  # v8：测量时强制渲染 content-visibility:auto 的区块
            if opn: pg.evaluate("document.querySelectorAll('details').forEach(e=>e.open=true)")
            if not nojs:
                # 滚动一遍以触发 reveal / 进度
                h=pg.evaluate('document.documentElement.scrollHeight')
                pg.evaluate('''async(h)=>{const f=()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));for(let y=0;y<h;y+=700){window.scrollTo(0,y);await f();}}''',h)  # 单次 evaluate 内滚动，免去每步往返
                pg.evaluate('window.scrollTo(0,0)'); pg.wait_for_timeout(200)
            ov=pg.evaluate(JS_OVER); cl=pg.evaluate(JS_CLIP); vis=pg.evaluate(JS_VIS); vc=pg.evaluate(JS_VCLIP) if os.environ.get('VCLIP','1')=='1' else []
            bad=[]
            if tocopen:
                tq=pg.evaluate(JS_TOC)
                if tq: bad.append(f"目录问题: {tq}")
            if ov['sw']>ov['vw']+1: bad.append(f"页面横向溢出 sw={ov['sw']} vw={ov['vw']}")
            if ov['n']: bad.append(f"元素越界 {ov['n']}: {ov['over']}")
            if cl: bad.append(f"文字被裁切: {cl}")
            if vc: bad.append(f"纵向裁切: {vc}")
            if errs: bad.append(f"JS错误: {errs[:2]}")
            if (nojs or rm) and vis['hidden']: bad.append(f"不可见元素 {vis}")
            if (nojs and vis['js']) : bad.append("no-JS 却带 js 类")
            if rm and vis['js']: bad.append("reduced-motion 却启用 reveal")
            if shots and w in (360,1280) and not nojs and not rm:
                os.makedirs('_shots',exist_ok=True); pg.screenshot(path=f'_shots/{f[:-5]}_{w}.png',full_page=True)
            tag='FAIL' if bad else 'ok'
            if bad: fail+=1; print(tag,f,w,bad)
            ctx.close()
    b.close()
print('QA',('toc='+os.environ.get('TOCW','min')) if tocopen else '',('nojs' if nojs else 'rm' if rm else 'normal'),'theme='+os.environ.get('THEME','night'),'open' if opn else 'collapsed','pages',len(pages),'widths',W,'fails',fail)
