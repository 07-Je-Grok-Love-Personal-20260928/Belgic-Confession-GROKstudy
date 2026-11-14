# -*- coding: utf-8 -*-
"""v3 地图集：每张图 = 离线示意 SVG（零网络）+ 多底图实时 Leaflet。"""
import json, html as H
from core import *
from whole import pagecore, stk
GOLD,BLUE,GREEN,RED,VIO,ORG,CY="#d4af37","#5aa9e6","#81b29a","#e07a5f","#a78bfa","#e0a85f","#6bb8d6"

# name, lat, lon, text, color, kind
def P(n,la,lo,t,c,k="city"): return dict(n=n,la=la,lo=lo,t=t,c=c,k=k)

BRES=[
 P("蒙斯 Mons",50.454,3.952,"约1522 德布利出生于此（一般史料）；后在此地作玻璃彩绘学徒（约）。",VIO,"birth"),
 P("伦敦 London",51.515,-0.083,"约1548–1552 避难于伦敦外侨教会（奥斯丁会堂 Austin Friars）（约）。",BLUE,"exile"),
 P("里尔 Lille",50.633,3.06,"约1552–1556 秘密牧养“玫瑰教会”（约）；1555 年出版《基督教信仰的杖》。",GOLD,"work"),
 P("洛桑 Lausanne",46.52,6.63,"约1556–1559 在洛桑、日内瓦受教（伯撒、加尔文）（约）。",CY,"study"),
 P("日内瓦 Geneva",46.204,6.143,"《法国信条》（1559）的来源地；BC 借鉴之，但是独立信条（CCI）。",CY,"study"),
 P("图尔奈 Tournai",50.607,3.389,"1559–1561 牧养秘密的“棕榈教会”；1561 年11月1–2日夜，信条抄本被抛过城堡围墙（一般史料）。",RED,"core"),
 P("色当 Sedan",49.70,4.94,"1561 年后避难色当，任布永公爵的牧师（约）。",VIO,"exile"),
 P("安特卫普 Antwerp",51.219,4.402,"1566 年安特卫普会议修订 BC（一般认为尤尼乌斯协助）；同年圣像破坏波及此城。",GOLD,"synod"),
 P("瓦朗谢讷 Valenciennes",50.357,3.523,"1566–67 在此牧养；1567年3月城陷，5月31日德布利在此被绞死（一般史料；CCI：1567年为主殉道）。",RED,"core"),
]
REFU=[
 P("伦敦 · 奥斯丁会堂",51.5155,-0.0994,"爱德华六世治下的外侨教会（Austin Friars），瓦隆与荷兰信徒的避难所、培训所（一般史料）。",BLUE,"hub"),
 P("埃姆登 Emden",53.367,7.206,"“荷兰改革宗的母亲教会”之一；1571 年流亡总会在此召开（CCI 译作“伊顿”），采纳 BC 作为合一告白（一般史料）。",RED,"core"),
 P("法兰克福 Frankfurt",50.110,8.682,"美因河畔的外侨教会与印刷网络；被逐信徒沿莱茵河谷移动（一般史料）。",VIO,"hub"),
 P("韦瑟尔 Wesel",51.66,6.62,"1568 年荷兰改革宗领袖在此会晤（CCI 教会规章导言）。",GOLD,"hub"),
 P("日内瓦 Geneva",46.204,6.143,"神学训练与法文诗篇的源头；许多流亡牧者曾在此受教。",CY,"study"),
 P("图尔奈 Tournai",50.607,3.389,"出发地之一：十字架下的教会把人推向流亡网络。",RED,"city"),
]
MART=[
 P("布鲁塞尔 Brussels",50.846,4.352,"1523 年两位奥古斯丁会修士在此被焚，是宗教改革后第一批新教殉道者（一般史料）。",RED,"hub"),
 P("图尔奈 Tournai",50.607,3.389,"1561 公开唱诗后遭镇压；信条在此抛过城墙（一般史料）。",RED,"core"),
 P("瓦朗谢讷 Valenciennes",50.357,3.523,"1567 年城陷，德布利于 5 月 31 日殉道（CCI：为主殉道）。",RED,"core"),
 P("安特卫普 Antwerp",51.219,4.402,"印刷与禁书中心；1566 圣像破坏后镇压加剧。",ORG,"city"),
 P("里尔 Lille",50.633,3.06,"地下“玫瑰教会”所在；低地南部逼迫最重的地带之一。",ORG,"city"),
 P("蒙斯 Mons",50.454,3.952,"埃诺省，血腥告示之下的故乡。",VIO,"city"),
]
REFM=[
 P("维滕贝格 Wittenberg",51.866,12.643,"1517 路德九十五条：改革的公开起点（一般史料）。",ORG,"hub"),
 P("苏黎世 Zurich",47.376,8.541,"茨温利在此改革，圣礼争论由此展开。",CY,"city"),
 P("日内瓦 Geneva",46.204,6.143,"加尔文，《法国信条》的背景地。",CY,"hub"),
 P("巴黎 Paris",48.857,2.352,"1559 年法国改革宗第一次全国总会通过《法国信条》（CCI：比 BC 早两年）。",VIO,"hub"),
 P("图尔奈 Tournai",50.607,3.389,"1561《比利时信条》：低地国家自己的告白。",RED,"core"),
 P("海德堡 Heidelberg",49.41,8.69,"1563《海德堡要理问答》：三项联合信条之二。",GREEN,"hub"),
 P("爱丁堡 Edinburgh",55.953,-3.189,"苏格兰改革，与欧陆改革宗互相影响。",BLUE,"city"),
 P("伦敦 London",51.507,-0.128,"爱德华六世时期的外侨教会，把欧陆改革带到英伦。",BLUE,"city"),
 P("埃姆登 Emden",53.367,7.206,"1571 流亡总会，BC 被采纳为合一告白。",GOLD,"city"),
 P("多德雷赫特 Dordrecht",51.813,4.69,"1618–19 多特大会：三项联合信条定稿（CCI）。",GREEN,"core"),
]
PROV=[
 P("图尔奈 Tournai",50.607,3.389,"图尔奈区：十七省之一，BC 抛墙之地。",RED,"core"),
 P("布鲁塞尔 Brussels",50.846,4.352,"布拉班特：哈布斯堡在低地的行政中心。",ORG,"hub"),
 P("安特卫普 Antwerp",51.219,4.402,"布拉班特北部大港，印刷与贸易中心。",GOLD,"city"),
 P("根特 Ghent",51.054,3.717,"佛兰德：毛纺与城市自治传统。",GOLD,"city"),
 P("蒙斯 Mons",50.454,3.952,"埃诺：德布利的故乡。",VIO,"city"),
 P("里尔 Lille",50.633,3.06,"与阿图瓦相邻的法语／弗拉芒交界地带。",ORG,"city"),
 P("米德尔堡 Middelburg",51.5,3.61,"泽兰：1581 年总会要求签署 BC（一般史料）。",GREEN,"city"),
 P("阿姆斯特丹 Amsterdam",52.372,4.900,"荷兰省后来的重心。",BLUE,"city"),
 P("乌得勒支 Utrecht",52.091,5.122,"1579《乌得勒支同盟》：北方联合的法理点。",BLUE,"hub"),
 P("多德雷赫特 Dordrecht",51.813,4.69,"荷兰省：多特大会之地。",GREEN,"city"),
 P("格罗宁根 Groningen",53.219,6.566,"北部一省。",BLUE,"city"),
 P("卢森堡 Luxembourg",49.611,6.132,"东南边缘的一省，面积大、人口稀。",VIO,"city"),
]
DORT=[
 P("多德雷赫特 Dordrecht",51.813,4.69,"1618–19 年国际性大会：修订 BC 文字，通过《多特信经》，三项联合信条在此齐备（CCI）。",GREEN,"core"),
 P("莱顿 Leiden",52.160,4.494,"阿米念曾任教于此；争论从教室走进全国（CCI）。",ORG,"hub"),
 P("海牙 The Hague",52.070,4.300,"三级会议政治中心，大会的召开背景。",BLUE,"city"),
 P("海德堡 Heidelberg",49.41,8.69,"普法尔茨派代表与会；HC 的出生地。",GREEN,"city"),
 P("日内瓦 Geneva",46.204,6.143,"瑞士教会派代表与会（一般史料）。",CY,"city"),
 P("伦敦 / 剑桥",51.51,-0.13,"英国教会派代表与会（一般史料）。",BLUE,"city"),
 P("埃姆登 Emden",53.367,7.206,"东弗里斯兰一线的改革宗网络。",GOLD,"city"),
 P("巴黎 Paris",48.857,2.352,"法国改革宗当时仍处逼迫中，大会记念这条线。",VIO,"city"),
]
WORLD=[
 P("多德雷赫特",51.813,4.69,"1619：三项联合信条在此定稿，成为后来移民与殖民教会的共同标准（CCI）。",GREEN,"core"),
 P("阿姆斯特丹",52.372,4.900,"荷兰改革宗的出发港之一。",BLUE,"hub"),
 P("开普敦 Cape Town",-33.925,18.424,"1652 年起荷兰改革宗在好望角建立会众；非洲荷兰语教会长期使用三项联合信条（一般史料）。",ORG,"hub"),
 P("大急流城 Grand Rapids",42.963,-85.668,"北美荷兰移民教会重镇；PRCA 等教会仍以三项联合信条为标准（一般史料）。",GOLD,"hub"),
 P("汉密尔顿 Hamilton, ON",43.255,-79.871,"加拿大改革宗教会（CanRC）与神学院所在（canadianreformedseminary.ca）。",GOLD,"hub"),
 P("阿纳海姆 Anaheim",33.836,-117.914,"北美联合改革宗教会（URCNA）等会众分布在北美西岸（urcna.org）。",GOLD,"city"),
 P("雅加达 Jakarta",-6.208,106.846,"印尼有继承荷兰改革宗传统的教会（一般史料；具体会名以各会自己的告白为准）。",CY,"city"),
 P("悉尼 Sydney",-33.869,151.209,"澳大利亚亦有认三项联合信条的改革宗教会（一般史料）。",CY,"city"),
 P("香港 / 华人教会",22.319,114.169,"CCI《赞美手册》中文版被华人改革宗教会使用；本站引文即据此。",RED,"hub"),
 P("洛杉矶 Los Angeles",34.052,-118.244,"恩约教会（ccreformed.org）等北美华人改革宗教会，认欧陆信条传统。",VIO,"city"),
]

