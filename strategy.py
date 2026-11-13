"""Experiment 33: EURUSD London morning liquidity reversion.
Mechanism: European dealer hedging before London morning fix temporarily overshoots;
liquidity providers fade last half-hour move. Signal and entry use completed bars only.
Falsifier: stressed PnL <=0 or any era PnL <=0.
"""
import numpy as np
FAMILY='fx-london-morning-liquidity-reversion'
PARAMS={'observe_ct_sec':19800,'entry_ct_sec':21600,'exit_ct_sec':23400,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='6E':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==19800];y=g[t[g]==21600]
    if len(x)and len(y):o[g[(t[g]>=21600)&(t[g]<23400)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
