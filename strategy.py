"""Experiment 52: Treasury curve-dispersion shock reversion.
Mechanism: an unusually large front-end versus long-end divergence at macro release is
liquidity fragmentation; belly duration mean-reverts as relative-value desks arbitrage.
Signal is causal ZF/ZB 08:30-09:00 direction difference, trade ZN 09:00-10:00.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np
FAMILY='rates-curve-dispersion-shock-reversion'
PARAMS={'observe_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':36000,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={s:np.zeros(len(d),dtype=np.int64)for s,d in p.items()}
 if not all(s in p for s in ('ZF','ZB','ZN')):return a
 side={}
 for s in ('ZF','ZB'):
  d=p[s];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
  for sess,g in d.groupby('session',sort=False).indices.items():
   x=g[t[g]==30600];y=g[t[g]==32400]
   if len(x)and len(y):side.setdefault(sess,{})[s]=int(np.sign(c[y[0]]-c[x[0]]))
 z=p['ZN'];t=z.ct_sec.to_numpy()
 for sess,g in z.groupby('session',sort=False).indices.items():
  q=side.get(sess,{})
  if q.get('ZF',0) and q.get('ZF')!=q.get('ZB'):a['ZN'][g[(t[g]>=32400)&(t[g]<36000)]]=-q['ZF']
 return a
