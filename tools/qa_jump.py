"""v4 锚点落点测试：点目录条目后目标是否对准顶部、滚动高亮是否指向它。"""
import os,sys
from playwright.sync_api import sync_playwright
pages=sys.argv[1:] or ['bc.html','hct.html','dtt.html','creedsx.html','bct.html','atlas.html','hist.html','bible.html']
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    bad=0;tot=0;spy=0
    for vw in (1440,390):
     for f in pages:
      ctx=b.new_context(viewport={'width':vw,'height':900},is_mobile=vw<600,has_touch=vw<600);pg=ctx.new_page();pg.goto('file://'+os.path.abspath(f));pg.wait_for_timeout(400)
      ids=pg.evaluate("(()=>{const a=[...document.querySelectorAll('#toc .tk-i.is-cur a[data-s]')].map(x=>x.dataset.s);return [...new Set([a[Math.floor(a.length*.45)],a[a.length-2],a[3],a[Math.floor(a.length*.7)]].filter(Boolean))]})()")
      out=[]
      for i in ids:
        if vw<600: pg.evaluate("TK.show()"); pg.wait_for_timeout(350)
        pg.evaluate("TK.expandAll(true)"); pg.click(f'#toc a[data-s="{i}"]'); pg.wait_for_timeout(900)
        t,on,mx=pg.evaluate(f"(()=>{{const e=document.getElementById('{i}');return [Math.round(e.getBoundingClientRect().top),document.querySelector('#toc a.on')?.dataset.s,document.documentElement.scrollHeight-innerHeight-scrollY]}})()")
        tot+=1; good=abs(t-16)<=3 or mx<3
        if not good: bad+=1
        if on!=i: spy+=1
        out.append(f"{i}:{t}{'' if good else '✗'}:{'✓' if on==i else on}")
      print(vw,f,out,flush=True); ctx.close()
    print('JUMP bad',bad,'of',tot,'spy-mismatch',spy)
    b.close()
