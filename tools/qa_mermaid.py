"""流程图离线渲染测试：屏蔽一切非本地请求，确认 pre.mermaid 渲染成 SVG。用法：python3 tools/qa_mermaid.py [BASE_URL]"""
import sys,os,glob
from playwright.sync_api import sync_playwright
base=sys.argv[1] if len(sys.argv)>1 else None
pages=[f for f in sorted(glob.glob('*.html')) if 'class="mermaid"' in open(f,encoding='utf-8').read()]
fails=0
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for f in pages:
        for w in (390,1280):
            ctx=b.new_context(viewport={'width':w,'height':850}); ext=[]
            host=(base or '').split('/')[2] if base else None
            def rt(r):
                u=r.request.url
                if u.startswith('file:') or u.startswith('data:') or (host and host in u): return r.continue_()
                ext.append(u); r.abort()
            ctx.route('**/*',rt)
            pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            pg.goto((base.rstrip('/')+'/'+f) if base else 'file://'+os.path.abspath(f)); pg.wait_for_timeout(300)
            for el in pg.query_selector_all('pre.mermaid'): el.scroll_into_view_if_needed(); pg.wait_for_timeout(300)
            pg.wait_for_timeout(2500)
            r=pg.evaluate("[...document.querySelectorAll('pre.mermaid')].map(e=>({p:e.dataset.processed||'',svg:!!e.querySelector('svg'),h:Math.round(e.getBoundingClientRect().height),nodes:e.querySelectorAll('.node').length}))")
            err=pg.evaluate("document.querySelectorAll('.mermaid-err').length")
            ov=pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")
            ok=all(x['svg'] and x['nodes']>0 and x['h']>50 for x in r) and not err and not errs and ov<=1
            if not ok: fails+=1
            print('ok' if ok else 'FAIL',f,w,r,'err',err,errs[:1],'overflow',ov,'blocked external',len(ext))
            ctx.close()
    b.close()
print('MERMAID offline pages',len(pages),'fails',fails)
