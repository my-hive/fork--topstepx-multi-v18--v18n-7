"""Experiment 38: Treasury rare volatility-shock continuation.
Mechanism: unusually large post-08:30 rate repricing is information shock, not noise;
residual institutional hedging continues into noon. Prior 20 sessions set causal range norm.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np
FAMILY='rates-rare-volatility-shock-continuation'
PARAMS={'observe_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':43200,'lookback_sessions':20,'range_multiple':2.0,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZN':
   c,h,l,t=d.close.to_numpy(),d.high.to_numpy(),d.low.to_numpy(),d.ct_sec.to_numpy();gs=list(d.groupby('session',sort=False).indices.values());ranges=[]
   for k,g in enumerate(gs):
    x=g[(t[g]>=30600)&(t[g]<32400)]; r=(h[x].max()-l[x].min()) if len(x)else 0.;ranges.append(r)
    if k>=20 and len(x) and r>2*np.median(ranges[k-20:k]):
     side=int(np.sign(c[x[-1]]-c[x[0]]));o[g[(t[g]>=32400)&(t[g]<43200)]]=side
  a[s]=o
 return a
