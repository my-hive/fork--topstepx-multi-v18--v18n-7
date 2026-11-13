"""Experiment 92: micro AUD commodity-risk confirmation continuation.
Mechanism: synchronized CL and AUD opening moves identify global commodity-risk flow;
M6A continues after US macro liquidity. Lower-cost micro implementation.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np
FAMILY='fx-micro-aud-commodity-risk-confirmation'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':39600,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={s:np.zeros(len(d),dtype=np.int64)for s,d in p.items()}
 if not all(s in p for s in ('CL','M6A')):return a
 sig={}
 for s in ('CL','M6A'):
  d=p[s];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
  for sess,g in d.groupby('session',sort=False).indices.items():
   x=g[t[g]==30600];y=g[t[g]==32400]
   if len(x)and len(y):sig.setdefault(sess,{})[s]=int(np.sign(c[y[0]]-c[x[0]]))
 d=p['M6A'];t=d.ct_sec.to_numpy()
 for sess,g in d.groupby('session',sort=False).indices.items():
  q=sig.get(sess,{})
  if q.get('CL',0) and q.get('CL')==q.get('M6A',0):a['M6A'][g[(t[g]>=32400)&(t[g]<39600)]]=q['M6A']
 return a
