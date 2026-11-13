"""Experiment 32: NQ 08:30 macro-release drift.
Mechanism: scheduled labor/inflation releases establish index discount-rate repricing;
first half-hour reaction continues while cash market digests information.
Falsifier: stressed PnL <=0 or any era block <=0.
"""
import numpy as np
FAMILY='index-macro-release-drift-0830'
PARAMS={'observe_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='NQ':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==30600];y=g[t[g]==32400]
    if len(x)and len(y):o[g[(t[g]>=32400)&(t[g]<43200)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
