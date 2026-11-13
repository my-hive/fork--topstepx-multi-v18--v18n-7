"""Experiment 93: Treasury pre-cash range compression breakout.
Mechanism: unusually quiet early rate trading reflects dealer inventory balance; US cash
participation resolves latent macro positioning, so first cash-hour break continues.
Causal range norm from 20 completed sessions. Falsifier: PnL <=0 or any era <=0.
"""
import numpy as np
FAMILY='rates-pre-cash-highrange-exhaustion-reversion'
PARAMS={'range_start_ct_sec':25200,'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':39600,'lookback_sessions':20,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZN':
   c,h,l,t=d.close.to_numpy(),d.high.to_numpy(),d.low.to_numpy(),d.ct_sec.to_numpy();gs=list(d.groupby('session',sort=False).indices.values());rng=[]
   for k,g in enumerate(gs):
    pre=g[(t[g]>=25200)&(t[g]<30600)]; r=(h[pre].max()-l[pre].min()) if len(pre) else 0.;rng.append(r);x=g[t[g]==30600];y=g[t[g]==32400]
    if k>=20 and len(x)and len(y) and r>2*np.median(rng[k-20:k]):o[g[(t[g]>=32400)&(t[g]<39600)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
