"""Experiment 108: AUD quarterly CPI-session continuation.
Mechanism: Australian CPI/rate expectations are repriced in Asia; Tokyo participation
extends AUD move on quarterly CPI months. Calendar proxy: Jan/Apr/Jul/Oct mid-month.
Falsifier: stressed PnL <=0 or any era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='fx-aud-quarterly-inflation-asia-continuation'
PARAMS={'observe_ct_sec':61200,'entry_ct_sec':64800,'exit_ct_sec':72000,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='6A':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);on=(dt.dt.month.isin([1,4,7,10])&dt.dt.day.between(20,31)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==61200];y=g[t[g]==64800]
    if len(x)and len(y)and on[g[0]]:o[g[(t[g]>=64800)&(t[g]<72000)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
