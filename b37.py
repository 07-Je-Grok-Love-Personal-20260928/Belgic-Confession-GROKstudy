# -*- coding: utf-8 -*-
"""合并 37 条深读数据，并把〔…〕摘引转为逐字核对过的引文。"""
import re,html as H
from quotes import BC
import b37a,b37b,b37c
A={}; A.update(b37a.A); A.update(b37b.A); A.update(b37c.A)
BAD=[]
def qconv(n,s):
    def f(m):
        t=m.group(1); k=n
        mm=re.match(r"^(\d+):(.*)$",t,re.S)
        if mm: k=int(mm.group(1)); t=mm.group(2)
        if t not in BC[k]: BAD.append((n,k,t)); return "“"+t+"”"
        return f'<q class="cq" title="比利时信条第{k}条 · CCI 原文逐字">{H.escape(t,quote=False)}</q>'
    return re.sub(r"〔(.*?)〕",f,s)
for n,d in A.items():
    for k in list(d): d[k]=qconv(n,d[k])
assert sorted(A)==list(range(1,38)), sorted(A)
if __name__=="__main__":
    print(len(A)); [print("BAD",b) for b in BAD]
