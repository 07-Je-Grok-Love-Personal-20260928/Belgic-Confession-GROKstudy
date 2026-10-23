import re
# -*- coding: utf-8 -*-
"""第三部分：三十七条逐条深读（核心页）。"""
import html as H
from core import *
from c_common import *
from widgets import *
from whole import pagecore
from b37 import A, BAD
from c_titles import BC37, BC_GROUPS
from c_core import BC_CORE, core_strip
from libs import rdet, bc_rows, J, fn
from c_bc import bcmap
assert not BAD, BAD
GI={
"g1":("先有神，后有一切；先有话语，后有认识。","第1条宣告神是谁，第2–7条回答“我们怎样认识他”：创造与圣言两条路、圣经的来源、正典、权威、次经、充分性。<b>六条写圣经，在16世纪的信条中极为罕见</b>——因为与罗马的根本争论就是“权威在哪里”。整组的逻辑是：神（1）→ 启示（2）→ 成文（3）→ 范围（4、6）→ 权威（5）→ 充分（7）。",
      "“唯独圣经”不是“只要圣经、不要信条”；而是圣经是唯一不受检验的准则，信条本身也在它之下（第7条）。"),
"g2":("一位神，三个位格：救恩的根就在三一神里。","第8条下定义，第9条给证据（并接受三大信经），第10条论子的神性，第11条论圣灵的神性。这组把改革宗<b>牢牢接在古代大公教会之上</b>：我们不是新宗教。",
      "三一的“一”与“三”不在同一层面：本质是一，位格是三。"),
"g3":("神造、神管、人堕落、罪遍及。","创造（12）、护理（13）、人的被造与堕落（14）、原罪（15）。这组是福音的“背景布”：没有创造，就没有对神的亏欠；没有堕落，就不需要救主。第13条也是全信条最温暖的安慰条文之一。",
      "神掌管一切（13），人却全然败坏（14–15）：神不是罪的创造者，人对罪负全责——信条在此拒绝越界推理。"),
"g4":("从拣选到中保：救恩的源头、成就与施行。","拣选（16）→ 应许（17）→ 道成肉身（18）→ 二性一位（19）→ 公义与怜悯（20）→ 大祭司的补赎（21）→ 因信称义（22–23）→ 成圣与善行（24）→ 律法的成全（25）→ 唯一中保（26）。<b>这十一条是全信条的心脏</b>，正好对应使徒信经第二段与 HC 第二部分。",
      "拣选只有一条（16），却放在救恩链的最前面——意思是：救恩从神开始，不从人开始。"),
"g5":("教会：基督永远有他的子民，也给她清楚的标志与秩序。","大公教会（27）、加入的责任（28）、真假教会与真信徒的标志（29）、治理（30）、职分的产生（31）、秩序与纪律（32）。<b>这是“十字架下的教会”最急需的部分</b>：秘密聚会的信徒要知道哪里是真教会、怎样有秩序地生存。",
      "“救恩不在她之外”（28）与“真信徒的圣会”（27）要一起读：教会是神施恩的常规场所，不是救恩的来源。"),
"g6":("可见的道：两个圣礼印证一个应许。","圣礼总论（33）、洗礼（34）、圣餐（35）。这组同时面对三条战线：罗马（七圣礼、化质说）、路德派（口吃基督身体）、重洗派（反对婴孩洗礼、重洗）。<b>第34条是三项联合信条中圣约神学最明确的条文</b>。",
      "圣礼“表明并印证”恩典，却不自动产生恩典；功效在于圣灵与信心。"),
"g7":("今世的秩序与末日的盼望。","官长（36）与末日审判（37）。第36条直接回应“叛乱者”的指控：顺服、纳税、代祷，但“在不违反圣经的一切事上”；第37条把殉道者的冤屈交给那位大审判官——今天被定为异端的信仰，那日要被神子承认为真。",
      "第36条有删改史（CCI 注：一句于1905年删除）；读它要分清原则（神设官长、顺服有界）与16世纪的政教处境。")}
FAC=[("why","🕰️","为何写 · 真实处境","#e07a5f"),("say","📜","写了什么 · 原文要义","#d4af37"),("bt","📖","圣经神学 · 整本圣经的线","#5aa9e6"),
     ("ct","🤝","圣约神学 · 约的角度","#81b29a"),("foe","⚔️","对手与界限 · 它反对什么","#c9a0dc"),("x","🔗","互参 · HC / Dort / 威斯敏斯特","#6bb8d6")]

