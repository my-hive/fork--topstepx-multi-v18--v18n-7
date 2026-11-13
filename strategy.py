"""Experiment 51: long-duration-to-belly Treasury lead-lag.
Mechanism: ZB has highest duration and reacts fastest to discount-rate news; ZN follows
when hedge demand spreads across curve. Observe ZB 08:30-09:00, trade ZN to noon.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np
FAMILY='rates-long-duration-to-belly-leadlag'
PARAMS={'observe_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={s:np.zeros(len(d),dtype=np.int64)for s,d in p.items()}
 if 'ZB' not in p or 'ZN' not in p:return a
 b,z=p['ZB'],p['ZN'];c,t=b.close.to_numpy(),b.ct_sec.to_numpy(); side={}
 for sess,g in b.groupby('session',sort=False).indices.items():
  x=g[t[g]==30600];y=g[t[g]==32400]
  if len(x)and len(y):side[sess]=int(np.sign(c[y[0]]-c[x[0]]))
 t=z.ct_sec.to_numpy()
 for sess,g in z.groupby('session',sort=False).indices.items():
  if sess in side:a['ZN'][g[(t[g]>=32400)&(t[g]<43200)]]=side[sess]
 return a
