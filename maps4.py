# -*- coding: utf-8 -*-
"""v4 地图集新增三对：八十年战争与南北分流、书与诗篇的印刷网络、三项联合信条的三座城。"""
from maps import P, duo, GOLD, BLUE, GREEN, RED, VIO, ORG, CY

WAR=[
 P("布里尔 Brielle",51.902,4.162,"1572 年 4 月 1 日“海上乞丐”攻占布里尔，北方起义由此打开局面（一般史料）。",BLUE,"hub"),
 P("莱顿 Leiden",52.160,4.494,"1574 年解围；1575 年创立莱顿大学，后来阿米念争论的教室（一般史料）。",ORG,"hub"),
 P("根特 Ghent",51.054,3.717,"1576《根特协定》：十七省一度联合驱逐西班牙驻军（一般史料）。",GOLD,"city"),
 P("乌得勒支 Utrecht",52.091,5.122,"1579《乌得勒支同盟》：北方诸省结盟，后来共和国的基础（一般史料）。",BLUE,"core"),
 P("阿拉斯 Arras",50.291,2.777,"1579《阿拉斯同盟》：南方瓦隆诸省回归国王（一般史料）。",RED,"hub"),
 P("海牙 The Hague",52.070,4.300,"1581《誓绝法案》：北方宣布不再效忠腓利二世（一般史料）。",BLUE,"hub"),
 P("安特卫普 Antwerp",51.219,4.402,"1585 年被帕尔马攻陷，新教徒限期离城，大批工匠、商人与牧者北迁（一般史料）。",RED,"core"),
 P("阿姆斯特丹 Amsterdam",52.372,4.900,"接纳南方难民，商业与印刷重心北移（一般史料）。",BLUE,"city"),
 P("明斯特 Münster",51.962,7.626,"1648《明斯特和约》：西班牙承认荷兰共和国独立，八十年战争结束（一般史料）。",GREEN,"hub"),
]
PRINT=[
 P("日内瓦 Geneva",46.204,6.143,"法文日内瓦诗篇在此成书（1562 年全本，一般史料）；瓦隆会众唱着它聚会。",CY,"hub"),
 P("安特卫普 Antwerp",51.219,4.402,"普朗坦（Plantin）1555 年在此开设印刷所；欧洲印刷中心，禁书也在此暗中流通（一般史料）。",ORG,"hub"),
 P("埃姆登 Emden",53.367,7.206,"流亡者的印刷基地：1562 年荷兰文“Deux-Aes 圣经”在此印行（一般史料）。",GOLD,"core"),
 P("海德堡 Heidelberg",49.410,8.690,"1563 HC 在此出版；1566 年达森（Datheen）荷兰文韵文诗篇在此印行（一般史料）。",GREEN,"core"),
 P("伦敦 London",51.5155,-0.0994,"奥斯丁会堂外侨教会：讲道、要理与诗篇的另一个出口（一般史料）。",BLUE,"city"),
 P("多德雷赫特 Dordrecht",51.813,4.690,"1618–19 多特大会决议重译圣经，1637 年《国译本》（Statenvertaling）出版（一般史料）。",GREEN,"hub"),
 P("图尔奈 Tournai",50.607,3.389,"1561 年会众公开唱诗游行，诗篇成了“十字架下的教会”的声音（一般史料）。",RED,"city"),
]
TRIAD=[
 P("图尔奈 Tournai",50.607,3.389,"1561《比利时信条》：37 条“我们相信”，向君王与世人公开表明信仰（CCI）。",GOLD,"core"),
 P("海德堡 Heidelberg",49.410,8.690,"1563《海德堡要理问答》：129 问，为教导青年与讲道而写（CCI）。",RED,"core"),
 P("多德雷赫特 Dordrecht",51.813,4.690,"1618–19《多特信经》：四项教义，回应抗辩派；三项联合信条在此齐备（CCI）。",GREEN,"core"),
]

