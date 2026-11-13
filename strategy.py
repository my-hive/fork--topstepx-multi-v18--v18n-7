"""Experiment 64: GBP cross London-opening relative-value reversion.
Mechanism: EURGBP dealer fixing flow is mean reverting after London cash liquidity opens.
Use 6B (GBPUSD) as liquid GBP proxy; fade initial London-hour move 02:00-03:00 CT.
Falsifier: stressed PnL <=0 or any era PnL <=0.
"""
import numpy as np
FAMILY='fx-london-gbp-opening-relativevalue-reversion'
PARAMS={'observe_ct_sec':7200,'entry_ct_sec':10800,'exit_ct_sec':14400,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='6B':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==7200];y=g[t[g]==10800]
    if len(x)and len(y):o[g[(t[g]>=10800)&(t[g]<14400)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
