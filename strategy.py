"""Experiment 65: JPY Tokyo cash-open carry unwind.
Mechanism: Tokyo cash equity and bank flows unwind thin overnight USDJPY carry moves.
Fade 6J 17:00-18:00 CT move through first Tokyo liquidity hour. Falsifier: PnL<=0/era<=0.
"""
import numpy as np
FAMILY='fx-tokyo-carry-unwind-reversal'
PARAMS={'observe_ct_sec':61200,'entry_ct_sec':64800,'exit_ct_sec':68400,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='6J':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==61200];y=g[t[g]==64800]
    if len(x)and len(y):o[g[(t[g]>=64800)&(t[g]<68400)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
