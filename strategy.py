"""Experiment 82: crude-to-CAD commodity-currency lead-lag.
Mechanism: oil price shock changes Canadian terms of trade; CL discovery precedes CAD
futures repricing. Observe CL 08:30-09:00, trade 6C in same direction (CAD up with oil).
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np
FAMILY='fx-cad-crude-terms-of-trade-leadlag'
PARAMS={'observe_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':39600,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={s:np.zeros(len(d),dtype=np.int64)for s,d in p.items()}
 if not all(s in p for s in ('CL','6C')):return a
 side={};d=p['CL'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for sess,g in d.groupby('session',sort=False).indices.items():
  x=g[t[g]==30600];y=g[t[g]==32400]
  if len(x)and len(y):side[sess]=int(np.sign(c[y[0]]-c[x[0]]))
 d=p['6C'];t=d.ct_sec.to_numpy()
 for sess,g in d.groupby('session',sort=False).indices.items():
  if sess in side:a['6C'][g[(t[g]>=32400)&(t[g]<39600)]]=side[sess]
 return a
