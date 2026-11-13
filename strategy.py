"""Experiment 124: copper dollar-confirmed opening continuation.
Mechanism: a synchronized inverse dollar/copper opening move identifies macro-industrial
flow, which persists as COMEX hedgers execute. Falsifier: PnL<=0 or any era<=0.
"""
import numpy as np
FAMILY='metals-copper-dollar-confirmed-opening-continuation'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':39600,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={s:np.zeros(len(d),dtype=np.int64)for s,d in p.items()}
 if not all(s in p for s in ('HG','M6E')):return a
 q={}
 for s in ('HG','M6E'):
  d=p[s];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
  for x,g in d.groupby('session',sort=False).indices.items():
   u=g[t[g]==30600];v=g[t[g]==32400]
   if len(u)and len(v):q.setdefault(x,{})[s]=int(np.sign(c[v[0]]-c[u[0]]))
 d=p['HG'];t=d.ct_sec.to_numpy()
 for x,g in d.groupby('session',sort=False).indices.items():
  z=q.get(x,{});
  if z.get('HG',0) and z.get('HG')==-z.get('M6E',0):a['HG'][g[(t[g]>=32400)&(t[g]<39600)]]=z['HG']
 return a
