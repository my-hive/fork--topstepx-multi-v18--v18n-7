"""Experiment 129: gold macro-release dollar-confirmed continuation.
Mechanism: inflation/rate surprise drives opposite gold-dollar repricing; when GC and
EURUSD inverse moves agree, macro hedge demand continues after first 30 minutes.
Falsifier: PnL <=0 or any era <=0.
"""
import numpy as np
FAMILY='metals-gold-macro-dollar-confirmed-reversal'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':39600,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={s:np.zeros(len(d),dtype=np.int64)for s,d in p.items()}
 if not all(s in p for s in ('GC','M6E')):return a
 q={}
 for s in ('GC','M6E'):
  d=p[s];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
  for x,g in d.groupby('session',sort=False).indices.items():
   u=g[t[g]==30600];v=g[t[g]==32400]
   if len(u)and len(v):q.setdefault(x,{})[s]=int(np.sign(c[v[0]]-c[u[0]]))
 d=p['GC'];t=d.ct_sec.to_numpy()
 for x,g in d.groupby('session',sort=False).indices.items():
  z=q.get(x,{})
  if z.get('GC',0) and z.get('GC')==-z.get('M6E',0):a['GC'][g[(t[g]>=32400)&(t[g]<39600)]]=-z['GC']
 return a
