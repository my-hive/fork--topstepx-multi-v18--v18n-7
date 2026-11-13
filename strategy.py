"""Experiment 101: ultra-bond safe-haven equity shock reversal.
Mechanism: equity opening risk shock creates immediate long-duration hedge demand; once
cash stock liquidity normalizes, temporary flight-to-quality flow in TN retraces.
Falsifier: stressed PnL <=0 or any era PnL <=0.
"""
import numpy as np
FAMILY='cross-asset-equity-ultrabond-opening-safehaven-reversal'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':39600,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={s:np.zeros(len(d),dtype=np.int64)for s,d in p.items()}
 if not all(s in p for s in ('ES','TN')):return a
 sig={};d=p['ES'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for sess,g in d.groupby('session',sort=False).indices.items():
  x=g[t[g]==30600];y=g[t[g]==32400]
  if len(x)and len(y):sig[sess]=-int(np.sign(c[y[0]]-c[x[0]]))
 d=p['TN'];t=d.ct_sec.to_numpy()
 for sess,g in d.groupby('session',sort=False).indices.items():
  if sig.get(sess,0):a['TN'][g[(t[g]>=32400)&(t[g]<39600)]]=-sig[sess]
 return a
