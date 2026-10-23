# -*- coding: utf-8 -*-
"""生成全站静态页面。用法：python3 build.py"""
import json,re,html as H
from core import *
import core
from c_common import *
import pdf15,storymap
import c_compare,c_west,c_src,libs
import p_bible,p_hist,p_bc,p_topics,p_mem

SITE="比利时信条 · 欧陆改革宗深读"
PAGES=[("index","index.html","首页","home"),("bible","bible.html","一 全本圣经与圣约","book"),("hist","hist.html","二 历史·地理·文化","map"),("bc","bc.html","三 37条逐条深读","scroll"),
 ("topics","topics.html","四 专题深析","brain"),("compare","compare.html","五 三项联合信条比较","link"),("westminster","westminster.html","六 威斯敏斯特对照","scale"),
 ("bct","bct.html","七 BC 原文·背诵","scroll"),("hct","hct.html","八 HC 原文·背诵","scroll"),("dtt","dtt.html","九 Dort 原文·背诵","scroll"),("creedsx","creedsx.html","十 三大信经","scroll"),
 ("memory","memory.html","十一 记忆自测","brain"),("sources","sources.html","十二 来源","library")]
if "home" not in P: P["home"]=P["book"]
PARTS={"bible":p_bible.part_bible,"hist":p_hist.part_hist,"bc":p_bc.part_bc,"topics":p_topics.part_topics,"compare":c_compare.part_compare,"westminster":c_west.part_westminster,
 "hct":libs.part_hct,"bct":libs.part_bct,"dtt":libs.part_dtt,"creedsx":libs.part_creedsx,"memory":p_mem.part_memory}
FILE={k:f for k,f,_,_ in PAGES}; LABEL={k:t for k,_,t,_ in PAGES}
BODY={}
L1N={"bible":1,"hist":2,"bc":3,"topics":4,"compare":5,"westminster":6,"bct":7,"hct":8,"dtt":9,"creedsx":10,"memory":11,"sources":12}
for k,_,_,_ in PAGES[1:]:
    core.CUR["f"]=FILE[k]; core.CUR["n"]=L1N[k]; core.CUR["c2"]=0
    if k=="sources": BODY[k]=c_src.part_src(BODY)
    else: BODY[k]=PARTS[k]()
TOC=core.TOC
IDS={}
for k,h in BODY.items():
    for i in re.findall(r'\bid="([^"]+)"',h): IDS.setdefault(i,FILE[k])
UNRES=[]
def rewrite(k,h):
    own=set(re.findall(r'\bid="([^"]+)"',h))
    def f(m):
        i=m.group(1)
        if i in own or i=="": return m.group(0)
        if i in IDS: return f'href="{IDS[i]}#{i}"'
        UNRES.append((k,i)); return m.group(0)
    return re.sub(r'href="#([^"]*)"',f,h)
def toc_html(cur):
    t='<nav id="toc" aria-label="目录"><div class="tochead"><b>目录</b><button id="tocx" class="btn ghost" aria-label="隐藏目录" type="button">✕</button></div>'
    t+='<a class="tochome'+(' on' if cur=="index" else '')+'" href="index.html">🏠 首页 · 学习路径与进度</a><ol>'
    for id,title,subs,f in TOC:
        page=[k for k,ff in FILE.items() if ff==f][0]
        def sub(s):
            sid,st,kids=s
            if not kids: return f'<li class="t2"><a href="{f}#{sid}">{st}</a></li>'
            return (f'<li class="t2 has closed"><div class="t2r"><a href="{f}#{sid}">{st}</a><button class="tg2" type="button" aria-label="展开或收起三级标题" aria-expanded="false">▾</button></div><ol>'
                    +"".join(f'<li class="t3"><a href="{f}#{i}">{tt}</a></li>' for i,tt in kids)+"</ol></li>")
        t+=f'<li class="t1{" cur" if page==cur else " closed"}" data-page="{page}"><div class="t1r"><a href="{f}#{id}">{title}</a><button class="tg" type="button" aria-label="展开或收起" aria-expanded="{"true" if page==cur else "false"}">▾</button></div><ol>'+"".join(sub(s) for s in subs)+"</ol></li>"
    return t+"</ol></nav>"
def tabs(cur):
    return '<nav class="ptabs" aria-label="页面导航">'+"".join(f'<a href="{f}"{" class=on aria-current=page" if k==cur else ""}>{t}</a>' for k,f,t,_ in PAGES)+'</nav>'
