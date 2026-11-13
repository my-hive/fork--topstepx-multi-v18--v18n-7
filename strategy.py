"""Experiment 58: cross-index opening divergence reversion.
Mechanism: ES/NQ opposite opening impulses are temporary basket-price dislocation;
index arbitrage reverts NQ's idiosyncratic leg after 09:00.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np
FAMILY='index-cross-index-opening-divergence-reversion'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={s:np.zeros(len(d),dtype=np.int64)for s,d in p.items()}
 if not all(s in p for s in ('ES','NQ')):return a
 side={}
 for s in ('ES','NQ'):
  d=p[s];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
  for sess,g in d.groupby('session',sort=False).indices.items():
   x=g[t[g]==30600];y=g[t[g]==32400]
   if len(x)and len(y):side.setdefault(sess,{})[s]=int(np.sign(c[y[0]]-c[x[0]]))
 d=p['NQ'];t=d.ct_sec.to_numpy()
 for sess,g in d.groupby('session',sort=False).indices.items():
  q=side.get(sess,{})
  if q.get('ES',0) and q.get('ES')==-q.get('NQ',0):a['NQ'][g[(t[g]>=32400)&(t[g]<43200)]]=-q['NQ']
 return a
