"""Experiment 96: EURUSD compressed-overnight US-open drift.
Mechanism: quiet overnight FX range stores unexecuted macro positioning; US cash/macro
liquidity releases it. Trade first US-hour impulse only after low causal overnight range.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np
FAMILY='fx-eurusd-compressed-overnight-usopen-drift'
PARAMS={'range_start_ct_sec':3600,'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':39600,'lookback_sessions':20,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='6E':
   c,h,l,t=d.close.to_numpy(),d.high.to_numpy(),d.low.to_numpy(),d.ct_sec.to_numpy();gs=list(d.groupby('session',sort=False).indices.values());rng=[]
   for k,g in enumerate(gs):
    pre=g[(t[g]>=3600)&(t[g]<30600)];r=(h[pre].max()-l[pre].min()) if len(pre) else 0.;rng.append(r);x=g[t[g]==30600];y=g[t[g]==32400]
    if k>=20 and len(x)and len(y) and r<np.median(rng[k-20:k]):o[g[(t[g]>=32400)&(t[g]<39600)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