def pager(cur):
    ks=[k for k,_,_,_ in PAGES]; i=ks.index(cur); out='<nav class="pager" aria-label="上一页下一页">'
    if i>0: out+=f'<a class="pg prev" href="{FILE[ks[i-1]]}"><small>← 上一页</small><b>{LABEL[ks[i-1]]}</b></a>'
    else: out+='<span></span>'
    if i<len(ks)-1: out+=f'<a class="pg next" href="{FILE[ks[i+1]]}"><small>下一页 →</small><b>{LABEL[ks[i+1]]}</b></a>'
    return out+'</nav>'
DESC={"index":"比利时信条（1561，德布利）欧陆改革宗中文深读：全本圣经与圣约、历史地理文化、37 条逐条深读、三项联合信条比较、CCI 原文逐字、背诵与自测。"}
MERMAID='''<script type="module">import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
mermaid.initialize({startOnLoad:false,securityLevel:"strict",theme:"base",flowchart:{htmlLabels:true,curve:"basis",useMaxWidth:true},themeVariables:{fontFamily:"PingFang SC, Noto Sans SC, Microsoft YaHei, sans-serif",fontSize:"14px",primaryColor:"#24345f",primaryTextColor:"#ffffff",primaryBorderColor:"#d4af37",lineColor:"#d4af37",secondaryColor:"#2c2550",tertiaryColor:"#16203f",clusterBkg:"#16203f",clusterBorder:"#5aa9e6",titleColor:"#f3d98b",edgeLabelBackground:"#0d1838",textColor:"#e8ecf6",nodeTextColor:"#ffffff"}});
const els=[...document.querySelectorAll("pre.mermaid")];const run=async(el)=>{if(el.dataset.processed)return;try{await mermaid.run({nodes:[el]})}catch(e){el.insertAdjacentHTML("afterend","<p class=mermaid-err>流程图未能渲染，上方为文字版。</p>")}};
if("IntersectionObserver" in window){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){io.unobserve(e.target);run(e.target)}}),{rootMargin:"400px"});els.forEach(e=>io.observe(e))}else els.forEach(run);</script>'''
def extra_js(cur,body):
    o=""
    if 'id="lmap"' in body: o+='<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin="" defer></script>'
    if 'class="mermaid"' in body: o+=MERMAID
    return o
def extra_css(cur,body):
    return '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="">' if 'id="lmap"' in body else ''
