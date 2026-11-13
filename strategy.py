"""Experiment 75: copper LME-to-COMEX overlap reversal.
Mechanism: London industrial hedging price discovery can overshoot as COMEX liquidity
joins; relative-value dealers fade pre-COMEX move. Observe 06:00-08:30, fade to 10:30.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np
FAMILY='metals-copper-lme-comex-overlap-reversal'
PARAMS={'observe_ct_sec':21600,'entry_ct_sec':30600,'exit_ct_sec':37800,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='HG':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==21600];y=g[t[g]==30600]
    if len(x)and len(y):o[g[(t[g]>=30600)&(t[g]<37800)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
