"""v3 交互性能：展开/目录/主题/地图平移。用法: python3 tools/perf3.py URL_OR_DIR [pages]"""
import sys,os,json,statistics as st
from playwright.sync_api import sync_playwright
target=sys.argv[1]; pages=sys.argv[2:] or ['index.html','bc.html','hist.html','atlas.html']
base = target if target.startswith('http') else 'file://'+os.path.abspath(target).rstrip('/')+'/'
W=int(os.environ.get('W','390')); CPU=float(os.environ.get('CPU','4'))

def stats(fr):
    if len(fr)<5: return dict(fps=0,jank=0,p95=0,n=len(fr))
    tot=sum(fr) or 1
    s=sorted(fr)
    return dict(fps=round(len(fr)/tot*1000,1), jank=sum(1 for x in fr if x>33), p95=round(s[int(len(s)*0.95)],1), max=round(s[-1]), n=len(fr))

JS_START="()=>{window.__fr=[];window.__run=1;let last=performance.now();function f(t){window.__fr.push(t-last);last=t;if(window.__run)requestAnimationFrame(f)}requestAnimationFrame(f)}"
JS_STOP="()=>{window.__run=0;const fr=window.__fr.slice(2);return fr}"

out={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for f in pages:
        mob=W<600
        ctx=b.new_context(viewport={'width':W,'height':844 if mob else 900},is_mobile=mob,has_touch=mob)
        pg=ctx.new_page(); cdp=ctx.new_cdp_session(pg)
        if CPU>1: cdp.send('Emulation.setCPUThrottlingRate',{'rate':CPU})
        pg.goto(base+f,wait_until='load'); pg.wait_for_timeout(600)
        rec={}
        # theme switch
        pg.evaluate(JS_START)
        for t in ('dawn','jade','ocean','grape','parch','night'):
            pg.evaluate("t=>{const b=document.querySelector('[data-theme-set=\"'+t+'\"]');if(b)b.click();else {const de=document.documentElement;if(t==='night')de.removeAttribute('data-theme');else de.setAttribute('data-theme',t)}}",t)
            pg.wait_for_timeout(80)
        rec['theme']=stats(pg.evaluate(JS_STOP))
        # toc
        pg.evaluate(JS_START)
        for i in range(6):
            pg.evaluate("document.getElementById('tocbtn')?.click(); document.getElementById('tocx')?.click()")
            pg.wait_for_timeout(120)
        rec['toc']=stats(pg.evaluate(JS_STOP))
        # details
        pg.evaluate(JS_START)
        pg.evaluate("document.querySelectorAll('details').forEach((e,i)=>{if(i<20)e.open=true})")
        pg.wait_for_timeout(200)
        pg.evaluate("document.querySelectorAll('details').forEach(e=>e.open=false)")
        pg.wait_for_timeout(200)
        rec['details']=stats(pg.evaluate(JS_STOP))
        # map pan if any
        box=pg.query_selector('.livebox')
        if box:
            box.scroll_into_view_if_needed(); pg.wait_for_timeout(2500)
            pg.evaluate(JS_START)
            try:
                cdp.send('Input.synthesizeScrollGesture',{'x':W//2,'y':420,'xDistance':-180,'yDistance':120,'speed':800,'gestureSourceType':'mouse'})
            except Exception as e:
                rec['map_err']=str(e)[:80]
            rec['map']=stats(pg.evaluate(JS_STOP))
        print(f, json.dumps(rec,ensure_ascii=False)); out[f]=rec
        ctx.close()
    b.close()
if os.environ.get('OUT'): json.dump(out,open(os.environ['OUT'],'w'),indent=1,ensure_ascii=False)
