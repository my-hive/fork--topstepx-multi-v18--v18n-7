"""Experiment 34: gold London-session drift continuation.
Mechanism: London bullion liquidity establishes price discovery ahead of COMEX;
last half-hour London move continues into US pre-open. Falsifier: PnL<=0 or era<=0.
"""
import numpy as np
FAMILY='metals-london-session-drift'
PARAMS={'observe_ct_sec':32400,'entry_ct_sec':34200,'exit_ct_sec':37800,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='GC':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==32400];y=g[t[g]==34200]
    if len(x)and len(y):o[g[(t[g]>=34200)&(t[g]<37800)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
