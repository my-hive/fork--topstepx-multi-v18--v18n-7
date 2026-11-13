"""Experiment 133: MGC opening volatility-shock reversion.
Mechanism: exceptional COMEX opening range is stop/liquidity cascade and mean reverts
as bullion dealers replenish inventory. Causal 20-session range benchmark.
Falsifier: PnL <=0 or any era PnL <=0.
"""
import numpy as np
FAMILY='metals-micro-gold-opening-volatility-continuation'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':39600,'lookback_sessions':20,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='MGC':
   c,h,l,t=d.close.to_numpy(),d.high.to_numpy(),d.low.to_numpy(),d.ct_sec.to_numpy();gs=list(d.groupby('session',sort=False).indices.values());r=[]
   for k,g in enumerate(gs):
    x=g[(t[g]>=30600)&(t[g]<32400)];v=h[x].max()-l[x].min() if len(x) else 0.;r.append(v)
    if k>=20 and len(x)and v>2*np.median(r[k-20:k]):o[g[(t[g]>=32400)&(t[g]<39600)]]=int(np.sign(c[x[-1]]-c[x[0]]))
  a[s]=o
 return a