def _js(mid, places, route=None, lines=None, view=None, z=5, maxZ=8):
    d=dict(p=places)
    if route: d['r']=route
    if lines: d['lines']=lines
    if view: d['view']=view; d['z']=z
    d['maxZ']=maxZ
    return f'<script type="application/json" class="mapdata" data-map="{mid}">{json.dumps(d,ensure_ascii=False)}</script>'

def _live(mid, cap):
    return (f'<figure class="livemap reveal"><div class="mapbar">'
      f'<label>在线底图</label><select class="tilesel" aria-label="选择地图底图"></select>'
      f'<span class="mapstat" aria-live="polite">等待加载</span></div>'
      f'<div class="livebox lmap" id="map-{mid}" data-map="{mid}" role="application" aria-label="{cap}"></div>'
      f'<figcaption>{cap} 可缩放、点标记看说明；滚轮缩放需先点击地图。底图可切换，某一源失败或超时会自动换下一个。'
      f'高德使用 GCJ-02 坐标，欧洲位置会偏移，只作中国大陆网络备用。Leaflet 已放在本站，不依赖 CDN。离线时请看示意图。</figcaption></figure>')

def duo(mid, title, svg, places, cap, route=None, lines=None, view=None, z=5, maxZ=8, cls=""):
    return (f'<div class="mapduo {cls}" id="duo-{mid}">'
            f'<figure class="sche reveal" aria-label="示意图：{title}">{svg}<figcaption><b>示意图（本站绘制，零网络）</b> · {cap}</figcaption></figure>'
            +_live(mid, title)+_js(mid, places, route, lines, view, z, maxZ)+'</div>')

