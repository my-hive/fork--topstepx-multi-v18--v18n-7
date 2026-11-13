"""Experiment 114: micro S&P monthly-expiry gamma pin reversion.
Mechanism: dealer gamma hedging dampens cash-open move on monthly option expiry; MES
low contract cost tests whether expiry liquidity effect survives realistic fills.
Falsifier: stressed PnL <=0 or any era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='index-micro-sp-monthly-gamma-pin-reversion'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':39600,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='MES':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);expiry=((dt.dt.weekday==4)&dt.dt.day.between(15,21)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==30600];y=g[t[g]==32400]
    if len(x)and len(y)and expiry[g[0]]:o[g[(t[g]>=32400)&(t[g]<39600)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
