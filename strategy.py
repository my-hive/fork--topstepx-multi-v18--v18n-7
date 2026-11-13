"""Experiment 26: copper Asian-to-US industrial-demand handoff.
Mechanism: Asian industrial price discovery transmits to COMEX when US liquidity opens.
Observe 18:00-08:20 CT, trade 08:30-10:30. Falsifier: nonpositive PnL/era.
"""
import numpy as np
FAMILY='metals-copper-asia-us-handoff'
PARAMS={'observe_ct_sec':64800,'entry_ct_sec':30600,'exit_ct_sec':37800,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='HG':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==64800];y=g[t[g]==30600]
    if len(x)and len(y):o[g[(t[g]>=30600)&(t[g]<37800)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
