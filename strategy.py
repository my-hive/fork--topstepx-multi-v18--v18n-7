"""Experiment 88: wheat harvest delivery-pressure continuation.
Mechanism: Northern Hemisphere harvest delivery and elevator hedging pressure develops
overnight and continues into US grain liquidity during July-August. Falsifier: PnL<=0/era<=0.
"""
import numpy as np,pandas as pd
FAMILY='grains-wheat-harvest-delivery-continuation'
PARAMS={'observe_ct_sec':7200,'entry_ct_sec':30600,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZW':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();m=pd.to_datetime(d.session.astype(str).str[:10]).dt.month.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==7200];y=g[t[g]==30600]
    if len(x)and len(y)and m[g[0]] in [7,8]:o[g[(t[g]>=30600)&(t[g]<43200)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