def svg_war():
    marks=[(150,250,"1572 布里尔",BLUE),(255,190,"1574–75 莱顿",ORG),(420,150,"1579 乌得勒支同盟",BLUE),(360,300,"1576 根特协定",GOLD),
           (205,370,"1579 阿拉斯同盟",RED),(520,230,"1581 誓绝法案",BLUE),(330,250,"1585 安特卫普陷落",RED),(650,130,"1648 明斯特和约",GREEN)]
    g=""
    for i,(x,y,t,c) in enumerate(marks):
        core=" pulse core" if t.startswith(("1579 乌","1585")) else ""
        anchor="end" if x>600 else "start"
        dx=-14 if anchor=="end" else 14
        g+=f'<g class="pt{core}" style="--c:{c}"><circle cx="{x}" cy="{y}" r="{11 if core else 8}"/><text x="{x+dx}" y="{y+4}" text-anchor="{anchor}">{t}</text></g>'
    return f'''<svg class="sch" viewBox="0 0 900 440" role="img" aria-label="八十年战争与南北分流示意图">
<defs><linearGradient id="gw1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0f2240"/><stop offset="1" stop-color="#2a1612"/></linearGradient>
<marker id="arw" markerWidth="10" markerHeight="10" refX="7" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#f3d98b"/></marker></defs>
<rect width="900" height="440" rx="18" fill="url(#gw1)"/>
<text x="24" y="34" class="stitle">八十年战争（1568–1648）：信条为什么“南写北存”</text>
<text x="24" y="56" class="ssub">北方（蓝）结盟立国，南方（红）回归西班牙；1585 年安特卫普陷落后，人、书与教会一起北迁。</text>
<path d="M40,286 C220,270 420,322 860,250" fill="none" stroke="#f3d98b" stroke-width="2" stroke-dasharray="3 6" opacity=".7"/>
<text x="846" y="240" text-anchor="end" class="rg">大河一线（示意）：北 ↑ ／ 南 ↓</text>
<rect x="30" y="80" width="840" height="190" rx="14" fill="#5aa9e6" fill-opacity=".07"/>
<rect x="30" y="290" width="840" height="110" rx="14" fill="#e07a5f" fill-opacity=".08"/>
<path class="dash" marker-end="url(#arw)" d="M330,262 C340,220 380,190 440,170"/>
<text x="452" y="196" class="rg">1585 后北迁</text>
{g}
<text x="24" y="424" class="sfoot">记忆钩：1572 起义 · 1579 南北分盟 · 1581 誓绝 · 1585 北迁 · 1648 独立。BC 在南方写成，在北方被采纳与定稿。</text>
</svg>'''

def svg_print():
    nodes=[(130,300,"日内瓦 · 诗篇",CY),(300,180,"安特卫普 · 印刷所",ORG),(470,110,"埃姆登 · 流亡印刷",GOLD),(560,300,"海德堡 · HC 与荷文诗篇",GREEN),
           (140,140,"伦敦 · 外侨教会",BLUE),(700,170,"多德雷赫特 · 国译本",GREEN),(300,340,"图尔奈 · 唱诗游行",RED)]
    g=""
    for x,y,t,c in nodes:
        g+=(f'<g class="pt" style="--c:{c}"><rect x="{x-15}" y="{y-11}" width="30" height="22" rx="4" fill="{c}" fill-opacity=".85" stroke="#fff" stroke-width="1.5"/>'
            f'<path d="M{x},{y-9} L{x},{y+9}" stroke="#0b1636" stroke-width="1.5"/><text x="{x}" y="{y+30}" text-anchor="middle">{t}</text></g>')
    return f'''<svg class="sch" viewBox="0 0 860 420" role="img" aria-label="书与诗篇的印刷网络示意图">
<defs><linearGradient id="gp1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1b1433"/><stop offset="1" stop-color="#10283a"/></linearGradient></defs>
<rect width="860" height="420" rx="18" fill="url(#gp1)"/>
<text x="24" y="34" class="stitle">书与诗篇：信仰怎样被印出来、唱出来</text>
<text x="24" y="56" class="ssub">印刷所、诗篇与外侨教会连成一张网；信条与要理问答沿着这张网流动。</text>
<path class="dash" d="M130,300 C200,240 240,200 300,180"/><path class="dash delay" d="M300,180 C360,140 420,120 470,110"/>
<path class="dash delay2" d="M470,110 C520,170 540,240 560,300"/><path class="dash" d="M140,140 C220,150 260,165 300,180"/>
<path class="dash delay" d="M560,300 C620,250 660,210 700,170"/><path class="dash delay2" d="M300,340 C300,280 300,230 300,180"/>
{g}
<text class="rg" x="836" y="372" text-anchor="end">♪ 诗篇 · 📖 圣经 · ❓ 要理</text>
<text x="24" y="404" class="sfoot">记忆钩：日内瓦给旋律，安特卫普与埃姆登给印刷，海德堡给要理问答，多特给国译本。</text>
</svg>'''

