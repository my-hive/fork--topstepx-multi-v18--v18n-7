"""Experiment 112: Russell overnight domestic-risk drift.
Mechanism: overnight US macro/news repricing persists in small-cap futures when US cash
liquidity broadens participation. Observe 02:00-08:30 and trade RTY through noon.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np
FAMILY='index-russell-overnight-domestic-risk-drift'
PARAMS={'observe_ct_sec':7200,'entry_ct_sec':30600,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='RTY':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==7200];y=g[t[g]==30600]
    if len(x)and len(y):o[g[(t[g]>=30600)&(t[g]<43200)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
