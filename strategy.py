"""Experiment 37: Nikkei Asia-session continuation.
Mechanism: US close reprices global risk; Tokyo cash participation carries overnight
futures direction. Observe 17:00-18:00 CT, trade 18:00-20:00 CT.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np
FAMILY='index-nikkei-asia-session-continuation'
PARAMS={'observe_ct_sec':61200,'entry_ct_sec':64800,'exit_ct_sec':72000,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='NKD':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==61200];y=g[t[g]==64800]
    if len(x)and len(y):o[g[(t[g]>=64800)&(t[g]<72000)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