# ---------- 示意 SVG ----------
def svg_bres():
    # stylized route through NW Europe
    return '''<svg class="sch" viewBox="0 0 900 420" role="img" aria-label="德布利一生路线示意图">
<defs><linearGradient id="gb1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#102044"/><stop offset="1" stop-color="#2a1d18"/></linearGradient>
<marker id="ar1" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#d4af37"/></marker></defs>
<rect width="900" height="420" rx="18" fill="url(#gb1)"/>
<text x="24" y="36" class="stitle">德布利的一生：一条被逼出来的路</text>
<text x="24" y="58" class="ssub">约 1522 蒙斯 → 伦敦避难 → 里尔地下 → 日内瓦受教 → 图尔奈写信条 → 色当 → 瓦朗谢讷殉道</text>
<path class="dash" marker-end="url(#ar1)" d="M210,250 C160,180 200,90 250,80 C320,65 380,95 330,160 C280,230 360,250 430,200 C520,140 560,210 620,240 C700,280 760,300 790,270"/>
<g class="pt" style="--c:#a78bfa"><circle cx="210" cy="250" r="9"/><text x="210" y="272" text-anchor="middle">① 蒙斯 出生</text></g>
<g class="pt" style="--c:#5aa9e6"><circle cx="250" cy="80" r="9"/><text x="236" y="98" text-anchor="end">② 伦敦 避难</text></g>
<g class="pt" style="--c:#d4af37"><circle cx="330" cy="160" r="9"/><text x="355" y="155">③ 里尔 地下牧养</text></g>
<g class="pt" style="--c:#6bb8d6"><circle cx="430" cy="200" r="9"/><text x="430" y="222" text-anchor="middle">④ 日内瓦 受教</text></g>
<g class="pt pulse core" style="--c:#e07a5f"><circle cx="620" cy="240" r="12"/><text x="620" y="262" text-anchor="middle">⑤ 图尔奈 1561</text></g>
<g class="pt pulse core" style="--c:#e07a5f"><circle cx="790" cy="270" r="12"/><text x="790" y="292" text-anchor="middle">⑥ 瓦朗谢讷 1567</text></g>
<text x="24" y="400" class="sfoot">记忆钩：南写北存——信条写在南部法语区，生命却在北方与流亡地延续。</text>
</svg>'''

