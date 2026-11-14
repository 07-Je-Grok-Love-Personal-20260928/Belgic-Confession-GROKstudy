# -*- coding: utf-8 -*-
"""v4：三级目录（编号、折叠、拖宽、搜索、滚动高亮）、标题层级 h1/h2/h3、部分编号重排后的站内引用、旧目录样式清理。"""
import re, html as H

CN = "零一二三四五六七八九十"
def cn2i(s):
    if s == "十": return 10
    if s.startswith("十"): return 10 + CN.index(s[1])
    if "十" in s:
        a, b = s.split("十"); return CN.index(a) * 10 + (CN.index(b) if b else 0)
    return CN.index(s)
def i2cn(n):
    if n <= 10: return "十" if n == 10 else CN[n]
    if n < 20: return "十" + CN[n - 10]
    return CN[n // 10] + "十" + (CN[n % 10] if n % 10 else "")
def bump(n): return n + 1 if n >= 3 else n   # v4：地图集成为第三部分，原三及以后各 +1

def remap_refs(h):
    """只改正文里指向本站各部分的引用（第X部分 / 见 N.M）。"""
    def part(m):
        nums = re.split(r'([、至])', m.group(3))
        out = "".join(x if x in "、至" else i2cn(bump(cn2i(x))) for x in nums)
        return m.group(1) + m.group(2) + out + m.group(4)
    h = re.sub(r'(本站|见|姊妹站与本站|与本站)(第)([一二三四五六七八九十、至]+)(部分)', part, h)
    h = re.sub(r'(">)(第)([一二三四五六七八九十、至]+)(部分</a>)', part, h)
    def dot(m):
        s = f'{m.group(1)}{m.group(2)}{bump(int(m.group(3)))}.{m.group(4)}'
        if m.group(5): s += f'{m.group(5)}{bump(int(m.group(6)))}.{m.group(7)}'
        return s
    h = re.sub(r'(见|本站|参见|详见|回看|部分)(\s?)(\d{1,2})\.(\d{1,2})(?:([–-])(\d{1,2})\.(\d{1,2}))?(?![\d.])', dot, h)
    return h

def split_num(t, lvl):
    if lvl == 1:
        m = re.match(r'^([一二三四五六七八九十]+)、(.*)$', t, re.S)
    else:
        m = re.match(r'^(\d+(?:\.\d+)+)\s+(.*)$', t, re.S)
    return (m.group(1), m.group(2)) if m else ("", t)

def toc_html(TOC, FILE, cur, emo):
    def li(lvl, href, sid, title, kids_html, page=None, iscur=False):
        n, t = split_num(title, lvl)
        if lvl == 1 and n: n = str(cn2i(n))
        e = emo(sid, title, lvl)
        has = bool(kids_html)
        cls = f'tk-i tk{lvl}' + (' has' if has else '') + (' is-cur' if iscur else '')
        tg = ('<button class="tk-tg" type="button" aria-expanded="false" aria-label="展开/收起"></button>'
              if has else '<span class="tk-sp"></span>')
        dp = f' data-page="{page}"' if page else ''
        return (f'<li class="{cls}"{dp}><div class="tk-row">{tg}<a href="{href}" data-s="{sid}">'
                f'<span class="tk-e">{e}</span><span class="tk-n">{n}</span><span class="tk-t">{t}</span></a></div>'
                + (f'<ol class="tk-l{lvl+1}">{kids_html}</ol>' if has else '') + '</li>')
    body = ""
    for l1id, l1t, subs, f in TOC:
        page = [k for k, ff in FILE.items() if ff == f][0]
        k2 = ""
        for sid, st, kids in subs:
            k3 = "".join(li(3, f'{f}#{i}', i, tt, "") for i, tt in kids)
            k2 += li(2, f'{f}#{sid}', sid, st, k3)
        body += li(1, f'{f}#{l1id}', l1id, l1t, k2, page=page, iscur=(page == cur))
    home = f'<a class="tk-home{" on" if cur=="index" else ""}" href="index.html"><span aria-hidden="true">🏠</span>首页 · 学习路径与进度</a>'
    return ('<nav id="toc" class="toc4" aria-label="目录"><div class="tk-head">'
            '<div class="tk-top"><b class="tk-title"><span aria-hidden="true">📑</span>目录</b>'
            '<button id="tocx" type="button" class="tk-b tk-x" aria-label="隐藏目录" title="隐藏目录">✕</button></div>'
            '<div class="tk-tools"><button type="button" class="tk-b" data-tk="open" title="展开全部层级">⊞ 全部展开</button>'
            '<button type="button" class="tk-b" data-tk="close" title="收起到一级">⊟ 收起</button>'
            '<button type="button" class="tk-b" data-tk="cur" title="定位到当前小节">◎ 定位当前</button></div>'
            '<label class="tk-q"><span aria-hidden="true">🔍</span><input id="tkq" type="search" placeholder="搜索目录（标题、条号）" autocomplete="off" aria-label="搜索目录"><em id="tkn" aria-live="polite"></em></label>'
            '<div class="tk-lv" aria-hidden="true"><span class="lv1">一级 · 部分</span><span class="lv2">二级 · 1.1</span><span class="lv3">三级 · 1.1.1</span></div></div>'
            f'<div class="tk-body" id="tkbody">{home}<ol class="tk-l1">{body}</ol><p class="tk-none" hidden>没有匹配的标题</p></div>'
            '<div id="tocgrip" role="separator" aria-orientation="vertical" tabindex="0" aria-label="拖动调整目录宽度（左右方向键微调，双击还原）" title="拖动调宽 · 双击还原"><i></i></div>'
            '</nav><div id="tkback" aria-hidden="true"></div>')

HEAD_INIT = ('<script>try{var de=document.documentElement,w=innerWidth,s=de.style,ls=localStorage;'
             'var a=+ls.getItem("tk4.w"),m=+ls.getItem("tk4.wm");'
             'if(a>=240&&a<=760)s.setProperty("--tkw",a+"px");'
             'if(m>=260&&m<=2000)s.setProperty("--tkwm",m+"px");'
             'if(ls.getItem("tk4.hide")==="1")de.classList.add("tk-hide")}catch(e){}</script>')

def shift_headings(h, index=False):
    """v4：页面层级 = 目录层级。部分标题 h1、二级 h2、三级 h3，其下卡片依次 h4–h5。首页保留 hero h1，其余标题加 .ixh 以沿用原样式。"""
    a = h.find('<main id="main">'); b = h.find('</main>', a)
    if a < 0: return h
    m = h[a:b]
    if index:
        m = re.sub(r'<(h[2-6])((?:\s[^>]*)?)>', lambda x: f'<{x.group(1)}{_addcls(x.group(2), "ixh")}>', m)
    else:
        m = re.sub(r'<(/?)h([2-6])\b', lambda x: f'<{x.group(1)}h{int(x.group(2))-1}', m)
    return h[:a] + m + h[b:]
def _addcls(attrs, c):
    if 'class="' in attrs: return attrs.replace('class="', f'class="{c} ', 1)
    return attrs + f' class="{c}"'

OLD_TOC = re.compile(r'#toc(?![a-z])|#tocgrip|tocopen|tochide|tocdrag|toc-open')
HTOK = re.compile(r'(?<![\w\-#.:])h([2-6])(?![\w\-])')
def css_v4(css):
    """去掉旧目录规则；标题选择器整体下移一级（h3→h2…），并为首页原层级保留一份 .ixh 副本。"""
    out = []; pos = 0
    for mm in re.finditer(r'([^{}]+)\{([^{}]*)\}', css):
        sel, dec = mm.group(1), mm.group(2)
        out.append(css[pos:mm.start()]); pos = mm.end()
        if OLD_TOC.search(sel): continue
        if sel.lstrip().startswith('@') or re.match(r'^\s*(from|to|\d+%)', sel):
            out.append(mm.group(0)); continue
        if HTOK.search(sel):
            shifted = HTOK.sub(lambda x: f'h{int(x.group(1))-1}', sel)
            orig = HTOK.sub(lambda x: f'h{x.group(1)}.ixh', sel)
            out.append(f'{shifted}{{{dec}}}{orig}{{{dec}}}')
        else:
            out.append(mm.group(0))
    out.append(css[pos:])
    return "".join(out)
