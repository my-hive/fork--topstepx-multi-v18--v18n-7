"""Experiment 68: silver-gold opening relative-value reversion.
Mechanism: SI higher-beta opening shock diverging from GC is temporary liquidity
fragmentation; silver reverts as metal-arbitrage desks restore relative pricing.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np
FAMILY='metals-silver-gold-opening-relativevalue-reversion'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':39600,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={s:np.zeros(len(d),dtype=np.int64)for s,d in p.items()}
 if not all(s in p for s in ('SI','GC')):return a
 sig={}
 for s in ('SI','GC'):
  d=p[s];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
  for sess,g in d.groupby('session',sort=False).indices.items():
   x=g[t[g]==30600];y=g[t[g]==32400]
   if len(x)and len(y):sig.setdefault(sess,{})[s]=int(np.sign(c[y[0]]-c[x[0]]))
 d=p['SI'];t=d.ct_sec.to_numpy()
 for sess,g in d.groupby('session',sort=False).indices.items():
  q=sig.get(sess,{})
  if q.get('SI',0) and q.get('GC',0) and q['SI']!=q['GC']:a['SI'][g[(t[g]>=32400)&(t[g]<39600)]]=-q['SI']
 return a
