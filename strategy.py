"""Experiment 121: Nasdaq earnings-season opening continuation.
Mechanism: concentrated tech earnings repricing produces sustained institutional index
hedging during Jan/Apr/Jul/Oct reporting windows. Follow cash-open NQ impulse.
Falsifier: stressed PnL <=0 or any era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='index-nasdaq-earnings-season-opening-reversal'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':39600,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='NQ':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();m=pd.to_datetime(d.session.astype(str).str[:10]).dt.month.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==30600];y=g[t[g]==32400]
    if len(x)and len(y)and m[g[0]] in [1,4,7,10]:o[g[(t[g]>=32400)&(t[g]<39600)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