def svg_refo():
    return '''<svg class="sch" viewBox="0 0 900 440" role="img" aria-label="宗教改革在欧洲的传播示意图">
<defs><linearGradient id="gb2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1430"/><stop offset="1" stop-color="#12243a"/></linearGradient></defs>
<rect width="900" height="440" rx="18" fill="url(#gb2)"/>
<text x="24" y="34" class="stitle">宗教改革怎样走到低地国家</text>
<text x="24" y="56" class="ssub">不是一条直线，是印刷、贸易、流亡与大学把告白带到各处。</text>
<path class="dash" d="M760,120 L560,200 L430,280 L280,160 L200,210"/>
<path class="dash delay" d="M430,280 L500,250 L620,300"/>
<path class="dash delay2" d="M280,160 L150,120 L80,200"/>
<g class="pt" style="--c:#e0a85f"><circle class="pulse" cx="760" cy="120" r="11"/><text x="760" y="102" text-anchor="middle">维滕贝格 1517</text></g>
<g class="pt" style="--c:#6bb8d6"><circle cx="560" cy="200" r="9"/><text x="560" y="222" text-anchor="middle">苏黎世</text></g>
<g class="pt" style="--c:#6bb8d6"><circle cx="430" cy="280" r="11"/><text x="430" y="302" text-anchor="middle">日内瓦 · 法国信条 1559</text></g>
<g class="pt pulse core" style="--c:#e07a5f"><circle cx="280" cy="160" r="12"/><text x="280" y="142" text-anchor="middle">图尔奈 · BC 1561</text></g>
<g class="pt" style="--c:#81b29a"><circle cx="200" cy="210" r="10"/><text x="80" y="230">海德堡 HC 1563</text></g>
<g class="pt" style="--c:#5aa9e6"><circle cx="150" cy="120" r="8"/><text x="150" y="104" text-anchor="middle">伦敦</text></g>
<g class="pt" style="--c:#5aa9e6"><circle cx="80" cy="200" r="8"/><text x="80" y="188" text-anchor="middle">爱丁堡</text></g>
<g class="pt" style="--c:#81b29a"><circle cx="620" cy="300" r="10"/><text x="620" y="322" text-anchor="middle">多德雷赫特 1619</text></g>
<text x="24" y="420" class="sfoot">BC 借鉴《法国信条》，但不是它的修订版（CCI）。三项联合信条在多特定齐。</text>
</svg>'''

def svg_prov():
    # 17 chips in rough geography (W=Flanders, E=Luxembourg, N=Groningen, S=Artois/Hainaut/Tournai)
    chips=[
      (420,50,"弗里斯兰",BLUE),(560,55,"格罗宁根",BLUE),(500,100,"上艾瑟尔",BLUE),(430,110,"乌得勒支",BLUE),
      (300,120,"荷兰",BLUE),(200,150,"泽兰",GREEN),(480,160,"海尔德兰",BLUE),(560,170,"聚特芬",BLUE),
      (250,200,"佛兰德",GOLD),(380,210,"布拉班特",ORG),(500,230,"林堡",VIO),(160,250,"阿图瓦",ORG),
      (300,260,"梅赫伦",ORG),(200,290,"里尔一带",ORG),(300,310,"埃诺",VIO),(250,350,"图尔奈区",RED),
      (420,300,"那慕尔",VIO),(580,290,"卢森堡",VIO),(380,160,"布鲁塞尔",ORG)
    ]
    g=""
    for x,y,n,c in chips:
        big = n in ("图尔奈区","布拉班特","荷兰")
        g+=f'<g class="chip{" pulse" if n=="图尔奈区" else ""}" style="--c:{c}"><rect x="{x-52}" y="{y-16}" rx="10" width="104" height="{32 if not big else 34}"/><text x="{x}" y="{y+5}" text-anchor="middle">{n}</text></g>'
    return f'''<svg class="sch" viewBox="0 0 760 460" role="img" aria-label="腓利二世治下低地十七省示意图">
<defs><linearGradient id="gb3" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0e2a22"/><stop offset="1" stop-color="#1a2038"/></linearGradient></defs>
<rect width="760" height="460" rx="18" fill="url(#gb3)"/>
<text x="24" y="32" class="stitle">低地十七省 · 1549 实用诏令之后</text>
<text x="24" y="54" class="ssub">拉丁文 Belgica＝整个低地，不单指今天的比利时。</text><text x="24" y="72" class="ssub">北（蓝）后来联合，南（金/红）多重新置于西班牙统治——大势，不是精确边界。</text>
<g transform="translate(0,40)">{g}</g>
<text x="24" y="444" class="sfoot">记忆钩：名字来自十七省；信条写在南部的图尔奈区。</text>
</svg>'''

def svg_mart():
    return '''<svg class="sch" viewBox="0 0 900 380" role="img" aria-label="逼迫与殉道地点示意图">
<defs><linearGradient id="gb4" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1010"/><stop offset="1" stop-color="#1a1020"/></linearGradient>
<radialGradient id="fl"><stop offset="0" stop-color="#ffd37a"/><stop offset="1" stop-color="#e07a5f00"/></radialGradient></defs>
<rect width="900" height="380" rx="18" fill="url(#gb4)"/>
<text x="24" y="34" class="stitle">十字架下的地理</text>
<text x="24" y="56" class="ssub">逼迫不是抽象气氛，是具体的城门、监狱与火刑柱。</text>
<circle cx="260" cy="200" r="70" fill="url(#fl)" class="glow"/>
<circle cx="520" cy="210" r="90" fill="url(#fl)" class="glow delay"/>
<g class="pt" style="--c:#e07a5f"><circle class="pulse" cx="200" cy="150" r="10"/><text x="200" y="132" text-anchor="middle">布鲁塞尔 1523 首批殉道</text></g>
<g class="pt pulse core" style="--c:#e07a5f"><circle cx="420" cy="190" r="13"/><text x="420" y="172" text-anchor="middle">图尔奈 1561 抛墙</text></g>
<g class="pt pulse core" style="--c:#e07a5f"><circle cx="620" cy="230" r="13"/><text x="620" y="252" text-anchor="middle">瓦朗谢讷 1567 殉道</text></g>
<g class="pt" style="--c:#e0a85f"><circle cx="500" cy="120" r="8"/><text x="520" y="110">安特卫普 · 禁书与圣像破坏</text></g>
<g class="pt" style="--c:#a78bfa"><circle cx="300" cy="260" r="8"/><text x="300" y="282" text-anchor="middle">里尔 · 地下教会</text></g>
<text x="24" y="360" class="sfoot">对照：第13条（护理）、第28条（即使面临死亡也当加入教会）、第36条（不是叛乱者）、第37条（那时真信仰要被承认）。</text>
</svg>'''

