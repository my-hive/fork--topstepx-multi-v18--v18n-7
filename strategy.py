"""Experiment 44: Treasury weekend-information reversal.
Mechanism: weekend macro/geopolitical headlines are incorporated into thin Sunday/Monday
liquidity and overshoot before cash bond market depth arrives. Fade early Monday ZN move.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='rates-weekend-information-reversal'
PARAMS={'observe_ct_sec':25200,'entry_ct_sec':28800,'exit_ct_sec':36000,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZN':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy(); dates=pd.to_datetime(d.session.astype(str).str[:10]).dt.weekday.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==25200];y=g[t[g]==28800]
    if len(x)and len(y)and dates[g[0]]==0:o[g[(t[g]>=28800)&(t[g]<36000)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