def page(cur,body):
    n={k:len(re.findall(r'<section class="l2',h)) for k,h in BODY.items()}
    title=LABEL[cur]+" · "+SITE if cur!="index" else "比利时信条 · 欧陆改革宗深读（Belgic Confession GROKstudy）"
    desc=DESC.get(cur) or re.sub(r'<[^>]+>','',re.search(r'<p class="lead">(.*?)</p>',body).group(1))+" "+SITE+"。"
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} {V}</title><meta name="description" content="{H.escape(desc[:150])}"><meta name="theme-color" content="#070d22"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><script>try{{var de=document.documentElement;de.classList.add("jsok");if(localStorage.getItem("mk.off")==="1")de.classList.add("mkoff");var s=de.style,a=+localStorage.getItem("tfu1.tw"),m=+localStorage.getItem("tfu1.twm"),w=innerWidth;if(a>=220&&a<=Math.min(680,w*.6))s.setProperty("--tw",a+"px");if(m>=240&&m<=Math.min(560,w*.94))s.setProperty("--twm",m+"px")}}catch(e){{}}</script><link rel="stylesheet" href="assets/styles.css?v={V}"><link rel="stylesheet" href="assets/bc.css?v={V}">{extra_css(cur,body)}</head><body data-page="{cur}" data-total="{n.get(cur,0)}">
<div id="prog"></div>{toc_html(cur)}<div id="tocgrip" role="separator" aria-orientation="vertical" aria-label="拖动调整目录宽度（左右方向键微调，双击还原）" title="拖动调整目录宽度；双击还原" tabindex="0"></div><button id="tocbtn" class="fab" aria-label="显示目录" aria-controls="toc" type="button">☰ 目录</button>
<main id="main">{tabs(cur)}{'' if cur=='index' else f'<p class="readchip">本页已读 <b id="pgread">0</b> / {n.get(cur,0)} 个小节</p>'}{'<div class="secbar"><b>🎯 阅读建议</b><span>先读彩色标记；“辅助”区块默认折叠。</span><button class="btn ghost" type="button" data-secall="open">展开全部辅助</button><button class="btn ghost" type="button" data-secall="close">收起全部辅助</button></div>' if 'class="secd"' in body else ''}{body}{pager(cur)}<footer class="foot"><p>{SITE} · <b>{V}</b></p><p>以圣经为最高权威；信条与信经为从属标准。三项联合信条与三大信经原文取自 <a href="https://ccifellowship.org/books/book-of-praise" target="_blank" rel="noopener">CCI《赞美手册》中文版</a>。姊妹站：<a href="{CREEDS_SITE}" target="_blank" rel="noopener">三大公教会信经 · 欧陆改革宗深读</a>。</p></footer></main>
<script>window.TEC={json.dumps({"v":V,"pages":[{"k":k,"f":f,"t":t,"n":n.get(k,0)} for k,f,t,_ in PAGES[1:]]},ensure_ascii=False)}</script>
<script src="assets/app.js?v={V}" defer></script><script src="assets/bc.js?v={V}" defer></script>{extra_js(cur,body)}</body></html>'''
def index_body():
    hc=J("hc"); nq=sum(1 for l in hc["lds"] for b in l["blocks"] if b["t"]=="h4")
    bcn=len(J("bc")["articles"]); dn=sum(len(h["items"]) for h in J("dort")["heads"])
    desc={"bible":"四幕救恩史 · 九个约 · 八条圣经神学主线 · 五个唯独 · 流程图","hist":"德布利的故事 · 时间线 · 交互地图 · 文化区域 · 版画图像 · 狱中书信",
      "bc":"37 条 × 六个面向：为何写 · 说什么 · 圣经神学 · 圣约 · 对手 · 联系；重点/难点/应用/记忆钩","topics":"三条战线 · 与法国信条比较 · 八个难点 · 安慰线 · 误解 · 数据图",
      "compare":"为什么是三份而不是一份：体裁、问题、对照矩阵、签署书","westminster":"WCF/WLC/WSC 十五个主题的对读","bct":"37 条逐字全文（CCI）· 背诵模式 · 朗读","hct":"129 问逐字全文（CCI）· 背诵模式","dtt":"63 个条目逐字全文（CCI）· 背诵模式",
      "creedsx":"使徒 · 尼西亚 · 亚他那修（CCI）背诵版","memory":"七群口诀 · 37 个钩子 · 填空 · 翻卡 · 25 题自测 · 37 天计划","sources":"CCI 逐字 · PDF 手册 · 参考站 · 图片版权"}
    icon={k:i for k,_,_,i in PAGES}
    steps="".join(f'<a class="step" href="{FILE[k]}" data-pg="{k}" style="--i:{n}"><span class="sno">{n+1}</span><span class="si">{ic(icon[k],"ic big")}</span><b>{LABEL[k]}</b><small>{desc[k]}</small><span class="bar"><i></i></span><em class="pc" data-pc="{k}">未读</em></a>' for n,(k,_,_,_) in enumerate(PAGES[1:]))
    hero=f'''<header class="hero bchero"><div class="hin"><div class="badge">欧陆改革宗 · 三项联合信条之一 · 1561</div><h1>比利时信条<br><span>Confessio Belgica · 一份从十字架下写出的告白</span></h1><p>德布利（Guido de Brès）在西班牙哈布斯堡的逼迫下写下 37 条“我们相信”。本站先看<b>整本圣经与圣约</b>，再走进<b>历史与地理</b>，然后<b>逐条深读</b>：为什么写、写了什么、怎样应用。所有信条引文<b>逐字取自 CCI《赞美手册》中文版</b>，并由程序核对。</p>
<div class="trio"><a href="bible.html" class="tri" style="--c:#5aa9e6"><i>{ic("book","ic big")}</i><b>整体</b><small>全本圣经与圣约</small></a><a href="hist.html" class="tri" style="--c:#e07a5f"><i>{ic("map","ic big")}</i><b>处境</b><small>1561 · 图尔奈 · 殉道</small></a><a href="bc.html" class="tri" style="--c:#d4af37"><i>{ic("scroll","ic big")}</i><b>局部</b><small>37 条逐条深读</small></a></div>
<div class="stats"><div><b data-count="{bcn}">{bcn}</b><small>条信条</small></div><div><b data-count="7">7</b><small>个分群</small></div><div><b data-count="9">9</b><small>个圣约节点</small></div><div><b data-count="222">222</b><small>张六面卡</small></div></div>
<div class="hbtn"><a class="btn" href="bible.html">开始：全本圣经视角</a><a class="btn ghost" href="hist.html">德布利的故事</a><a class="btn ghost" href="bc.html#bx-map">37 条地图</a><a class="btn ghost" href="bct.html">原文背诵</a></div></div></header>'''
    prog='''<section class="l1" id="path"><header class="l1h reveal"><span class="ico">'''+ic("map","ic big")+'''</span><div><div class="kick">学习路径</div><h2>十二站学习路径与进度</h2><p class="lead">建议顺序：整体（圣经与圣约）→ 处境（历史地理）→ 局部（逐条）→ 专题 → 比较 → 原文背诵 → 自测。进度只保存在你的浏览器里（localStorage），不上传。</p></div></header>