WARN={
 2:"误读：受造界与良心既然也像一本书，人就能靠自然得救。——不对。自然启示使人<b>无可推诿</b>；认识救恩，要靠第二本书：圣经。",
 5:"误读：圣经的权威来自教会认可。——不对。教会<b>承认</b>正典，并不<b>授予</b>正典权威；权威来自神自己，并由圣灵在心里印证。",
 14:"误读：人全然败坏，所以人对罪不负责任。——不对。人失去的是<b>行善得救的能力</b>，不是责任；败坏正是人有罪的证明。",
 16:"误读：拣选＝宿命论，人做什么都无所谓。——不对。本条要显明的是<b>怜悯与公义</b>，目的是安慰信徒、归荣耀给神，不是让人放弃悔改与信心。",
 22:"误读：信心本身是一种功劳，所以我信就换来称义。——不对。信心只是<b>工具</b>（手），抓住的是基督和他的义；称义的根据只在基督。",
 24:"误读：既然因信称义，好行为可有可无。——不对。真信心必然<b>结出</b>好行为；好行为是果子，不是根基，不能作称义的理由。",
 27:"误读：大公教会＝罗马天主教会。——不对。这里的大公指<b>普世、历代</b>一切真信徒的会众，不是某个宗派的名字。",
 29:"误读：真教会就是没有罪人、没有问题的教会。——不对。标记看的是<b>纯正传讲福音、正确施行圣礼、施行教会惩戒</b>，不是成员已经完美。",
 34:"误读：受洗这个动作本身就自动使人重生。——不对。水洗是<b>记号与印证</b>，真正洗净的是基督的血与圣灵的工作。",
 35:"误读：圣餐只是一场纪念会，或饼杯变成了肉身。——两头都不对。本条说信徒藉<b>圣灵与信心</b>真实地领受基督，不是变质，也不只是回忆。",
 36:"误读：本条可以原样套到今天的政教关系。——要小心。本条写于国家教会时代；今天不少改革宗教会对其中官员与教会关系的措辞另有说明，读时应看所属教会采用的版本。",
 37:"误读：最后审判只该让信徒害怕。——不对。对信徒，这日是<b>安慰与盼望</b>：他们的冤屈要得伸张，神的儿女要得着荣耀。",
}
def art(n,col,lab):
    d=A[n]; t,kw,ico=BC37[n]
    D=J("bc")["articles"][n-1]
    full="".join(f'<p class="ex">{fn(b["x"])}</p>' for b in D["blocks"] if b["t"]=="p")
    fac='<div class="fac">'+"".join(f'<div class="fc" style="--c:{c}"><h5><i>{i}</i>{tt}</h5><p>{d[k]}</p></div>' for k,i,tt,c in FAC[:4])+'</div>'
    more='<details class="fmore"><summary><span>⚔️ 对手与界限</span><span>🔗 互参 HC · Dort · 威斯敏斯特</span><small>次要 · 点开</small></summary><div class="fac f2">'+"".join(f'<div class="fc" style="--c:{c}"><h5><i>{i}</i>{tt}</h5><p>{d[k]}</p></div>' for k,i,tt,c in FAC[4:])+'</div></details>'
    body=(f'<div class="l3m"><span class="pch p2" style="background:{col}">{lab}</span><span class="qr">{BCT[n]}</span><span class="kw">{"".join(f"<i>{w}</i>" for w in kw.replace("＋","·").split("·"))}</span></div>'
          +core_strip(BC_CORE[n])+fac+'<div class="kha">'+key(d["key"])+hard(d["hard"])+app(d["app"])+'</div>'+(warn(re.sub(r'^误读：(.*?)——',r'<span class="mk-w">\1</span> ✗ ',WARN[n])) if n in WARN else '')
          +f'<div class="hookbar"><span>🧠 <b>记忆钩</b><span class="mk-hl">{d["hook"]}</span></span><span>📖 <b>钥节</b>{d["vs"]}</span></div>'+more
          +f'<details class="ftx"><summary>📜 第{n}条 CCI 原文全文（逐字） <small>点开阅读 · 可朗读</small></summary><div class="ftb" id="ft{n}">{full}</div>'
          +f'<p class="spk"><button class="btn ghost" type="button" data-speak="#ft{n}">🔊 朗读本条</button><button class="btn ghost" type="button" data-stop>⏹ 停止</button> <a href="bct.html#bc-{n}">背诵版</a> · <a href="{D["url"]}" target="_blank" rel="noopener">CCI 原文页 ↗</a></p>'
          +rdet(f"第{n}条",bc_rows(n),sum(len(x) for _,x in bc_rows(n)))+'</details>')
    return L3(f"bx-{n}",f"第{n}条 · {t}",body,ico,sub=f"BC {n}",cls="ldc")
