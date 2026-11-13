"""Experiment 89: lean-hog cash-open commercial-flow continuation.
Mechanism: overnight processor and producer hedge demand carries into US livestock cash
market liquidity. Observe 02:00-08:30; follow through noon. Falsifier: PnL <=0 or era <=0.
"""
import numpy as np
FAMILY='livestock-hog-cashopen-commercial-continuation'
PARAMS={'observe_ct_sec':7200,'entry_ct_sec':30600,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(p): return {s:np.full(len(d),250.,dtype=float) for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='HE':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==7200];y=g[t[g]==30600]
    if len(x)and len(y): o[g[(t[g]>=30600)&(t[g]<43200)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
