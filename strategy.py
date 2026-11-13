"""Experiment 61: micro crude opening inventory reversion.
Mechanism: CL opening hedging and liquidity shock overshoots in thin early book;
market-maker inventory unwinds after first half-hour. Test lower-cost MCL contract.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np
FAMILY='energy-micro-crude-opening-inventory-reversion'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':36000,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='MCL':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==30600];y=g[t[g]==32400]
    if len(x)and len(y):o[g[(t[g]>=32400)&(t[g]<36000)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
