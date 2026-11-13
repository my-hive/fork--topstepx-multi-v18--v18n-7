"""Experiment 83: Treasury cash-close dealer hedge unwind.
Mechanism: cash-bond close hedging creates short-lived futures pressure; after 14:00 CT,
dealers unwind temporary duration inventory before futures settle. Fade 13:30-14:00 move.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np
FAMILY='rates-cash-close-dealer-hedge-unwind'
PARAMS={'observe_ct_sec':48600,'entry_ct_sec':50400,'exit_ct_sec':54000,'risk_dollars':250}
def entry_risk(p): return {s:np.full(len(d),250.,dtype=float) for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZN':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==48600];y=g[t[g]==50400]
    if len(x)and len(y):o[g[(t[g]>=50400)&(t[g]<54000)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
