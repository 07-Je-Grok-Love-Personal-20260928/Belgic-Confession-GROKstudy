"""v4 目录交互测试（多轮）：鼠标/触摸/笔拖宽 + 上下限 + 记忆、键盘调宽、双击复位、折叠记忆、隐藏记忆、搜索、滚动高亮、手机抽屉。
用法: PASSES=3 python3 tools/qa_toc4.py [pages]"""
import sys,os
from playwright.sync_api import sync_playwright
pages=sys.argv[1:] or ['index.html','bc.html','hist.html','atlas.html','compare.html']
PASSES=int(os.environ.get('PASSES','3')); fails=[]; n=0
def ok(c,msg):
    global n; n+=1
    if not c: fails.append(msg); print('FAIL',msg)
def W(pg): return pg.evaluate("Math.round(document.getElementById('toc').getBoundingClientRect().width)")
def drag(pg,cdp,dx,kind):
    bb=pg.query_selector('#tocgrip').bounding_box(); x=bb['x']+bb['width']/2; y=bb['y']+bb['height']/2
    if kind=='mouse':
        pg.mouse.move(x,y); pg.mouse.down()
        for i in range(1,13): pg.mouse.move(x+dx*i/12,y)
        pg.mouse.up()
    elif kind=='pen':
        cdp.send('Input.dispatchMouseEvent',{'type':'mousePressed','x':x,'y':y,'button':'left','clickCount':1,'pointerType':'pen'})
        for i in range(1,13): cdp.send('Input.dispatchMouseEvent',{'type':'mouseMoved','x':x+dx*i/12,'y':y,'button':'left','buttons':1,'pointerType':'pen'})
        cdp.send('Input.dispatchMouseEvent',{'type':'mouseReleased','x':x+dx,'y':y,'button':'left','clickCount':1,'pointerType':'pen'})
    else:
        cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
        for i in range(1,13): cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+dx*i/12,'y':y}]})
        cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    pg.wait_for_timeout(250)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for ps in range(PASSES):
        for f in pages:
            url='file://'+os.path.abspath(f)
            # ---------- 桌面 ----------
            ctx=b.new_context(viewport={'width':1440,'height':900}); pg=ctx.new_page(); cdp=ctx.new_cdp_session(pg); errs=[]
            pg.on('pageerror',lambda e:errs.append(str(e)))
            pg.goto(url); pg.wait_for_timeout(400); T=f'[p{ps+1} {f} 桌面]'
            lo,hi=pg.evaluate('TK.limits()'); w0=W(pg)
            ok(pg.evaluate('TK.isOpen()'),T+' 默认打开')
            m=pg.evaluate("document.getElementById('main').getBoundingClientRect().left"); ok(m>=w0-1,T+f' 正文让出目录宽 {m}<{w0}')
            kind=['mouse','pen','touch'][ps%3] if ps%3!=2 else 'mouse'
            drag(pg,cdp,150,kind); w1=W(pg); ok(abs(w1-(w0+150))<=3,T+f' {kind} 拖宽 {w0}->{w1}')
            pg.wait_for_timeout(450); m=pg.evaluate("document.getElementById('main').getBoundingClientRect().left"); ok(abs(m-w1)<=2,T+f' 松手后正文跟随 {m} vs {w1}')
            ok(pg.evaluate("localStorage.getItem('tk4.w')")==str(w1),T+' 宽度已记忆')
            drag(pg,cdp,2000,kind); ok(W(pg)==hi,T+f' 上限 {W(pg)}!={hi}')
            drag(pg,cdp,-3000,kind); ok(W(pg)==lo,T+f' 下限 {W(pg)}!={lo}')
            drag(pg,cdp,123,'mouse'); wk=W(pg); pg.wait_for_timeout(600); pg.reload(); pg.wait_for_timeout(400); ok(abs(W(pg)-wk)<=1,T+f' 刷新后宽度保持 {W(pg)} vs {wk}')
            pg.focus('#tocgrip'); a=W(pg); pg.keyboard.press('ArrowRight'); pg.keyboard.press('ArrowRight'); ok(W(pg)>a,T+' 键盘右键加宽')
            pg.keyboard.press('Home'); ok(W(pg)==lo,T+' Home=最窄'); pg.keyboard.press('End'); ok(W(pg)==hi,T+' End=最宽')
            pg.dblclick('#tocgrip'); pg.wait_for_timeout(200); ok(pg.evaluate("localStorage.getItem('tk4.w')") is None,T+' 双击复位')
            # 折叠
            li=pg.query_selector('#toc .tk-i.has:not(.open)')
            if li:
                sid=li.evaluate("l=>l.firstChild.lastChild.dataset.s"); li.query_selector('.tk-tg').click(); pg.wait_for_timeout(200)
                ok(li.evaluate("l=>l.classList.contains('open')&&getComputedStyle(l.querySelector('ol')).display!=='none'"),T+' 点开一级/二级')
                pg.wait_for_timeout(200); pg.reload(); pg.wait_for_timeout(400)
                ok(pg.evaluate("s=>document.querySelector('#toc a[data-s=\"'+s+'\"]').closest('.tk-i').classList.contains('open')",sid),T+' 展开状态刷新后保持')
                pg.evaluate("s=>document.querySelector('#toc a[data-s=\"'+s+'\"]').closest('.tk-i').querySelector('.tk-tg').click()",sid); pg.wait_for_timeout(150)
                ok(not pg.evaluate("s=>document.querySelector('#toc a[data-s=\"'+s+'\"]').closest('.tk-i').classList.contains('open')",sid),T+' 再点收起')
            pg.click('[data-tk=open]'); pg.wait_for_timeout(600)
            ok(pg.evaluate("document.querySelectorAll('#toc .tk-i.has:not(.open)').length")==0,T+' 全部展开按钮')
            ok(pg.evaluate("document.querySelectorAll('#toc .tk3').length")>0 or f=='index.html',T+' 有三级条目')
            pg.click('[data-tk=close]'); pg.wait_for_timeout(200); ok(pg.evaluate("document.querySelectorAll('#toc .tk-i.open').length")==0,T+' 全部收起按钮')
            # 搜索
            pg.fill('#tkq','圣约'); pg.wait_for_timeout(300)
            r=pg.evaluate("[document.querySelectorAll('#toc .tk-i.m').length,[...document.querySelectorAll('#toc .tk-i')].filter(l=>l.offsetParent&&!l.classList.contains('m')&&!l.classList.contains('mh')).length]")
            ok(r[0]>0 and r[1]==0,T+f' 搜索过滤 {r}')
            pg.fill('#tkq',''); pg.wait_for_timeout(250); ok(not pg.evaluate("document.getElementById('toc').classList.contains('tk-filter')||!!document.querySelector('#toc .tk-filter')"),T+' 清空搜索复原')
            # 滚动高亮
            if f!='index.html':
                sid=pg.evaluate("(()=>{const a=[...document.querySelectorAll('#toc .tk-i.is-cur a[data-s]')];const t=a[Math.floor(a.length*0.6)];return t?t.dataset.s:null})()")
                if sid:
                    pg.evaluate("s=>{document.getElementById(s).scrollIntoView({behavior:'instant'});window.scrollBy({top:40,behavior:'instant'})}",sid); pg.wait_for_timeout(700)
                    on=pg.evaluate("document.querySelector('#toc a.on')?.dataset.s"); ok(on is not None,T+f' 滚动高亮存在 (目标 {sid} 现 {on})')
                    ok(pg.evaluate("(()=>{let a=document.querySelector('#toc a.on');if(a&&!a.offsetParent){let li=a.closest('.tk-i');while(li&&!li.offsetParent)li=li.parentElement.closest('.tk-i');a=li&&li.querySelector('a');if(!a||!a.closest('.on-p'))return false}if(!a)return false;const r=a.getBoundingClientRect(),b=document.getElementById('tkbody').getBoundingClientRect();return r.top>=b.top-2&&r.bottom<=b.bottom+2})()"),T+' 高亮项自动滚入目录可视区')
            # 隐藏 + 记忆
            pg.click('#tocx'); pg.wait_for_timeout(400); ok(not pg.evaluate('TK.isOpen()'),T+' ✕ 隐藏')
            m=pg.evaluate("document.getElementById('main').getBoundingClientRect().left"); ok(m<5,T+f' 隐藏后正文占满 {m}')
            pg.reload(); pg.wait_for_timeout(400); ok(not pg.evaluate('TK.isOpen()'),T+' 隐藏状态刷新后保持')
            pg.click('#tocbtn'); pg.wait_for_timeout(400); ok(pg.evaluate('TK.isOpen()'),T+' 按钮再打开')
            ok(not errs,T+f' JS 错误 {errs[:2]}'); ctx.close()
            # ---------- 手机 ----------
            ctx=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True); pg=ctx.new_page(); cdp=ctx.new_cdp_session(pg); errs=[]
            pg.on('pageerror',lambda e:errs.append(str(e)))
            pg.goto(url); pg.wait_for_timeout(400); T=f'[p{ps+1} {f} 手机]'
            ok(not pg.evaluate('TK.isOpen()'),T+' 默认收起')
            pg.tap('#tocbtn'); pg.wait_for_timeout(450); ok(pg.evaluate("document.documentElement.classList.contains('tk-open')"),T+' 点按打开抽屉')
            vis=pg.evaluate("(()=>{const r=document.getElementById('toc').getBoundingClientRect();return r.left>=-1&&r.right<=innerWidth+1})()"); ok(vis,T+' 抽屉在屏内')
            lo,hi=pg.evaluate('TK.limits()'); w0=W(pg); drag(pg,cdp,-60,'touch'); w1=W(pg); ok(w1<w0 or w0==lo,T+f' 触摸拖窄 {w0}->{w1}')
            drag(pg,cdp,800,'touch'); ok(W(pg)==hi,T+f' 触摸上限 {W(pg)}!={hi}'); ok(pg.evaluate("localStorage.getItem('tk4.wm')")==str(hi),T+' 手机宽度单独记忆')
            # 三级在抽屉里
            pg.evaluate('TK.expandAll(true)'); pg.wait_for_timeout(200)
            ok(pg.evaluate("document.querySelectorAll('#toc .tk-i.has:not(.open)').length")==0,T+' 抽屉同样三级展开')
            pg.evaluate("TK.collapseAll()")
            # 点遮罩关闭
            pg.mouse.click(385,420); pg.wait_for_timeout(400)
            ok(not pg.evaluate("document.documentElement.classList.contains('tk-open')"),T+' 点遮罩关闭')
            pg.tap('#tocbtn'); pg.wait_for_timeout(400); pg.keyboard.press('Escape'); pg.wait_for_timeout(350); ok(not pg.evaluate('TK.isOpen()'),T+' Esc 关闭')
            pg.tap('#tocbtn'); pg.wait_for_timeout(400)
            a=pg.query_selector('#toc .tk-i.is-cur .tk-row a[data-s]') if f!='index.html' else None
            if a:
                a.tap(); pg.wait_for_timeout(500); ok(not pg.evaluate('TK.isOpen()'),T+' 点条目后自动收起')
            ok(not errs,T+f' JS 错误 {errs[:2]}'); ctx.close()
    b.close()
print('TOC4 tests',n,'fails',len(fails))
