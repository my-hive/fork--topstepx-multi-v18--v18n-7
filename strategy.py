"""Experiment 27: NQ post-close overnight reversal.
Mechanism: late-US liquidity exaggerates directional close; overnight market-making
inventory unwinds. Trade NQ 17:00-20:00 CT after prior RTH close impulse.
Falsifier: nonpositive stressed PnL or any era block <=0.
"""
import numpy as np
FAMILY='index-overnight-close-reversal'
PARAMS={'rth_end_ct_sec':54000,'entry_ct_sec':61200,'exit_ct_sec':72000,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='NQ':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==54000];y=g[t[g]==61200]
    if len(x)and len(y):o[g[(t[g]>=61200)&(t[g]<72000)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