def svg_refu():
    return '''<svg class="sch" viewBox="0 0 900 400" role="img" aria-label="流亡教会网络示意图">
<defs><linearGradient id="gb5" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0c1c33"/><stop offset="1" stop-color="#163028"/></linearGradient></defs>
<rect width="900" height="400" rx="18" fill="url(#gb5)"/>
<text x="24" y="34" class="stitle">流亡教会：伦敦 · 埃姆登 · 法兰克福 · 韦瑟尔</text>
<text x="24" y="56" class="ssub">避难所、训练所、印刷所。第一届荷兰改革宗总会开在德国境内的埃姆登。</text>
<path class="sea" d="M40,300 C180,260 220,320 360,280 C500,240 560,300 860,250"/>
<path class="dash" d="M180,220 C260,180 400,200 520,140 C600,110 700,160 760,150"/>
<path class="dash delay" d="M400,250 L520,140 L620,80 L700,90"/>
<g class="boat"><polygon points="0,0 28,8 0,16 -4,8" fill="#d4af37"/><rect x="10" y="-16" width="3" height="20" fill="#f3e2a0"/></g>
<g class="pt" style="--c:#5aa9e6"><circle cx="180" cy="220" r="11"/><text x="180" y="202" text-anchor="middle">伦敦 奥斯丁会堂</text></g>
<g class="pt pulse core" style="--c:#e07a5f"><circle cx="700" cy="90" r="12"/><text x="700" y="72" text-anchor="middle">埃姆登 1571 总会</text></g>
<g class="pt" style="--c:#a78bfa"><circle cx="620" cy="80" r="9"/><text x="500" y="70">法兰克福</text></g>
<g class="pt" style="--c:#d4af37"><circle cx="520" cy="140" r="9"/><text x="520" y="162" text-anchor="middle">韦瑟尔 1568</text></g>
<g class="pt" style="--c:#6bb8d6"><circle cx="400" cy="250" r="8"/><text x="400" y="272" text-anchor="middle">日内瓦</text></g>
<text x="24" y="382" class="sfoot">没有这些城，南部被摧毁的会众就难以把告白带进 1571 与 1619。</text>
</svg>'''

def svg_dort():
    return '''<svg class="sch" viewBox="0 0 900 426" role="img" aria-label="多特大会示意图">
<defs><linearGradient id="gb6" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a2040"/><stop offset="1" stop-color="#2a2410"/></linearGradient></defs>
<rect width="900" height="426" rx="18" fill="url(#gb6)"/>
<text x="24" y="32" class="stitle">1618–19 · 多德雷赫特：一项国际会议</text>
<text x="24" y="54" class="ssub">CCI：代表主要来自荷兰改革宗教会，另有 27 位来自其他国家的教会。</text><text x="24" y="72" class="ssub">BC 在此经文字修订，与 HC、Dort 合成三项联合信条。</text>
<g transform="translate(0,26)"><!-- hall -->
<rect x="260" y="90" width="380" height="220" rx="14" fill="#243056" stroke="#d4af37" stroke-width="2"/>
<rect x="300" y="120" width="300" height="28" rx="6" fill="#d4af37" opacity=".9"/>
<text x="450" y="140" text-anchor="middle" fill="#1a1408" font-size="13" font-weight="700">多特大会主席台</text>
<g fill="#5aa9e6" opacity=".9">'''+ "".join(f'<rect x="{300+(i%8)*32}" y="{170+(i//8)*28}" width="22" height="14" rx="3"/>' for i in range(24)) +'''</g>
<text x="450" y="265" text-anchor="middle" class="ssub">荷兰代表</text>
<g class="pt" style="--c:#81b29a"><circle cx="200" cy="180" r="9"/><text x="200" y="162" text-anchor="middle">海德堡</text></g>
<g class="pt" style="--c:#6bb8d6"><circle cx="160" cy="280" r="9"/><text x="160" y="302" text-anchor="middle">日内瓦等瑞士教会</text></g>
<g class="pt" style="--c:#5aa9e6"><circle cx="720" cy="180" r="9"/><text x="720" y="162" text-anchor="middle">英国代表</text></g>
<g class="pt pulse core" style="--c:#d4af37"><circle cx="450" cy="80" r="10"/><text x="450" y="68" text-anchor="middle">多德雷赫特</text></g></g>
<text x="24" y="408" class="sfoot">记忆钩：Dort 不是另起炉灶，是为保护已有的恩典福音（拣选、十架、重生、持守）作国际裁决。</text>
</svg>'''

