"""Experiment 53: EURUSD London-New York overlap trend.
Mechanism: European macro and flows establish a London-morning trend, then US real-money
participation continues it during overlap. Observe 03:00-07:00 CT; trade 07:00-09:00.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np
FAMILY='fx-london-newyork-overlap-trend'
PARAMS={'observe_ct_sec':10800,'entry_ct_sec':25200,'exit_ct_sec':32400,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='6E':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==10800];y=g[t[g]==25200]
    if len(x)and len(y):o[g[(t[g]>=25200)&(t[g]<32400)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
