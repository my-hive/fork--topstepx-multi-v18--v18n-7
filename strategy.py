"""Experiment 91: micro EURUSD London opening continuation.
Mechanism: London interbank price discovery adds liquidity and carries pre-open direction;
M6E tests lower-cost implementation of European flow. Falsifier: PnL <=0 or era <=0.
"""
import numpy as np
FAMILY='fx-micro-eurusd-london-opening-continuation'
PARAMS={'observe_ct_sec':7200,'entry_ct_sec':10800,'exit_ct_sec':18000,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='M6E':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==7200];y=g[t[g]==10800]
    if len(x)and len(y):o[g[(t[g]>=10800)&(t[g]<18000)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