def svg_world():
    # decorative world + arcs from Dordrecht
    def xy(lo,la):
        return (lo+180)/360*860+20, (90-la)/180*300+70
    cities=[("多德雷赫特",4.69,51.81,GREEN),("开普敦",18.42,-33.93,ORG),("大急流城",-85.67,42.96,GOLD),
            ("汉密尔顿",-79.87,43.26,GOLD),("阿纳海姆",-117.91,33.84,GOLD),("雅加达",106.85,-6.21,CY),
            ("悉尼",151.21,-33.87,CY),("华人教会",114.17,22.32,RED),("洛杉矶",-118.24,34.05,VIO)]
    blobs=[(-100,45,90,40,BLUE,"北美"),(20,5,70,50,ORG,"非洲"),(10,50,50,28,GREEN,"欧洲"),
           (90,40,90,40,GOLD,"亚洲"),(134,-25,40,22,CY,"澳洲"),(120,-2,40,16,CY,"印尼")]
    b="".join(f'<ellipse cx="{xy(lo,la)[0]:.0f}" cy="{xy(lo,la)[1]:.0f}" rx="{rx}" ry="{ry}" fill="{c}" fill-opacity=".18" stroke="{c}" stroke-opacity=".4"/>'
              f'<text x="{xy(lo,la)[0]+(22 if lab=="非洲" else 0):.0f}" y="{xy(lo,la)[1]+(0 if lab=="非洲" else ry+12):.0f}" text-anchor="middle" class="rg">{lab}</text>' for lo,la,rx,ry,c,lab in blobs)
    o,dxy=xy(4.69,51.81)
    arcs=""
    for n,lo,la,c in cities[1:]:
        x,y=xy(lo,la)
        mx,my=(o+x)/2,(min(o,y)-40 if la<0 else (dxy+y)/2-30)
        arcs+=f'<path class="dash" d="M{o:.0f},{dxy:.0f} Q{mx:.0f},{my:.0f} {x:.0f},{y:.0f}" stroke="{c}"/>'
    pts=""
    for n,lo,la,c in cities:
        x,y=xy(lo,la)
        lx,ly,an={"开普敦":(x+12,y+18,"start"),"大急流城":(x-4,y-12,"end"),"汉密尔顿":(x+6,y-12,"start"),"阿纳海姆":(x,y+22,"middle"),"洛杉矶":(x-4,y-12,"end")}.get(n,(x,y-12,"middle"))
        pts+=f'<g class="pt" style="--c:{c}"><circle cx="{x:.0f}" cy="{y:.0f}" r="{12 if n=="多德雷赫特" else 7}"/><text x="{lx:.0f}" y="{ly:.0f}" text-anchor="{an}">{n}</text></g>'
    return f'''<svg class="sch" viewBox="0 0 900 420" role="img" aria-label="三项联合信条在世界的传播示意图">
<defs><linearGradient id="gb7" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1a33"/><stop offset="1" stop-color="#102210"/></linearGradient></defs>
<rect width="900" height="420" rx="18" fill="url(#gb7)"/>
<text x="24" y="32" class="stitle">从多德雷赫特到世界</text>
<text x="24" y="54" class="ssub">随荷兰移民、殖民与后来的宣教、华人教会网络传播。示意图不绘精确海岸线；认信以各教会自己的文件为准。</text>
{b}{arcs}{pts}
<text x="24" y="404" class="sfoot">北美：CanRC、URCNA、PRCA、HRC 等；非洲：南非荷兰语改革宗传统；亚洲：印尼与使用 CCI《赞美手册》的华人教会。</text>
</svg>'''

# captions (schematic)
CAP={
 "bres":"按人生顺序连线，不代表精确逐日行程；年份带“约”的是通识史料。",
 "refo":"年份是公开节点；福音与书籍的流动比线条更密。不绘海岸线。",
 "prov":"十七省色块为概念位置，不是历史边界；南北着色表示 1579 年后的大势。",
 "mart":"只标与 BC 直接相关的关键地点，不是殉道者全集。",
 "refu":"海上弧线为示意航路，不是某一次航行的日志。",
 "dort":"会场为示意；外国代表的城市是派出地，不是会址。",
 "world":"等距圆柱投影的装饰性世界图，位置近似；认信情况请核各会官方网站。",
}

def block_bres():
    route=[[50.454,3.952],[51.515,-0.083],[50.633,3.06],[46.52,6.63],[46.204,6.143],[50.607,3.389],[49.70,4.94],[51.219,4.402],[50.357,3.523]]
    return duo("bres","德布利的足迹",svg_bres(),BRES,CAP["bres"],route=route,view=[49.8,3.5],z=6,maxZ=9)

def block_refo():
    lines=[{"c":ORG,"w":2,"dash":"7 8","latlngs":[[51.866,12.643],[47.376,8.541],[46.204,6.143],[50.607,3.389]]},
           {"c":GREEN,"w":2,"dash":"7 8","latlngs":[[46.204,6.143],[49.41,8.69],[51.813,4.69]]}]
    return duo("refo","宗教改革在欧洲的传播",svg_refo(),REFM,CAP["refo"],lines=lines,view=[50,5],z=4,maxZ=7)