def svg_triad():
    return '''<svg class="sch" viewBox="0 0 860 440" role="img" aria-label="三项联合信条的三座城示意图">
<defs><linearGradient id="gt1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14203f"/><stop offset="1" stop-color="#1d2a1a"/></linearGradient>
<radialGradient id="gt2"><stop offset="0" stop-color="#f3d98b" stop-opacity=".35"/><stop offset="1" stop-color="#f3d98b" stop-opacity="0"/></radialGradient></defs>
<rect width="860" height="440" rx="18" fill="url(#gt1)"/>
<text x="24" y="34" class="stitle">三份文件，三座城，一个信仰</text>
<text x="24" y="56" class="ssub">告白（向世界说）· 要理问答（向孩子与会众教）· 法规（向争议裁决）。</text>
<circle cx="430" cy="245" r="120" fill="url(#gt2)" class="glow"/>
<path class="dash" d="M210,330 L430,120"/><path class="dash delay" d="M430,120 L650,330"/><path class="dash delay2" d="M650,330 L210,330"/>
<g class="pt pulse core" style="--c:#d4af37"><circle cx="210" cy="330" r="15"/><text x="210" y="364" text-anchor="middle">图尔奈 · 1561</text><text x="210" y="382" text-anchor="middle">比利时信条 · 37 条</text></g>
<g class="pt pulse core" style="--c:#e07a5f"><circle cx="430" cy="120" r="15"/><text x="452" y="112">海德堡 · 1563</text><text x="452" y="92">海德堡要理问答 · 129 问</text></g>
<g class="pt pulse core" style="--c:#81b29a"><circle cx="650" cy="330" r="15"/><text x="650" y="364" text-anchor="middle">多德雷赫特 · 1618–19</text><text x="650" y="382" text-anchor="middle">多特信经 · 四项教义</text></g>
<text x="430" y="240" text-anchor="middle" class="stitle">三项联合信条</text>
<text x="430" y="262" text-anchor="middle" class="rg">同认三大普世信经 · 以圣经为最高权威</text>
<text x="24" y="424" class="sfoot">记忆钩：1561 说“我们相信”，1563 问“你唯一的安慰”，1619 答“恩典如何临到”。</text>
</svg>'''

CAP4={"war":"概念位置，不是战线图；年份为公开史实节点（一般史料）。",
      "print":"连线表示书籍、诗篇与人员的流向，不是某一次运输记录（一般史料）。",
      "triad":"三角为记忆用的概念图；三座城的位置以右侧实时地图为准。"}

def block_war():
    lines=[{"c":RED,"w":3,"dash":"8 8","latlngs":[[51.219,4.402],[52.372,4.900]]},{"c":BLUE,"w":2,"dash":"4 8","latlngs":[[51.902,4.162],[52.160,4.494],[52.091,5.122],[52.070,4.300]]}]
    return duo("war","八十年战争与南北分流（1568–1648）",svg_war(),WAR,CAP4["war"],lines=lines,view=[51.6,4.8],z=7,maxZ=9)
def block_print():
    lines=[{"c":CY,"w":2,"dash":"6 7","latlngs":[[46.204,6.143],[51.219,4.402],[53.367,7.206],[49.41,8.69],[51.813,4.69]]}]
    return duo("print","书与诗篇的印刷网络",svg_print(),PRINT,CAP4["print"],lines=lines,view=[50.5,5],z=5,maxZ=8)
def block_triad():
    lines=[{"c":GOLD,"w":3,"dash":"6 6","latlngs":[[50.607,3.389],[49.41,8.69],[51.813,4.69],[50.607,3.389]]}]
    return duo("triad","三项联合信条的三座城",svg_triad(),TRIAD,CAP4["triad"],lines=lines,view=[50.6,5.6],z=7,maxZ=8)
