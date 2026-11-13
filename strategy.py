"""Experiment 45: ES monthly options-expiry dealer-unwind reversal.
Mechanism: third-Friday gamma hedging amplifies pre-open price discovery then unwinds
as cash liquidity arrives. Fade 08:00-08:30 move on known monthly expiry calendar.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='index-options-expiry-dealer-unwind'
PARAMS={'observe_ct_sec':28800,'entry_ct_sec':30600,'exit_ct_sec':36000,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ES':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy(); date=pd.to_datetime(d.session.astype(str).str[:10]); expiry=((date.dt.weekday==4)&date.dt.day.between(15,21)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==28800];y=g[t[g]==30600]
    if len(x)and len(y)and expiry[g[0]]:o[g[(t[g]>=30600)&(t[g]<36000)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