def block_prov():
    return duo("prov","腓利二世治下的低地十七省",svg_prov(),PROV,CAP["prov"],view=[51.0,4.5],z=7,maxZ=9)

def block_mart():
    return duo("mart","逼迫与殉道地点",svg_mart(),MART,CAP["mart"],view=[50.6,4.0],z=8,maxZ=10)

def block_refu():
    lines=[{"c":CY,"w":2,"dash":"6 7","latlngs":[[50.607,3.389],[51.5155,-0.0994],[51.66,6.62],[50.11,8.682],[53.367,7.206]]}]
    return duo("refu","流亡教会网络（伦敦、埃姆登、法兰克福、韦瑟尔）",svg_refu(),REFU,CAP["refu"],lines=lines,view=[51.5,3],z=5,maxZ=8)

def block_dort():
    return duo("dort","多特大会与派出地",svg_dort(),DORT,CAP["dort"],view=[51.2,4.2],z=6,maxZ=9)

def block_world():
    lines=[{"c":GOLD,"w":2,"dash":"6 8","latlngs":[[51.813,4.69],[42.963,-85.668]]},
           {"c":ORG,"w":2,"dash":"6 8","latlngs":[[51.813,4.69],[-33.925,18.424]]},
           {"c":RED,"w":2,"dash":"6 8","latlngs":[[51.813,4.69],[22.319,114.169]]}]
    return duo("world","三项联合信条在世界的传播",svg_world(),WORLD,CAP["world"],lines=lines,view=[20,20],z=2,maxZ=5,cls="wide")

def jumpbar():
    items=[("bres","👣","德布利足迹"),("refo","🔥","改革传播"),("prov","seventeen","十七省"),("mart","✝️","殉道地点"),("refu","🚢","流亡教会"),("dort","🏛️","多特大会"),("world","🌍","世界传播")]
    # avoid weird key
    items[2]=("prov","🛡️","十七省")
    return '<nav class="mapjump" aria-label="地图目录">'+"".join(f'<a href="#duo-{i}"><span>{ic}</span>{t}</a>' for i,ic,t in items)+'</nav>'