def charts():
    D=J("bc")["articles"]; L={a["n"]:sum(len(b["x"]) for b in a["blocks"] if b["t"]=="p") for a in D}
    col={}; 
    for g,lab,c,lo,hi,ico in BC_GROUPS:
        for n in range(lo,hi+1): col[n]=(c,lab)
    mx=max(L.values()); tot=sum(L.values())
    bars="".join(f'<a class="cb" href="#bx-{n}" style="--c:{col[n][0]};--h:{L[n]/mx:.3f};--i:{n}" title="第{n}条 · {L[n]} 字"><i></i><small>{n}</small></a>' for n in range(1,38))
    # donut by chars per group
    r=54; C=2*3.14159*r; off=0; seg=""; leg=""
    for g,lab,c,lo,hi,ico in BC_GROUPS:
        v=sum(L[n] for n in range(lo,hi+1)); f=v/tot
        seg+=f'<circle r="{r}" cx="70" cy="70" fill="none" stroke="{c}" stroke-width="22" stroke-dasharray="{f*C:.1f} {C:.1f}" stroke-dashoffset="{-off*C:.1f}"/>'
        leg+=f'<li style="--c:{c}"><i></i>{lab}<b>{round(f*100)}%</b><small>{hi-lo+1} 条</small></li>'; off+=f
    donut=f'<div class="donut"><svg viewBox="0 0 140 140" role="img" aria-label="七群篇幅占比"><g transform="rotate(-90 70 70)">{seg}</g><text x="70" y="66" text-anchor="middle" class="dn1">37</text><text x="70" y="86" text-anchor="middle" class="dn2">条 · {tot//100*100}+ 字</text></svg><ul>{leg}</ul></div>'
    return (f'<div class="chartrow"><figure class="chart"><figcaption>📊 每条篇幅（CCI 原文字数，柱高＝长度；点柱跳转）</figcaption><div class="cbars">{bars}</div>'
            f'<p class="cnote">最长的几条：第{"、".join(str(n) for n in sorted(L,key=L.get,reverse=True)[:4])}条。其中第34、35条（洗礼、圣餐）篇幅长，是因为这正是当年与罗马、路德宗、重洗派三方同时争论的地方。</p></figure>'
            f'<figure class="chart"><figcaption>🍩 七群篇幅占比</figcaption>{donut}</figure></div>')
def part_bc():
    b=pagecore("37 条逐条：为何写（处境）→ 写了什么（CCI 原文）→ 圣经神学 → 圣约神学 → 对手与界限 → 互参 → 重点、难点、应用、记忆钩。",
               "七群：神与启示 1–7｜三一 8–11｜创造与人 12–15｜拣选与基督 16–26｜教会 27–32｜圣礼 33–35｜官长与末日 36–37",
               "第13条（神命定一切而非罪的创造者）、第16条（拣选与任凭）、第19条（二性一位）、第35条（属灵的真实临在）、第36条（1905年删改）。",
               "每条的彩色“原文要义”中，带下划线的引文全部逐字取自 CCI《赞美手册》，构建时程序核对。")
    b+=L2("bx-map","3.1","三十七条地图：一眼看全",'<p>点任一方块，跳到本页该条的深读；颜色＝七群（本站分组）。</p>'+bcmap().replace('href="#bc-','href="#bx-').replace("点任一方块跳到原文","点任一方块跳到该条深读")
        +flow([("神与启示","1–7","#5aa9e6"),("三位一体","8–11","#a78bfa"),("创造与人","12–15","#81b29a"),("拣选与基督","16–26","#d4af37"),("教会","27–32","#e07a5f"),("圣礼","33–35","#6bb8d6"),("官长·末日","36–37","#c9a0dc")])
        
        +charts()
        +key("<b>读法：</b>先读每组的导语（为什么这几条放在一起），再读每条的六面卡片；最后点开“CCI 原文全文”，对照原文再读一遍。"))
    for g,lab,col,lo,hi,ico in BC_GROUPS:
        one,intro,hd=GI[g]
        x=f'<div class="gintro reveal" style="--c:{col}"><p class="g1">{one}</p><p>{intro}</p></div>'+hard(hd)
        for n in range(lo,hi+1): x+=art(n,col,lab)
        b+=L2(f"bx-{g}","3.x",f"{lab}（第{lo}–{hi}条）",x)
    return L1("bc","三","三十七条逐条深读","scroll","每一条：真实处境、原文要义（CCI 逐字）、圣经神学、圣约神学、对手、互参、重点难点、应用与记忆钩。",b)
