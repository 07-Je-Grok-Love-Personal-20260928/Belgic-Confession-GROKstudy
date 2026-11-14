"""在线逐字核对：重新抓取 ccifellowship.org 每个源页面，确认 data/*.json 中每段原文（站点正文由它生成、verify_exact 已核对）仍与 CCI 网站逐字一致。
用法：python3 tools/verify_live.py"""
import json,re,html,urllib.request,concurrent.futures as cf
def norm(s): return re.sub(r'\s+','',s)
def fetch(u):
    for _ in range(3):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 GROKstudy-verifier'}),timeout=40)
            h=r.read().decode('utf-8','replace'); return norm(html.unescape(re.sub(r'<[^>]+>',' ',h)))
        except Exception as e: err=e
    raise err
def dat(x): return norm(re.sub(r'⟦(\d+)⟧',r'\1',x))
units=[]
c=json.load(open('data/creeds.json',encoding='utf-8'))
for k in ('apostles','nicene','athanasian'): units.append((c[k]['url'],c[k]['paras']))
bc=json.load(open('data/bc.json',encoding='utf-8'))
for a in bc['articles']: units.append((a['url'],[b['x'] for b in a['blocks'] if b['t'] in('p','h4')]))
hc=json.load(open('data/hc.json',encoding='utf-8'))
for l in hc['lds']: units.append((l['url'],[b['x'] for b in l['blocks'] if b['t'] in('p','h4')]))
dt=json.load(open('data/dort.json',encoding='utf-8'))
for h in dt['heads']:
    for i in h['items']: units.append((i['url'],[b['x'] for b in i['blocks'] if b['t'] in('p','h4')]))
tot=bad=0;pages=0;fe=0
with cf.ThreadPoolExecutor(8) as ex:
    futs={ex.submit(fetch,u):(u,ts) for u,ts in units}
    for f in cf.as_completed(futs):
        u,ts=futs[f]
        try: p=f.result(); pages+=1
        except Exception as e: fe+=1; print('FETCH-FAIL',u,e); continue
        for t in ts:
            tot+=1; d=dat(t); d2=norm(re.sub(r'⟦\d+⟧','',t))
            if d not in p and d2 not in p: bad+=1; print('DIFF',u,t[:60])
print('LIVE CCI pages',pages,'fetch-fail',fe,'paragraphs',tot,'mismatch',bad)