def part_atlas():
    b=pagecore("地图先看示意图：它在无网络时也能讲清关系。再打开右边（或下方）的实时地图，用多种底图核对位置。底图会自动回退。",
               "七张图：足迹 · 传播 · 十七省 · 殉道 · 流亡 · 多特 · 世界",
               "示意图由本站绘制，不绘精确国界。通史细节标“一般史料”或“约”；CCI 的记载单独写出。")
    b+=L2("at-how","2续.0","怎样用这些地图",
        cards([("📐","示意图永远在","SVG 画在页面里，不请求任何地图服务器。网络不稳时，先读示意图和表。",GOLD),
               ("🛰️","实时地图可换源","OpenStreetMap、OSM 法国/HOT、CARTO、Esri 街道/地形/卫星、OpenTopoMap；中国大陆可试高德（有偏移）。",BLUE),
               ("🔁","自动回退","某一源超时或连续失败，会换下一个。你的选择记在本地。",GREEN),
               ("📦","Leaflet 在本站","库文件放在 assets/leaflet/，不依赖任何外部 CDN；流程图库 Mermaid 同样放在本站 assets/mermaid/。",VIO)],"g4")
        +note("高德（AutoNavi）瓦片使用 GCJ-02，俗称火星坐标，在欧洲会整体偏移，不能当精确地理用，只作备用通道。"))
    b+=L2("at-bres","2续.1","德布利的足迹",
        '<p>一条路，把信条的语气说清楚：它为什么克制（要给国王看），又为什么温暖（要给受苦的会众用）。</p>'
        +jumpbar()+block_bres()
        +key("记忆钩：<b>南写北存</b>。写在图尔奈、殉于瓦朗谢讷；存活于埃姆登、米德尔堡、多德雷赫特。")
        +warn('<span class="mk-w">把这条路线当成精确到日的游记。</span> ✗ 若干年份是约数，连线只表示顺序与方向。'))
    b+=L2("at-refo","2续.2","宗教改革在欧洲怎样传到低地",
        '<p>低地国家不是路德的复制，也不是加尔文的行省。它有自己的城市、印刷所和殉道者。<span class="mk-u">《比利时信条》借鉴《法国信条》，但不是它的修订版</span>（CCI）。</p>'
        +block_refo()
        +stk(["节点","年份","与 BC 的关系"],[
          ["维滕贝格","1517","改革公开开始；低地很快有书籍与殉道（1523 布鲁塞尔）。"],
          ["日内瓦 / 法国总会","1559","《法国信条》比 BC 早两年（CCI）。"],
          ["图尔奈","1561","BC 写成：为抗议逼迫，并表明不是叛乱者（CCI）。"],
          ["海德堡","1563","HC：三项联合信条中负责牧养与教导的那一份。"],
          ["多德雷赫特","1618–19","文字修订 BC，通过 Dort，三项齐备（CCI）。"]])
        +mem("一条链：1517 点燃 → 1559 法国先写 → 1561 低地自己写 → 1563 要理问答 → 1619 定稿。"))
    b+=L2("at-prov","2续.3","十七省：为什么叫“比利时”信条",
        '<p><span class="mk-hl">Belgica 在十六世纪指整个低地十七省</span>，不是今天的比利时王国。1549 年查理五世的实用诏令把十七省绑成一个可继承的整体，腓利二世后来一并接收。信条用拉丁文 Confession Belgica，说的是这片土地上的教会。</p>'
        +block_prov()
        +cards([("🗣️","法语写成","作者来自瓦隆／埃诺，原文 Confession de foy；1562 年才有荷兰文译本。",GOLD),
                ("⚖️","南与北","南部（佛兰德、埃诺、图尔奈）逼迫最重，也是写作成熟之地；北部在叛乱与立国后成为信条的定居处。",BLUE),
                ("👑","哈布斯堡","宗教裁判、驻军与“血腥告示”，迫使教会在告白里同时讲真理与顺服（第36条）。",RED)],"g3")
        +hard("难点：不要用今天的比利时、荷兰、法国边界回读 1561。图尔奈今天在比利时，瓦朗谢讷今天在法国，当时同在哈布斯堡的低地世界里。"))
    b+=L2("at-mart","2续.4","逼迫与殉道：信条写成的地址",
        '<p>CCI 导言：当时荷兰的教会“受到罗马天主教政府极为残酷的逼迫”。德布利写信条，是要抗议逼迫，并向逼迫者表明：改革宗信徒不是叛乱者，而是照着圣经宣告真基督教信仰的守法公民。</p>'
        +block_mart()
        +app("读第13、28、36、37条时，把地点放回去：护理不是口号，加入教会不是安全的选择，顺服官长不是讨好，末日承认也不是遥远的诗句。"))
    b+=L2("at-refu","2续.5","流亡教会：伦敦、埃姆登、法兰克福、韦瑟尔",
        '<p>南部会众被打散以后，信仰没有消失，是沿着商路和海路转移到外侨教会。这些会堂既收留人，也印刷书、训练牧者、预备总会。</p>'
        +block_refu()
        +stk(["城","关键年份","作用"],[
          ["伦敦 奥斯丁会堂","约 1548–1553","爱德华六世时期的外侨教会；玛丽一世即位后许多人再逃（一般史料）。"],
          ["埃姆登","1571","流亡中的第一届荷兰改革宗总会；BC 成为合一告白（CCI 译作伊顿；采纳为一般史料）。"],
          ["法兰克福","十六世纪中叶","莱茵上游的外侨与印刷节点（一般史料）。"],
          ["韦瑟尔","1568","荷兰改革宗领袖会晤（CCI 教会规章导言）。"]])
        +key("记忆钩：<b>总会开在别人的土地上</b>——1571 年在埃姆登，说明当时这是一个流亡中的教会。"))
    b+=L2("at-dort","2续.6","多特大会：三项联合信条定齐的地方",
        '<p>CCI：多特大会召开，代表主要来自荷兰改革宗教会，另有 27 位来自其他国家的教会。大会修订 BC（主要在文字，不是内容），通过《多特信经》，并再次强调 HC 的教导地位。</p>'
        +block_dort()
        +warn('<span class="mk-w">多特是“荷兰地方小会”，或“发明了新教义”。</span> ✗ 它是国际性会议，目的是护住已有的恩典福音，驳回抗辩派的五点。'))
    b+=L2("at-world","2续.7","三项联合信条怎样走到世界",
        '<p>认信的传播，走的是移民船、殖民据点、后来的宣教和华人教会网络。<span class="mk-u">本图只标有公开资料可核的传统</span>，不替任何一座堂会“代认”。</p>'
        +block_world()
        +stk(["地区","可核的线索","说明"],[
          ["荷兰","多特、国家与自由教会传统","源头。"],
          ["南非","1652 年后的荷兰改革宗","长期使用三项联合信条（一般史料）。"],
          ["北美","canrc.org · urcna.org · prca.org · heritagereformed.com","移民教会及其分立／联合，多以三项联合信条为标准。"],
          ["亚洲与澳洲","印尼荷兰传统；CCI《赞美手册》；ccreformed.org","华人改革宗教会使用 CCI 中文；印尼、澳洲有认同一信条的会众（一般史料）。"]])
        +note("请以各教会官方网站的认信声明为准。本站是学习材料，不是任何总会的名录。"))
    return L1("atlas","2续","地图集：足迹、逼迫与传播","map","七张成对的地图：左边（或上方）是永远可看的示意图，右边是可换源的实时地图。",b)

def hist_more():
    """插在历史页 2.4 之后：导向地图集，并放入十七省与流亡的缩略说明。"""
    return (jumpbar().replace('href="#duo-','href="atlas.html#duo-')
            +'<p class="mapmore">更多成对地图（示意图 + 多源实时底图）见 <a href="atlas.html">二续 · 地图集</a>：宗教改革传播、十七省、殉道地点、流亡教会、多特大会、世界传播。</p>')
