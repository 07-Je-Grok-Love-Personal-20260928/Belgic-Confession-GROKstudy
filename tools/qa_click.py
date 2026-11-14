"""v3 点击交互测试：目录开关、主题按钮逐个点击、逐个点开 summary、地图底图切换与离线回退。用法：python3 tools/qa_click.py [页面...]"""
import sys,os,glob
from playwright.sync_api import sync_playwright
pages=[a for a in sys.argv[1:] if a.endswith('.html')] or sorted(glob.glob('*.html'))
BLOCK=('tile.openstreetmap','basemaps.cartocdn','arcgisonline','opentopomap','openstreetmap.fr','openstreetmap.de','autonavi')
fails=[]
def chk(c,m):
    if not c: fails.append(m); print('FAIL',m)
OV="()=>document.documentElement.scrollWidth-document.documentElement.clientWidth"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for f in pages:
        for w in (360,1280):
            mob=w<600
            ctx=b.new_context(viewport={'width':w,'height':800},is_mobile=mob,has_touch=mob)
            pg=ctx.new_page(); errs=[]
            pg.on('pageerror',lambda e:errs.append(str(e)))
            pg.goto('file://'+os.path.abspath(f)); pg.wait_for_timeout(300)
            tag=f'{f}@{w}'
            # TOC
            if pg.query_selector('#tocbtn'):
                pg.click('#tocbtn'); pg.wait_for_timeout(350)
                op=pg.evaluate("document.body.classList.contains('toc-open')||document.getElementById('toc')?.classList.contains('open')||getComputedStyle(document.getElementById('toc')).visibility!=='hidden'")
                chk(op,f'{tag} 目录未打开'); chk(pg.evaluate(OV)<=1,f'{tag} 目录打开后横向溢出')
                pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
                if pg.evaluate("document.body.classList.contains('toc-open')"): pg.click('#tocbtn',force=True); pg.wait_for_timeout(300)
            # 主题
            if pg.query_selector('#thmb'):
                for t in ('dawn','jade','ocean','grape','parch','night'):
                    pg.click('#thmb'); pg.wait_for_timeout(120)
                    pg.click(f'[data-theme-set="{t}"]'); pg.wait_for_timeout(120)
                    got=pg.evaluate("document.documentElement.getAttribute('data-theme')||'night'")
                    chk(got==t,f'{tag} 主题 {t} 未生效（{got}）')
            # summary 全部点开
            n=pg.evaluate("(()=>{let n=0;document.querySelectorAll('details>summary').forEach(s=>{const d=s.parentElement;if(!d.open&&s.offsetParent){s.click();n++}});return n})()")
            pg.wait_for_timeout(250)
            closed=pg.evaluate("[...document.querySelectorAll('details>summary')].filter(s=>s.offsetParent&&!s.parentElement.open).length")
            chk(closed==0,f'{tag} 有 {closed} 个 summary 点不开')
            chk(pg.evaluate(OV)<=1,f'{tag} 展开后横向溢出 {pg.evaluate(OV)}')
            chk(not errs,f'{tag} JS 错误 {errs[:2]}')
            print('ok' if not [x for x in fails if x.startswith(tag)] else '--',tag,'summaries',n)
            ctx.close()
    # 地图：在线加载与切换
    for f in [x for x in pages if x in ('atlas.html','hist.html')]:
        for mode in ('online','blocked'):
            ctx=b.new_context(viewport={'width':390,'height':800},is_mobile=True,has_touch=True)
            if mode=='blocked': ctx.route('**/*',lambda r: r.abort() if any(x in r.request.url for x in BLOCK) else r.continue_())
            pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            pg.goto('file://'+os.path.abspath(f)); pg.wait_for_timeout(300)
            boxes=pg.query_selector_all('.livebox')
            for i,bx in enumerate(boxes):
                bx.scroll_into_view_if_needed(); pg.wait_for_timeout(200)
            pg.wait_for_timeout(3000 if mode=='online' else 9000)
            res=pg.evaluate("[...document.querySelectorAll('.livebox')].map(b=>({ok:b.dataset.ok,tiles:b.querySelectorAll('img.leaflet-tile-loaded').length,mk:b.querySelectorAll('.leaflet-interactive').length,stat:(b.closest('.livemap')||b.parentElement).querySelector('.mapstat')?.textContent||''}))")
            svg=pg.evaluate("[...document.querySelectorAll('.mapduo svg, figure svg.sch')].filter(s=>s.getBoundingClientRect().height>100).length")
            for i,r in enumerate(res):
                chk(r['ok']=='1',f'{f} {mode} 地图{i} 未初始化 {r}')
                chk(r['mk']>0,f'{f} {mode} 地图{i} 无标记')
                if mode=='online': chk(r['tiles']>0,f'{f} online 地图{i} 无瓦片 {r["stat"]}')
                else: chk(r['tiles']==0 and r['stat']!='',f'{f} blocked 地图{i} 回退提示缺失 {r}')
            chk(svg>=len(res),f'{f} {mode} 示意图数 {svg} < 地图数 {len(res)}')
            if mode=='online' and boxes:
                sel=pg.query_selector('.tilesel')
                for tid in ('carto','esri','otm','gaode','osm'):
                    sel.select_option(tid); pg.wait_for_timeout(2500)
                    t=pg.evaluate(f"document.querySelectorAll('.livebox img.tl-{tid}.leaflet-tile-loaded, .livebox .tl-{tid} img.leaflet-tile-loaded').length")
                    print('  tile',tid,'loaded imgs',t); chk(t>0,f'{f} 切换到 {tid} 无瓦片')
            chk(not errs,f'{f} {mode} JS 错误 {errs[:2]}')
            print(f,mode,[ (r['tiles'],r['stat'][:24]) for r in res])
            ctx.close()
    b.close()
print('CLICK QA pages',len(pages),'fails',len(fails))
