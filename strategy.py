"""Experiment 63: rare, cross-index-confirmed Russell opening shock.
Mechanism: ETF/basket imbalance only merits trade when ES confirms sign and M2K opening
move exceeds its causal 20-session median; then component basket execution continues.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np
FAMILY='equity-russell-confirmed-opening-shock'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':43200,'lookback_sessions':20,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={s:np.zeros(len(d),dtype=np.int64)for s,d in p.items()}
 if not all(s in p for s in ('ES','M2K')):return a
 signals={}
 for s in ('ES','M2K'):
  d=p[s];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();gs=list(d.groupby('session',sort=False).indices.values());v={}
  for g in gs:
   x=g[t[g]==30600];y=g[t[g]==32400]
   if len(x)and len(y):v[d.session.iloc[g[0]]]=c[y[0]]-c[x[0]]
  signals[s]=v
 d=p['M2K'];t=d.ct_sec.to_numpy();gs=list(d.groupby('session',sort=False).indices.values());hist=[]
 for g in gs:
  sess=d.session.iloc[g[0]];move=signals['M2K'].get(sess,0.);hist.append(abs(move))
  if len(hist)>20 and abs(move)>np.median(hist[-21:-1]) and np.sign(move)==np.sign(signals['ES'].get(sess,0)):
   a['M2K'][g[(t[g]>=32400)&(t[g]<43200)]]=int(np.sign(move))
 return a
