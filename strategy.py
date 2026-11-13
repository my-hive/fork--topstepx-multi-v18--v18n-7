"""Experiment 123: soybean-oil biofuel hedge continuation.
Mechanism: energy-linked biodiesel hedgers transmit overnight soybean oil information
into US open; first opening response continues while commercial orders execute.
Falsifier: PnL <=0 or any era <=0.
"""
import numpy as np
FAMILY='grains-soyoil-usopen-biofuel-hedge-continuation'
PARAMS={'observe_ct_sec':28800,'entry_ct_sec':30600,'exit_ct_sec':37800,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZL':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==28800];y=g[t[g]==30600]
    if len(x)and len(y):o[g[(t[g]>=30600)&(t[g]<37800)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
