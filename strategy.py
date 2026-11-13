"""Experiment 107: CAD central-bank decision-day continuation.
Mechanism: Bank of Canada policy decisions and guidance release at 09:00 CT on scheduled
Wednesday cadence; initial CAD repricing persists while North American hedgers react.
Calendar proxy: second Wednesday monthly, signal 09:00-09:30, trade 09:30-11:00.
Falsifier: stressed PnL <=0 or any era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='fx-cad-central-bank-decision-continuation'
PARAMS={'observe_ct_sec':32400,'entry_ct_sec':34200,'exit_ct_sec':39600,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='6C':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session.astype(str).str[:10]);on=((dt.dt.weekday==2)&dt.dt.day.between(8,14)).to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==32400];y=g[t[g]==34200]
    if len(x)and len(y)and on[g[0]]:o[g[(t[g]>=34200)&(t[g]<39600)]]=int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