<div class="progbox reveal"><div class="ring2" id="ringbox"><svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="52" class="rb"/><circle cx="60" cy="60" r="52" class="rf" id="ringf" pathLength="100" stroke-dasharray="0 100"/></svg><div class="rt"><b id="ringn">0%</b><small>已读小节</small></div></div><div class="pinfo"><p>已读 <b id="readn">0</b> / <b id="readt">0</b> 个小节（滚动到小节即记为已读）。自测最近得分：<b id="quizs">未做</b>。</p><p><button class="btn ghost" id="resetp" type="button">清除进度</button></p></div></div>
<div class="steps">'''+steps+'''</div></section>'''
    vis=[("🌍","交互地图（Leaflet）","德布利一生足迹与 16 个地点，可缩放；另有 SVG 示意图。","hist.html#hs-map"),("🧭","时间线与故事线","1517–今天；动画时间轴与故事步骤。","hist.html#hs-tl"),("🏰","城墙动画","1561 年图尔奈城堡：信条越过城墙。","hist.html#hs-wall"),
         ("🔀","流程图（Mermaid）","圣约之线、37 条的内在逻辑、七群流程。","bible.html#bb-cov"),("🧩","37 条地图","七群着色方块，点击跳到逐条深读。","bc.html#bx-map"),("🎴","六面卡","每条：为何写·说什么·圣经神学·圣约·对手·联系。","bc.html#bx-1"),
         ("🔊","朗读（TTS）","逐条原文可用浏览器中文语音朗读。","bc.html#bx-1"),("⚔️","三条战线","罗马 · 重洗派 · 路德宗：BC 在跟谁说话。","topics.html#tp-fronts"),("📋","三项联合信条对照","为什么是三份而不是一份。","compare.html"),
         ("✍️","填空 · 翻卡 · 自测","15 句 CCI 金句填空，25 题自测。","memory.html#mem-cloze"),("🔤","背诵版","BC/HC/Dort/三信经原文背诵模式。","bct.html"),("↔️","可拖宽的目录","拖目录右缘金色手柄调宽；可收起。","index.html#idx-vis")]
    v="".join(f'<a class="card vcard" href="{u}" style="--c:#d4af37"><div class="ct"><span>{i}</span>{t}</div><p>{p}</p></a>' for i,t,p,u in vis)
    guide='''<section class="l2 reveal" id="idx-vis"><h3><span class="n">·</span>'''+ic("cross")+'''本站的视觉与互动工具</h3><div class="grid g3">'''+v+'''</div>
'''+key("<b>读法：</b>先整体后局部。颜色约定：<span class=hl-f>蓝＝父</span>、<span class=hl-s>金＝子</span>、<span class=hl-g>绿＝圣灵</span>；🔑 重点、⚠️ 难点、🌱 应用、🪝 记忆钩。没有 JavaScript 时所有内容仍然可见。")+note("信条与信经原文来自 CCI；讲解、图表与比较是本站的学习材料。来源与版权见"+'<a href="sources.html">第十二部分</a>。')+'</section>'
    return hero+prog+guide
BODY["index"]=index_body()
core.CUR["f"]="index.html"
import own,t87
import notes,trim
DEEP={"bible","hist","bc","topics","compare","westminster","memory"}; RECITE={"creedsx"}
MKS={};CUT={}
for k,f,_,_ in PAGES:
    h=own.mark(rewrite(k,BODY[k]))
    h,c=trim.cut(k,h); CUT[k]=c
    out=page(k,h)
    out,st=notes.apply(out,deep=k in DEEP,recite=k in RECITE); MKS[k]=st
    out=t87.post(out,fold=k in {"hct","bct","dtt","creedsx"})
    out,_ny=t87.extras(out,k,"tfu")
    out=re.sub(r'(<pre class="mermaid">)(.*?)(</pre>)',lambda m:m.group(1)+re.sub(r'<(?!br/?>)[^>]+>','',m.group(2))+m.group(3),out,flags=re.S)
    open(f,"w",encoding="utf-8").write(out)
trim.check()
print("marks",{k:v for k,v in MKS.items() if v}); print("trim chars",CUT,sum(CUT.values()))
own.check()
if UNRES: print("WARN unresolved links:",sorted(set(UNRES))[:40],len(UNRES))
print("built",[(f,round(len(open(f,encoding="utf-8").read())/1024)) for _,f,_,_ in PAGES])
