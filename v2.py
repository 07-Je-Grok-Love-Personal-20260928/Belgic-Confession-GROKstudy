# -*- coding: utf-8 -*-
"""v2 后处理：合并并压缩 CSS/JS、懒加载 Leaflet/Mermaid、预取、图片懒加载。"""
import re
from core import V
CSS = ["assets/styles.css", "assets/t87.css", "assets/bc.css", "assets/v2.css", "assets/v3.css"]
JS = ["assets/toc4.js", "assets/app.js", "assets/t87.js", "assets/bc.js", "assets/v2.js", "assets/maps.js"]

def _mincss(c):
    c = re.sub(r'/\*.*?\*/', '', c, flags=re.S)
    c = re.sub(r'\s+', ' ', c)
    c = re.sub(r'\s*([{};,>])\s*', r'\1', c)
    return c.replace(';}', '}').strip()

def bundle():
    css = "\n".join(open(f, encoding="utf-8").read() for f in CSS)
    css = css.replace("html[data-theme=dawn]", "html:is([data-theme=dawn],[data-theme=parch])")
    css = _mincss(css)
    import v4
    css = v4.css_v4(css) + "\n" + _mincss(open("assets/v4.css", encoding="utf-8").read())
    open("assets/site.css", "w", encoding="utf-8").write(css)
    js = "\n;".join(open(f, encoding="utf-8").read() for f in JS)
    open("assets/site.js", "w", encoding="utf-8").write(js)
    return len(css), len(js)

SPEC = '<script type="speculationrules">{"prefetch":[{"source":"document","where":{"selector_matches":"a[href$=\\".html\\"],a[href*=\\".html#\\"]"},"eagerness":"moderate"}]}</script>'
def post(h, k):
    h = re.sub(r'<link rel="stylesheet" href="assets/(?:styles|t87|bc)\.css\?v=[^"]+">', '', h)
    h = re.sub(r'<script src="assets/(?:app|t87|bc)\.js\?v=[^"]+" defer></script>', '', h)
    pre = ""
    if 'class="livebox"' in h or 'id="lmap"' in h:
        pre += ('<link rel="preconnect" href="https://tile.openstreetmap.org">'
                '<link rel="preconnect" href="https://basemaps.cartocdn.com" crossorigin>'
                '<link rel="preconnect" href="https://server.arcgisonline.com">')
    h = h.replace('</head>', pre + f'<link rel="stylesheet" href="assets/site.css?v={V}"></head>', 1)
    h = h.replace('</body>', f'<script src="assets/site.js?v={V}" defer></script>{SPEC}</body>', 1)
    h = re.sub(r'<img(?![^>]*\bloading=)', '<img loading="lazy" decoding="async"', h)
    return h
