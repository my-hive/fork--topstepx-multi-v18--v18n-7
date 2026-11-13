"""Experiment 50: front-end to 10-year curve transmission.
Mechanism: short-rate repricing via policy expectations leads broader curve adjustment;
large ZF move 08:30-09:00 predicts ZN direction 09:00-noon. Causal same-date observation.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np
FAMILY='rates-front-end-to-belly-transmission'
PARAMS={'observe_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={s:np.zeros(len(d),dtype=np.int64)for s,d in p.items()}
 if 'ZF' not in p or 'ZN' not in p:return a
 f,z=p['ZF'],p['ZN'];fc,ft=f.close.to_numpy(),f.ct_sec.to_numpy(); side={}
 for sess,g in f.groupby('session',sort=False).indices.items():
  x=g[ft[g]==30600];y=g[ft[g]==32400]
  if len(x)and len(y):side[sess]=int(np.sign(fc[y[0]]-fc[x[0]]))
 zt=z.ct_sec.to_numpy()
 for sess,g in z.groupby('session',sort=False).indices.items():
  if sess in side:a['ZN'][g[(zt[g]>=32400)&(zt[g]<43200)]]=side[sess]
 return a
