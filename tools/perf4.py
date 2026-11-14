"""v4 交互性能（手机 390 宽 + CPU 降速 / 桌面 1280）：滚动、目录拖宽、目录展开收起、主题切换、地图平移、details 展开。
用法: OUT=x.json python3 tools/perf4.py DIR [pages]"""
import sys,os,json
from playwright.sync_api import sync_playwright
target=sys.argv[1]; pages=sys.argv[2:] or ['index.html','bc.html','hist.html','atlas.html','hct.html']
base='file://'+os.path.abspath(target).rstrip('/')+'/'
W=int(os.environ.get('W','390')); CPU=float(os.environ.get('CPU','4'))
def stats(fr):
    if len(fr)<5: return dict(fps=0,jank=0,max=0,n=len(fr))
    s=sorted(fr); return dict(fps=round(len(fr)/(sum(fr) or 1)*1000,1),jank=sum(1 for x in fr if x>33),max=round(s[-1]),n=len(fr))
START="()=>{window.__fr=[];window.__run=1;let l=performance.now();function f(t){window.__fr.push(t-l);l=t;if(window.__run)requestAnimationFrame(f)}requestAnimationFrame(f)}"
STOP="()=>{window.__run=0;return window.__fr.slice(2)}"
OPEN="()=>{if(window.TK){TK.show()}else{const b=document.body;if(innerWidth>=1100)b.classList.remove('tochide');else b.classList.add('tocopen')}}"
EXP="(on)=>{if(window.TK){on?TK.expandAll():TK.collapseAll()}else{document.querySelectorAll('#toc .t1, #toc .t2.has').forEach(li=>li.classList.toggle('closed',!on))}}"
out={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for f in pages:
        mob=W<600
        ctx=b.new_context(viewport={'width':W,'height':844 if mob else 900},is_mobile=mob,has_touch=mob)
        pg=ctx.new_page(); cdp=ctx.new_cdp_session(pg)
        if CPU>1: cdp.send('Emulation.setCPUThrottlingRate',{'rate':CPU})
        pg.goto(base+f,wait_until='load'); pg.wait_for_timeout(800); rec={}
        # 滚动
        pg.evaluate(START)
        cdp.send('Input.synthesizeScrollGesture',{'x':W//2,'y':500,'yDistance':-2600,'speed':2400,'gestureSourceType':'touch' if mob else 'mouse','repeatCount':1})
        rec['scroll']=stats(pg.evaluate(STOP)); pg.evaluate('window.scrollTo(0,0)'); pg.wait_for_timeout(300)
        # 目录打开 + 展开/收起
        pg.evaluate(OPEN); pg.wait_for_timeout(500)
        pg.evaluate(START)
        for on in (1,0,1,0): pg.evaluate(EXP,on); pg.wait_for_timeout(150)
        rec['toc_fold']=stats(pg.evaluate(STOP))
        # 目录拖宽（指针拖动手柄）
        g=pg.query_selector('#tocgrip')
        if g and g.is_visible():
            bb=g.bounding_box(); x0=bb['x']+bb['width']/2; y0=bb['y']+bb['height']/2
            pg.evaluate(START); pg.mouse.move(x0,y0); pg.mouse.down()
            for i in range(1,31): pg.mouse.move(x0+i*(6 if not mob else 2),y0); pg.wait_for_timeout(16)
            for i in range(30,-1,-1): pg.mouse.move(x0+i*(6 if not mob else 2),y0); pg.wait_for_timeout(16)
            pg.mouse.up(); pg.wait_for_timeout(200); rec['toc_drag']=stats(pg.evaluate(STOP))
        # 主题
        pg.evaluate(START)
        for t in ('dawn','jade','ocean','grape','parch','night'):
            pg.evaluate("t=>{const b=document.querySelector('[data-theme-set=\"'+t+'\"]');if(b)b.click()}",t); pg.wait_for_timeout(120)
        rec['theme']=stats(pg.evaluate(STOP))
        # 关目录（手机），展开 details
        if mob: pg.evaluate("()=>{if(window.TK)TK.hide();else document.body.classList.remove('tocopen')}"); pg.wait_for_timeout(400)
        pg.evaluate(START)
        pg.evaluate("document.querySelectorAll('details').forEach((e,i)=>{if(i<20)e.open=true})"); pg.wait_for_timeout(250)
        pg.evaluate("document.querySelectorAll('details').forEach(e=>e.open=false)"); pg.wait_for_timeout(250)
        rec['details']=stats(pg.evaluate(STOP))
        # 地图平移
        box=pg.query_selector('.livebox')
        if box:
            box.scroll_into_view_if_needed(); pg.wait_for_timeout(3000); bb=box.bounding_box()
            if bb:
                cx=bb['x']+bb['width']/2; cy=bb['y']+bb['height']/2
                pg.evaluate(START); pg.mouse.move(cx,cy); pg.mouse.down()
                for i in range(1,26): pg.mouse.move(cx-i*6,cy+i*3); pg.wait_for_timeout(16)
                pg.mouse.up(); pg.wait_for_timeout(300); rec['map_pan']=stats(pg.evaluate(STOP))
        print(f,json.dumps(rec,ensure_ascii=False),flush=True); out[f]=rec; ctx.close()
    b.close()
if os.environ.get('OUT'): json.dump(out,open(os.environ['OUT'],'w'),indent=1,ensure_ascii=False)
