"""Experiment 81: soybean commercial inventory reversion.
Mechanism: soybean processor and elevator hedging pushes prior-day price moves beyond
cash-market equilibrium; next US session reverses as crush demand absorbs inventory.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np
FAMILY='grains-soy-commercial-inventory-reversion'
PARAMS={'entry_ct_sec':30600,'exit_ct_sec':46800,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZS':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();gs=list(d.groupby('session',sort=False).indices.values());r=np.array([c[g[-1]]-c[g[0]] for g in gs])
   for k in range(1,len(gs)):
    g=gs[k];o[g[(t[g]>=30600)&(t[g]<46800)]]=-int(np.sign(r[k-1]))
  a[s]=o
 return a
